from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.analysis_backup import AnalysisBackup
from schemas.analysis_backup import AnalysisBackupCreate, AnalysisBackupResponse
from datetime import datetime

router = APIRouter(prefix = '/analysis_backup', tags = ['Analysis Backup'])

# Rota de criação de backup de análise
@router.post('/create', response_model = AnalysisBackupResponse, status_code = status.HTTP_201_CREATED)
def create_analysis_backup(analysis_backup: AnalysisBackupCreate, db: Session = Depends(get_db)):
    
    new_analysis_backup = AnalysisBackup(
        analysis_id = analysis_backup.analysis_id,
        user_id = analysis_backup.user_id,
        file_path = analysis_backup.file_path,
        created_at = datetime.utcnow
    )

    db.add(new_analysis_backup)
    db.commit()
    db.refresh(new_analysis_backup)

    return new_analysis_backup

# Rota para mostrar o backup da análise
@router.get('/get:{analysis_backup_id}', response_model = AnalysisBackupResponse)
def get_analysis_backup(analysis_backup_id: int, db: Session = Depends(get_db)):
    analysis_backup = db.query(AnalysisBackup).filter(AnalysisBackup.id == analysis_backup_id).first()

    if not analysis_backup:
        raise HTTPException(status_code = 404, detail = 'Análise de Backup não encontrada.')
    
    return analysis_backup

# Rota para deletar o backup da análise
@router.delete('/delete:{analysis_backup_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_analysis_backup(analysis_backup_id: int, db: Session = Depends(get_db)):
    analysis_backup = db.query(AnalysisBackup).filter(AnalysisBackup.id == analysis_backup_id).first()

    if not analysis_backup:
        raise HTTPException(status_code = 404, detail = 'Análise de Backup não encontrada.')
    
    db.delete(analysis_backup)
    db.commit()

    return {'message' : 'Análise de Backup deletada com sucesso!'}
