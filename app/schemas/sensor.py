from pydantic import BaseModel
from datetime import datetime

class SensorRead(BaseModel):
    hive_id: int
    temperature: float
    humidity: float

class SensorResponse(BaseModel):
    id: int
    hive_id: int
    temperature: float
    humidity: float
    created_at: datetime

    class Config:
        from_attributes = True
