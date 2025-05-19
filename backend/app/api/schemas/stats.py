from pydantic import BaseModel, Field

class StatsResponse(BaseModel):
    total_users: int = Field(ge=0)
    total_files: int = Field(ge=0)
    deleted_files: int = Field(ge=0)