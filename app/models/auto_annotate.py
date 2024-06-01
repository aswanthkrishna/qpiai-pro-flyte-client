
from pydantic import BaseModel
from typing import Dict, Optional

class AutoAnnotateInputs(BaseModel):
    class_dict : Dict[str, str]
    repo_path: str
    s3_access_key: str
    s3_secret_key: str 
    s3_endpoint_url: str
    fiftyone_controller_endpoint: str
    branch: str = "main"
    view_name: Optional[str] = None
    user_id: Optional[str] = None

