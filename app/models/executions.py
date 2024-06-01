from datetime import datetime
from pydantic import BaseModel

class ExecutionInfo(BaseModel):
    id: str
    status: str
    time: int
    start_time: datetime
    task: str
