from pydantic import BaseModel
from typing import Optional

class BeeTypeCreate(BaseModel):
    name: str
    description: str
    user_id: int

class BeeTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    class Config:
        orm_mode = True

class BeeTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None
