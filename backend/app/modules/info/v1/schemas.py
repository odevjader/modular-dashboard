# backend/app/modules/info/v1/schemas.py
from pydantic import BaseModel
import datetime

class SystemInfoResponse(BaseModel):
    environment: str
    project_name: str
    server_time_utc: datetime.datetime
    api_prefix: str