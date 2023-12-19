from __future__ import annotations

import datetime
import itertools
import json
import uuid
from collections import Counter

import celery
import celery.states
from celery import Task


def duplicates(items):
    return list((Counter(items) - Counter(set(items))).keys())


class WFNotFound(Exception):
    pass


class NonRetryableException(Exception):
    pass


def _validate_args(steps, name, app_id):
    assert len(steps) > 0, 'steps is empty'
    for i, step in enumerate(steps):
        attrs = ['name', 'task']
        for attr in attrs:
            assert attr in step, f'step[{i}] does not have "{attr}" key'
            assert isinstance(attr, str), f'step[{i}]["{attr}"] is not a string'
            assert len(step[attr]) > 0, f'step[{i}]["{attr}"] is an empty string'
        if 'queue' in step:
            attr = 'queue'
            assert isinstance(attr, str), f'step[{i}]["{attr}"] is not a string'
            assert len(step[attr]) > 0, f'step[{i}]["{attr}"] is an empty string'
        # assert step['task'] in self.app.tasks, \
        #     f' step - {i} Task {step["task"]} is not registered in the celery application'
    names = [step['name'] for step in steps]
    duplicate_names = duplicates(names)
    assert len(duplicate_names) == 0, f'Steps with duplicate names: {duplicate_names}'

    assert name, 'name cannot be empty'
    assert app_id, 'app_id cannot be empty'


