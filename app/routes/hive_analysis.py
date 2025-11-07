from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive_analysis import HiveAnalysis
from models.hive import Hive
from schemas.hive_analysis import HiveAnalysisCreate, HiveAnalysisResponse
from core.auth import require_access

router = APIRouter(prefix = '/hive_analyses', tags = ['Hive Analyses'])

@router.post('/create', response_model = HiveAnalysisResponse, status_code = status.HTTP_201_CREATED)
def create_hive_analysis(hive_analysis: HiveAnalysisCreate, db: Session = Depends(get_db)):

    new_hive_analysis = HiveAnalysis(
        hive_id = hive_analysis.hive_id,
        account = hive_analysis.account,
        image_path = hive_analysis.image_path,
        varroa_detected = hive_analysis.varroa_detected,
        detection_confidence = hive_analysis.detection_confidence
    )

    db.add(new_hive_analysis)
    db.commit()
    db.refresh(new_hive_analysis)

    return new_hive_analysis

@router.get('/all', response_model = list[HiveAnalysisResponse])
def get_all_hive_analyses(account: str, hive_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(HiveAnalysis).join(Hive).filter(Hive.account == account)
    
    if not query:
        raise HTTPException(status_code=404, detail='Não existem colmeias cadastradas para este usuário.')

    if hive_id is not None:
        query = query.filter(HiveAnalysis.hive_id == hive_id)

    hive_analysis = query.all()

    if not hive_analysis:
        raise HTTPException(status_code = 404, detail = 'Não há registros de analises de colmeias.')
    
    return hive_analysis

@router.get('/hive/{hive_id}', response_model = HiveAnalysisResponse)
def get_last_analysis_by_hive(hive_id: int, db: Session = Depends(get_db)):
    hive_analysis = db.query(HiveAnalysis).join(Hive).filter(HiveAnalysis.hive_id == hive_id).order_by(HiveAnalysis.created_at.desc()).first()
    if not hive_analysis:
        raise HTTPException(status_code = 404, detail = 'Análise da colmeia não encontrada.')
    
    return hive_analysis

@router.get('/{hive_analysis_id}', response_model = HiveAnalysisResponse)
def get_hive_analysis(hive_analysis_id: int, db: Session = Depends(get_db)):
    hive_analysis = db.query(HiveAnalysis).join(Hive).filter(HiveAnalysis.id == hive_analysis_id).first()

    if not hive_analysis:
        raise HTTPException(status_code = 404, detail = 'Análise da colmeia não encontrada.')
    
    return hive_analysis

@router.delete('/{hive_analysis_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_hive_analysis(hive_analysis_id: int, db: Session = Depends(get_db)):
    hive_analysis = db.query(HiveAnalysis).filter(HiveAnalysis.id == hive_analysis_id).first()

    if not hive_analysis:
        raise HTTPException(status_code = 404, detail = 'Análise de colmeia não encontrada.')
    
    db.delete(hive_analysis)
    db.commit()

    return {'message': f'Análise de colmeia deletada com sucesso!'}