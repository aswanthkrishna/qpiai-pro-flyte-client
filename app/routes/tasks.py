from typing import List
import uuid

from fastapi import APIRouter

from ..models.executions import ExecutionInfo
from ..models.auto_annotate import AutoAnnotateInputs
from ..models.train import TrainMMdetectionInputs
from ..models.dataset_health_check import DatasetHealthCheckInputs


from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
from flytekit.models.core.execution import WorkflowExecutionPhase

from flytekit.models.common import Labels
from flytekit.tools.translator import Options

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


    execution_name = str(uuid.uuid4().hex)[:8]
    s = execution_name[0] if execution_name[0].islower() else 'a'
    execution_name = s + execution_name

    if request.user_id: execution_name = request.user_id + "-" + execution_name
    print(execution_name)

    task_inputs = dict(request)
    user_id = task_inputs.pop("user_id")

    if request.model_repo_path == "grounding-dino" or request.model_repo_path == None:
        task = remote.fetch_task(
                name="grounding_dino.auto_annotate",
                #version="jjwsygsOCkpn3wJtegvLrA",
                version="3Df3PhEGVIiPq5zukXcKag",
                project=PROJECT_NAME,
                domain=PROJECT_DOMAIN
            )
        print(task)
        print(request)
        task_inputs.pop("model_repo_path")
    else:
        task = remote.fetch_task(
                name="mmdetection.mmdet_infer.mmdetection_batch_infer",
                version="mb6MjR8j13lFKPkzTUGfYw", #"E0sPFaXxFUdntSAaQv3f-Q",
                project=PROJECT_NAME,
                domain=PROJECT_DOMAIN
            )
        print(task)
        print(request)
        task_inputs.pop("class_dict")

    # options=Options(
    #     labels=Labels({"user":user_id}),
    # ),
    
    execution = remote.execute(task, inputs=task_inputs, wait=False, project=PROJECT_NAME, domain=PROJECT_DOMAIN, execution_name=execution_name, tags=[f"user:{user_id}"])
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

@router.post("/train_mmdetection")
def train_mmdetection(request: TrainMMdetectionInputs) -> ExecutionInfo:

    task = remote.fetch_task(
            name="mmdetection.train.train",
            version="szAhaOC7FuDymL378A2ghw",
            project=PROJECT_NAME,
            domain=PROJECT_DOMAIN
        )
    print(task)

    execution_name = str(uuid.uuid4().hex)[:8]
    s = execution_name[0] if execution_name[0].islower() else 'a'
    execution_name = s + execution_name

    if request.user_id: execution_name = request.user_id + "-" + execution_name
    print(execution_name)

    task_inputs = dict(request)
    task_inputs["user_id"]
    print(task_inputs)
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

@router.post("/dataset_health_check")
def train_mmdetection(request: DatasetHealthCheckInputs) -> ExecutionInfo:

    task = remote.fetch_task(
            name="dataset_health_check.workflow.dataset_health",
            project=PROJECT_NAME,
            domain=PROJECT_DOMAIN
        )
    print(task)

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
