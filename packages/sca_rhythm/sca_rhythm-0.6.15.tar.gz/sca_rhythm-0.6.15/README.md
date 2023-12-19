# Rhythm

Rhythm allows you to design and control workflows made of Celery tasks. A workflow is a sequence of steps to run one
after the other. Rhythm simplifies the process of executing workflows consisting of long-running tasks with reliability.

The following are the features of Rhythm workflows:

- If a workflow consisting of three steps (S1, S2, and S3) encounters a failure while executing S2 (even after retries
  by Celery), it is possible to resume the workflow later. Resuming the workflow with restart S2 with previous arguments
  and after its completion S3 will be run.
- A workflow can be paused and resumed later.
- You can keep track of which step is currently running, as well as its progress.

### Installation

```
pip install sca-rhythm
```

see on [pypi](https://pypi.org/project/sca-rhythm/)

### Prerequisites

Celery app should be configured with a mongo database backend.

### Create Tasks with `WorkflowTask` class

```python
import os
import time

from celery import Celery

from sca_rhythm import WorkflowTask

app = Celery("tasks")


@app.task(base=WorkflowTask, bind=True)
def task1(self, batch_id, **kwargs):
    print(f'task - {os.getpid()} 1 starts with {batch_id}')
    # do work
    time.sleep(1)

    # update progress to result backend
    # sets the task's state as "PROGRESS"
    self.update_progress({
        'done': 2873,
        'total': 100000
    })

    # do some more work
    return batch_id, {'return_obj': 'foo'}
```

#### :warning: Task Constraints :warning:

1. The task signature must contain `**kwargs` for the workflow orchestration to function.
2. The return type must be of list / tuple type and the first element of the return value is sent to the next task as
   its argument.

### Create Workflows with `Workflow` class

```python
from celery import Celery

from sca_rhythm import Workflow

steps = [
    {
        'name': 'inspect',
        'task': 'tasks.inspect'
        'queue': 'q1',
    },
    {
        'name': 'archive',
        'task': 'tasks.archive',
        'queue': 'q1',
    },
    {
        'name': 'stage',
        'task': 'tasks.stage',
        'queue': 'q2',
        'priority': 5
    }
]

wf = Workflow(app, steps=steps, name='archive_batch', app_id='app')
wf.start('batch-id-test')
```

The provided code defines a workflow consisting of multiple steps, each representing a task to be executed in a specific order. The workflow is initiated with a unique identifier, and its steps are configured with task names, associated queues, and optional priorities.

Each step is represented as a dictionary with the following properties:

- name: A descriptive name for the step.
- task: The task to be executed, specified as a string containing the task's import path.
- queue: The Celery queue to which the task should be sent.
- priority (optional): An integer (between 0 and 9) indicating the priority of the task in the queue. If not provided, the priority is set to the step's position in the workflow. If there are more than 9 tasks, tasks in positions 10 and above will all recieve priority 9.

**Priority Scheme**:
The priority scheme is designed to optimize the execution of tasks within the same workflow. Tasks with higher priorities are executed before those with lower priorities. If no priority is specified, the default priority is set to the step's position in the workflow. This scheme ensures that tasks within a workflow are executed sequentially with increasing priority, minimizing the likelihood of interweaving tasks from different workflows.

### Pause and Resume Workflows

Pausing a workflow stop the current running task and resuming a workflow will restart the stopped task with the same
arguments.

```python
wf = Workflow(app, workflow_id='2f87decb-a431-472b-b26e-32c894993881')

wf.pause()

wf.resume()
```

### Build & Publish

```bash
poetry install
poetry publish --build
```

### Task Status

- PENDING: Task state is unknown (assumed pending since you know the id).
- STARTED: Task was started by a worker (task_track_started = True)
- SUCCESS: Task succeeded
- FAILURE: Task failed
- REVOKED: Task was revoked
- RETRY: Task is waiting for retry.

### Workflow Status

The workflow status is a summative status that is determined by the status of the initial step that is not marked as "
SUCCESS," which is referred to as a "pending step".

- PENDING - the pending step is the first step in the workflow and its status is pending.
- STARTED - the status of the pending step is one of STARTED, RETRY, PENDING.
- REVOKED - the pending step was revoked, the workflow can be resumed.
- FAILURE - the pending step was failed, the workflow can be resumed.
- SUCCESS - all steps have succeeded.

#### Status Groups:

- DONE: { SUCCESS, FAILURE, REVOKED }
- ACTIVE: !DONE