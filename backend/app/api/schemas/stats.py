# Stats & analytics schemas
from pydantic import BaseModel

class StatsResponse(BaseModel):
    total_users: int
    total_files: int
    deleted_files: int