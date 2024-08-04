
from pydantic import BaseModel
from typing import Dict, Optional

class TrainMMdetectionInputs(BaseModel):
    repo_path: str
    s3_access_key: str
    s3_secret_key: str 
    s3_endpoint_url: str
    model_repo_path: str
    experiment_id: Optional[str]
    run_id: Optional[str]
    user_id: Optional[str]
    base_model: str
    branch: str = "main"
    mlflow_url: str = "http://192.168.9.13:5000"
    max_epochs: int = 100


