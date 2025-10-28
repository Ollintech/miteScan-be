from pydantic import BaseModel
from datetime import datetime

class AnalysisBackupCreate(BaseModel):
    analysis_id: int
    user_root_id: int
    file_path: str
    created_at: datetime

class AnalysisBackupResponse(BaseModel):
    id: int
    analysis_id: int
    user_root_id: int
    file_path: str

    class Config:
        from_attributes = True