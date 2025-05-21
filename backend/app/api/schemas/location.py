from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class LocationBase(BaseModel):
    name: str
    path: str

class LocationCreate(LocationBase):
    pass

class LocationUpdate(LocationBase):
    pass

class LocationOut(LocationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
