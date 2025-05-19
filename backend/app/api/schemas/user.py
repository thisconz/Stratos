# User-related Pydantic schemas
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        orm_mode = True