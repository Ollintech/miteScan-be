from pydantic import BaseModel

class BeeTypeCreate(BaseModel):
    name: str
    description: str
    user_id: int

    class Config:
        orm_mode = True

class BeeTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    class Config:
        orm_mode = True