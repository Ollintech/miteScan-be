from pydantic import BaseModel

class SensorRead(BaseModel):
    colmeia_id: int
    temperature: float
    humidity: float