class Workflow:
    RESUME_LOCK_ATTR = 'resume_lock'

    def __init__(self, celery_app, workflow_id=None, steps=None, name=None, app_id=None, description=None):
        self.app = celery_app
        db = self.app.backend.database
        self.wf_col = db.get_collection('workflow_meta')

        assert workflow_id is not None or steps is not None, 'Either workflow_id or steps should not be None'

        if workflow_id is not None:
            # load from db
            res = self.wf_col.find_one({'_id': workflow_id})
            if res:
                self.workflow = res
            else:
                raise WFNotFound(f'Workflow with id {workflow_id} is not found')
        else:  # steps is not None:
            # create workflow object and save to db
            _validate_args(steps, name, app_id)
            self.workflow = {
                '_id': str(uuid.uuid4()),
                'created_at': datetime.datetime.utcnow(),
                'steps': steps,
                'name': name,
                'app_id': app_id,
                'description': description,
                '_status': celery.states.PENDING
            }
            self.wf_col.insert_one(self.workflow)

    def wf_send_task(self, step: dict, step_position: int, task_args: list | tuple = None, task_kwargs: dict = None,
                     **kwargs):
        task_name = step['task']
        task_queue = step.get('queue', None)
        _task_priority = step.get('priority', step_position)
        task_priority = max(0, min(_task_priority, 9))  # between 0 and 9

        # kwargs precedence: 'workflow_id', 'step', 'wf_app_id' > keys in task_kwargs > keys in step['kwargs']
        _task_kwargs = step.get('kwargs', {}) or {}
        _task_kwargs.update(task_kwargs or {})
        _task_kwargs['workflow_id'] = self.workflow['_id']
        _task_kwargs['step'] = step['name']
        _task_kwargs['app_id'] = self.workflow['app_id']

        # print(f'sending task with priority: {task_priority}')
        self.app.send_task(name=task_name, args=task_args, kwargs=_task_kwargs,
                           queue=task_queue, priority=task_priority, **kwargs)

    def start(self, *args, **kwargs):
        """
        Launches the task of the first step in this workflow.

        The task is called with given args and kwargs
        along with additional keyword args "workflow_id" and "step"

        :return: None
        """
        first_step = self.workflow['steps'][0]
        self.wf_send_task(first_step, step_position=1, task_args=args, task_kwargs=kwargs)

    def pause(self, refresh=True):
        """
        Revoke the current running task.

        :return: status of the pause operation and the revoked step if successful
        - dict { "paused": bool, "revoked_step": dict }
        """
        # find running task
        # revoke it

        if refresh:
            self.refresh()

        first_step_not_succeeded = self.get_pending_step()
        if first_step_not_succeeded:
            i, status = first_step_not_succeeded
            if status not in [celery.states.SUCCESS, celery.states.FAILURE]:
                step = self.workflow['steps'][i]
                task_runs = step.get('task_runs', [])
                if task_runs is not None and len(task_runs) > 0:
                    task_id = task_runs[-1]['task_id']
                    # https://docs.celeryq.dev/en/stable/userguide/workers.html#revoke-revoking-tasks
                    self.app.control.revoke(task_id, terminate=True)
                    # print(f' revoked task: {task_id} in step-{i + 1} {step["name"]}')
                    self.workflow['_status'] = celery.states.REVOKED
                    self.update()
                    return {
                        'paused': True,
                        'revoked_step': {
                            'task_id': task_id,
                            'task': step['task'],
                            'name': step['name']
                        }
                    }
        return {
            'paused': False
        }

    def resume(self, force: bool = False, args: list = None, refresh=True) -> dict:
        """
        Submit a new task in the step that has FAILED / REVOKED before and continue the workflow.

        :param force: submit the next task even if its status is not FAILED / REVOKED
        :param args: if the workflow stopped before creating a task instance then its args are not stored.
                     The new task will be triggered with given "args"
        :return: status of the resume operation and the restart if successful
        - dict { "resumed": bool, "restarted_step": dict }
        """
        # find failed / revoked task
        # submit a new task with arguments
        # TODO: if the pending step is not the first step, and it has never run before,
        #  then get the args from the previous step
        # cannot resume the step automatically, that has never started, provide args

        if refresh:
            self.refresh()

        if not self.is_resume_locked():
            first_step_not_succeeded = self.get_pending_step()
            if first_step_not_succeeded:
                i, status = first_step_not_succeeded
                if (status in [celery.states.FAILURE, celery.states.REVOKED]) or force:
                    step = self.workflow['steps'][i]

                    # failed / revoked task instance
                    task_inst = self.get_last_run_task_instance(step)
                    assert not (
                            task_inst is None and args is None), 'no args are provided and there is no last run task'
                    task_args = task_inst['args'] if task_inst is not None else args

                    self.wf_send_task(step, step_position=i + 1, task_args=task_args)
                    self.lock_resume()
                    self.update()

                    # print(f' resuming step {step["name"]}')
                    return {
                        'resumed': True,
                        'restarted_step': {
                            'name': step['name'],
                            'task': step['task']
                        }
                    }
        return {
            'resumed': False
        }

    def on_step_start(self, step_name: str, task_id: str) -> None:
        """
        Called by an instance of WorkflowTask before it starts work.
        Updates the workflow object's step with the task_id and date_start.

        If the task is resubmitted with the old task_id, task_runs will not be updated.

        :param step_name: name of the step that the task is running
        :param task_id: id of the task
        :return: None
        """
        step = self.get_step(step_name)
        step['task_runs'] = step.get('task_runs', [])

        prev_task_ids_set = set(task_run.get('task_id', '') for task_run in step['task_runs'])
        if task_id not in prev_task_ids_set:
            step['task_runs'].append({
                'date_start': datetime.datetime.utcnow(),
                'task_id': task_id
            })

            # print(f' starting {step_name} with task id: {task_id}')
        # else:
        #     print(f' on_step_start {step_name} {task_id} already in prev task runs. not adding.')
        self.workflow['_status'] = celery.states.STARTED
        self.unlock_resume()
        self.update()

    def on_step_success(self, retval: tuple, step_name: str) -> None:
        """
        Called by an instance of WorkflowTask after it completes work.
        calls the next step (if there is one) with the first element of the retval as an argument.

        :param retval: the return value of the task of tuple type. the first element is sent to the next step as an arg
        :param step_name: name of the step that the task is running
        :return:
        """

        next_step_idx = self.get_next_step_idx(step_name)

        try:
            # apply next task with retval
            if next_step_idx is not None:
                next_step = self.workflow['steps'][next_step_idx]
                self.wf_send_task(next_step, step_position=next_step_idx + 1, task_args=(retval[0],))
                # print(f' starting next step {next_step["name"]}')
            else:
                # this is the last step and it succeeded
                self.workflow['_status'] = celery.states.SUCCESS
        finally:
            self.update()

    def on_step_failure(self):
        self.workflow['_status'] = celery.states.FAILURE
        self.update()

    def update(self):
        """
        Update the workflow object in mongo db
        :return: None
        """
        self.workflow['updated_at'] = datetime.datetime.utcnow()
        self.wf_col.update_one({'_id': self.workflow['_id']}, {'$set': self.workflow})

    def lock_resume(self):
        self.workflow[self.RESUME_LOCK_ATTR] = datetime.datetime.utcnow()

    def is_resume_locked(self):
        return bool(self.workflow.get(self.RESUME_LOCK_ATTR, None))

    def unlock_resume(self):
        if self.RESUME_LOCK_ATTR in self.workflow:
            self.workflow[self.RESUME_LOCK_ATTR] = None

    # def update_step_end_time(self, step_name):
    #     step = self.get_step(step_name)
    #     task_runs = step.get('task_runs', [])
    #     if len(task_runs) > 0:
    #         last_task_run = task_runs[-1]
    #         last_task_run['end_time'] = datetime.datetime.utcnow()
    #     self.update()

    def get_step_status(self, step: dict) -> celery.states.state:
        """
        If there are any tasks run for this step, return the status of the last task run, else, return PENDING

        celery.states.FAILURE
        celery.states.PENDING
        celery.states.RETRY
        celery.states.REVOKED
        celery.states.STARTED
        celery.states.SUCCESS

        """
        task_runs = step.get('task_runs', [])
        if len(task_runs) > 0:
            task_id = task_runs[-1]['task_id']
            task_status = self.app.backend.get_status(task_id)
            return task_status
        else:
            return celery.states.PENDING

    def get_pending_step(self) -> tuple[int, celery.states.state] | None:
        """
        finds the index of the first step whose status is not celery.states.SUCCESS
        if all steps have succeeded, it returns None
        :return: tuple (index:int, status:CELERY.states.STATE)
        """
        statuses = [(i, self.get_step_status(step)) for i, step in enumerate(self.workflow['steps'])]
        return next((s for s in statuses if s[1] != celery.states.SUCCESS), None)

    def get_workflow_status(self) -> celery.states.state:
        """
        The workflow status is a summative status that is determined by the
        status of the initial step that is not marked as "SUCCESS"
        which is referred to as a "pending step".

        - PENDING - the pending step is the first step in the workflow and its status is pending.
        - STARTED - the status of the pending step is one of STARTED, RETRY, PENDING.
        - REVOKED - the pending step was revoked, the workflow can be resumed.
        - FAILURE - the pending step was failed, the workflow can be resumed.
        - SUCCESS - all steps have succeeded.

        :return: celery.states.state
        """
        pending_step = self.get_pending_step()
        if pending_step:
            step_idx, task_status = pending_step
            if step_idx == 0 and task_status == celery.states.PENDING:
                return celery.states.PENDING
            if task_status in [celery.states.STARTED, celery.states.RETRY, celery.states.PENDING]:
                return celery.states.STARTED
            else:
                return task_status
        else:
            return celery.states.SUCCESS

    def get_step(self, step_name):
        it = itertools.dropwhile(lambda step: step['name'] != step_name, self.workflow['steps'])
        return next(it, None)

    def get_next_step_idx(self, step_name: str) -> int | None:
        # it = itertools.dropwhile(lambda step: step['name'] != step_name, self.workflow['steps'])
        # skip_one_it = itertools.islice(it, 1, None)
        # return next(skip_one_it, None)

        curr_step_idx = None
        for i, step in enumerate(self.workflow['steps']):
            if step['name'] == step_name:
                curr_step_idx = i
                break
        if curr_step_idx is not None and curr_step_idx < len(self.workflow['steps']) - 1:
            return curr_step_idx + 1
        return None

    def get_task_instance(self, task_id, date_start=None):
        col = self.app.backend.collection
        task = col.find_one({'_id': task_id})
        if task is not None:
            task['date_start'] = date_start
            if 'result' in task and task['result'] is not None:
                try:
                    task['result'] = json.loads(task['result'])
                except Exception as e:
                    print('unable to parse result json', e, task['_id'], task['result'])
            if 'date_done' in task:
                try:
                    task['date_done'] = datetime.datetime.strptime(task['date_done'], "%Y-%m-%dT%H:%M:%S.%f")
                except Exception as e:
                    print('unable to convert date_done date string into date object', e, task['_id'], task['date_done'])

        return task

    def get_last_run_task_instance(self, step):
        """
        returns the latest task instance (task object) from the step object
        """
        task_runs = step.get('task_runs', [])
        if task_runs is not None and len(task_runs) > 0:
            task_id = task_runs[-1]['task_id']
            date_start = task_runs[-1].get('date_start', None)
            return self.get_task_instance(task_id, date_start)

    def refresh(self):
        workflow_id = self.workflow['_id']
        res = self.wf_col.find_one({'_id': workflow_id})
        if res:
            self.workflow = res
        else:
            raise WFNotFound(f'Workflow with id {workflow_id} is not found')

    def get_embellished_workflow(self, last_task_run=True, prev_task_runs=False, refresh=True):
        """

        @param last_task_run: include last run task for each step: boolean
        @param prev_task_runs: include previous task runs for each step: boolean
        @param refresh: fetch latest workflow state from db
        :return:

        """
        if refresh:
            self.refresh()
        status = self.get_workflow_status()
        pending_step_idx, _ = self.get_pending_step() or (None, None)
        steps = []
        for step in self.workflow['steps']:
            emb_step = {
                'name': step['name'],
                'task': step['task'],
                'status': self.get_step_status(step)
            }
            if last_task_run:
                emb_step['last_task_run'] = self.get_last_run_task_instance(step)
            if prev_task_runs:
                emb_step['prev_task_runs'] = [
                    self.get_task_instance(t['task_id'], t.get('date_start', None)) for t in
                    step.get('task_runs', [])[:-1]
                ]
            steps.append(emb_step)

        # number of steps done is same of index of the pending step
        # if all steps are complete pending_step_idx is None, then steps_done is len(steps)
        return {
            'id': self.workflow['_id'],
            'name': self.workflow.get('name', None),
            'app_id': self.workflow.get('app_id', None),
            'description': self.workflow.get('description', None),
            'created_at': self.workflow.get('created_at', None),
            'updated_at': self.workflow.get('updated_at', None),
            'status': status,
            'steps_done': pending_step_idx if pending_step_idx is not None else len(steps),
            'total_steps': len(steps),
            'steps': steps,
            self.RESUME_LOCK_ATTR: self.workflow.get(self.RESUME_LOCK_ATTR, None)
        }


