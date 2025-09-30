from pydantic import BaseModel

class SensorRead(BaseModel):
    hive_id: int
    temperature: float
    humidity: float

class SensorResponse(BaseModel):
    id: int
    hive_id: int
    temperature: float
    humidity: float

    class Config:
        from_attributes = True
