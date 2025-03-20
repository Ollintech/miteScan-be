from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True