from pydantic import BaseModel
from typing import Optional

class BeeTypeCreate(BaseModel):
    name: str
    description: Optional[str] = None

class BeeTypeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class BeeTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
