
from pydantic import BaseModel, HttpUrl

class DatasetHealthCheckInputs(BaseModel):
    callback_url: str
    s3_secret_key: str
    dataset_Id: str
    s3_endpoint_url: str
    path_id: str
    action: str
    s3_access_key: str
    user_id: str
    action: str = 'callback'