from typing import List

from fastapi import APIRouter

from ..models.executions import ExecutionInfo

from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
from flytekit.models.core.execution import WorkflowExecutionPhase

router = APIRouter()

PROJECT_NAME = "flytesnacks"

remote = FlyteRemote(Config.auto(config_file='config.yaml'))

@router.get("/executions")
def get_executions() -> List[ExecutionInfo]:

    executions, _ = remote.client.list_executions_paginated(
            PROJECT_NAME,
            "development",
        )
    
    execution_infos = []

    for execution in executions : 
            
        name = execution.id.name
        status = WorkflowExecutionPhase.enum_to_string(execution.closure.phase)
        time = int(execution.closure.duration.seconds)
        start_time = execution.closure.started_at
        task = execution.spec.launch_plan.name

        execution_infos.append(ExecutionInfo(
                                    id=name,
                                    status=status,
                                    time=time,
                                    start_time=start_time,
                                    task=task
                                ))
    print(executions)

    return execution_infos