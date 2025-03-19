from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True