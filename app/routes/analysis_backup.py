from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.analysis_backup import AnalysisBackup
from schemas.analysis_backup import AnalysisBackupCreate, AnalysisBackupResponse

router = APIRouter(prefix = '/analysis_backup', tags = ['analysis_backup'])

@router.post('/create', response_model = AnalysisBackupResponse, status_code = status.HTTP_201_CREATED)
def create_analysis_backup(analysis_backup: AnalysisBackupCreate, db: Session = Depends(get_db)):
    
    new_analysis_backup = AnalysisBackup(
        analysis_id = analysis_backup.analysis_id,
        user_id = analysis_backup.user_id
    )