from pydantic import BaseModel
from datetime import datetime

class HiveAnalysisCreate(BaseModel):
    hive_id: int
    account: str
    image_path: str
    varroa_detected: bool = False
    detection_confidence: float

class HiveAnalysisResponse(BaseModel):
    id: int
    hive_id: int
    account: str
    image_path: str
    varroa_detected: bool = False
    detection_confidence: float
    created_at: datetime

    class Config:
        from_attributes = True
