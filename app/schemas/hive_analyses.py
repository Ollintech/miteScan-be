from pydantic import BaseModel
from datetime import datetime

class HiveAnalysesCreate(BaseModel):
    hive_id: int
    user_id: int
    image_path: str
    varroa_detected: bool = False
    detection_confidence: float

    class Config:
        orm_mode = True

class HiveAnalysesCreate(BaseModel):
    id: int
    hive_id: int
    user_id: int
    image_path: str
    varroa_detected: bool = False
    detection_confidence: float
    created_at: datetime

    class Config:
        orm_mode = True