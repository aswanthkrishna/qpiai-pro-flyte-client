from typing import List
import uuid

from fastapi import APIRouter

from ..models.executions import ExecutionInfo
from ..models.auto_annotate import AutoAnnotateInputs


from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
from flytekit.models.core.execution import WorkflowExecutionPhase

router = APIRouter()

PROJECT_NAME = "flytesnacks"
PROJECT_DOMAIN = "development"

remote = FlyteRemote(Config.auto(config_file='config.yaml'))

@router.get("/tasks")
def get_tasks():

    tasks = remote.fetch_task(
            name="grounding_dino.auto_annotate",
            version="6ibxAMdGXiZFd2AXfmoIuw"
        )
    print(tasks)
    
    return {}

@router.post("/auto_annotate")
def auto_annotate(request: AutoAnnotateInputs) -> ExecutionInfo:

    task = remote.fetch_task(
            name="grounding_dino.auto_annotate",
            version="Zbn_dOa46PXfX09tY_7zzg",
            project=PROJECT_NAME,
            domain=PROJECT_DOMAIN
        )
    print(task)
    print(request)

    execution_name = str(uuid.uuid4().hex)[:8]
    s = execution_name[0] if execution_name[0].islower() else 'a'
    execution_name = s + execution_name

    if request.user_id: execution_name = request.user_id + "-" + execution_name
    print(execution_name)

    task_inputs = dict(request)
    task_inputs.pop("user_id")

    execution = remote.execute(task, inputs=task_inputs, wait=False, project=PROJECT_NAME, domain=PROJECT_DOMAIN, execution_name=execution_name)
    print(execution)
    name = execution.id.name
    status = WorkflowExecutionPhase.enum_to_string(execution.closure.phase)
    time = int(execution.closure.duration.seconds)
    start_time = execution.closure.started_at
    task = execution.spec.launch_plan.name


    return ExecutionInfo(id=name,
                        status=status,
                        time=time,
                        start_time=start_time,
                        task=task
                     )

