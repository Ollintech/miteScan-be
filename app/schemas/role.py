from pydantic import BaseModel, Optional

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None