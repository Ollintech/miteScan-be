from pydantic import BaseModel
from typing import Optional

class BeeTypeCreate(BaseModel):
    name: str
    description: str
    user_root_id: int

class BeeTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    user_root_id: int

    class Config:
        from_attributes = True

class BeeTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_root_id: Optional[int] = None
