from pydantic import BaseModel
from datetime import datetime

class AnalysisBackupCreate(BaseModel):
    analysis_id: int
    account: str
    file_path: str

class AnalysisBackupResponse(BaseModel):
    id: int
    analysis_id: int
    account: str
    file_path: str
    created_at: datetime

    class Config:
        from_attributes = True