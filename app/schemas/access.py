from pydantic import BaseModel

class AccessResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True