class WorkflowTask(Task):  # noqa
    # trail = True

    def __init__(self):
        self.workflow = None
        self.id = None
        self.workflow_id = None
        self.step = None

    def before_start(self, task_id, args, kwargs):
        # print(f' before_start, task_id:{task_id}, kwargs:{kwargs} name:{self.name}')

        # A task's result in the backend is not updated until the tasks succeeds, fails, revoked
        # or updated through code after it start execution.
        # To the observers that task will appear to be in a pending state.
        # Programmatically setting the state to PROGRESS before starting execution.
        # setting task_track_started=True accomplishes the same while setting state as started. (yet to be tested)
        # self.update_progress({})

        self.id = task_id

        if 'workflow_id' in kwargs and 'step' in kwargs:
            workflow_id = kwargs['workflow_id']
            step = kwargs['step']
            self.workflow_id = workflow_id
            self.step = step
            self.workflow = Workflow(self.app, workflow_id)
            self.workflow.on_step_start(step, task_id)

    def on_success(self, retval, task_id, args, kwargs):
        # print(f' on_success, task_id: {task_id}, kwargs: {kwargs}')

        if self.workflow is not None:
            self.workflow.on_step_success(retval, kwargs['step'])

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # print('in on_failure', exc, task_id, args, kwargs, einfo)
        if self.workflow is not None:
            # self.workflow.on_step_failure(exc, kwargs['step'])
            self.workflow.on_step_failure()

    def update_progress(self, progress_obj):
        # called_directly: This flag is set to true if the task was not executed by the worker.
        if not self.request.called_directly:
            self.update_state(
                state='STARTED',
                meta=progress_obj
            )
