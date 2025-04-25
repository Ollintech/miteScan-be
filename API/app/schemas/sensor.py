from pydantic import BaseModel

class SensorRead(BaseModel):
    colmeia_id: int
    temperature: float
    humidity: float

class SensorResponse(BaseModel):
    id: int
    colmeia_id: int
    temperature: float
    humidity: float

    class Config:
        from_attributes = True
