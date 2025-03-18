from pydantic import BaseModel
from datetime import datetime

class AnalysisBackupCreate(BaseModel):
    analysis_id: int
    user_id: int
    file_path: str

class AnalysisBackupCreate(BaseModel):
    id: int
    analysis_id: int
    user_id: int
    file_path: str

    class Config:
        orm_mode = True