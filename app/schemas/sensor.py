from pydantic import BaseModel
from datetime import datetime

class SensorDataCreate(BaseModel):
    account_name: str
    hive_name: str
    temperature: float
    humidity: float

class SensorResponse(BaseModel):
    id: int
    hive_id: int
    temperature: float
    humidity: float
    created_at: datetime

    class Config:
        orm_mode = True
