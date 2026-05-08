from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive_analysis import HiveAnalysis
from models.hive import Hive
from schemas.hive_analysis import HiveAnalysisCreate, HiveAnalysisResponse
from core.auth import require_access
import shutil
import os
from ai.predict import predict_image
from datetime import datetime

router = APIRouter(prefix = '/hive_analyses', tags = ['Hive Analyses'])

@router.post('/create', response_model = HiveAnalysisResponse, status_code = status.HTTP_201_CREATED)
def create_hive_analysis(hive_analysis: HiveAnalysisCreate, db: Session = Depends(get_db)):
    """Rota legado (JSON) - Mantida para compatibilidade, mas menos segura."""
    hive = db.query(Hive).filter(Hive.id == hive_analysis.hive_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')

    new_hive_analysis = HiveAnalysis(
        hive_id = hive_analysis.hive_id,
        account = hive.account,
        image_path = hive_analysis.image_path,
        varroa_detected = hive_analysis.varroa_detected,
        bee_status = hive_analysis.bee_status,
        detection_confidence = hive_analysis.detection_confidence
    )

    db.add(new_hive_analysis)
    db.commit()
    db.refresh(new_hive_analysis)
    return new_hive_analysis

@router.post('/create-protected', response_model = HiveAnalysisResponse, status_code = status.HTTP_201_CREATED)
async def create_protected_analysis(
    hive_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Rota SEGURA: Recebe o arquivo, processa na IA e salva o resultado final."""
    
    # 1. Verificar colmeia
    hive = db.query(Hive).filter(Hive.id == hive_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')

    # 2. Salvar imagem da análise
    os.makedirs("uploads/analyses", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"uploads/analyses/{hive.account}_hive{hive_id}_{timestamp}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Chamar IA para predição REAL
    try:
        print(f"\n--- 🔍 NOVA ANÁLISE INICIADA ---")
        print(f"📸 Imagem recebida: {file.filename}")
        print(f"🐝 Colmeia ID: {hive_id}")
        print(f"🤖 Enviando para o modelo de IA...")
        
        ai_result = predict_image(file_path)
        
        status_ai = ai_result.get("classe", "normal")
        confianca = ai_result.get("confianca", 0.0)
        
        print(f"✅ Processamento concluído!")
        print(f"⚖️ VEREDITO FINAL: {status_ai.upper()} ({confianca*100:.1f}% de confiança)")
        print(f"--------------------------------\n")
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Erro no processamento da IA: {str(e)}")

    # 4. Salvar no banco
    new_hive_analysis = HiveAnalysis(
        hive_id = hive_id,
        account = hive.account,
        image_path = file_path,
        varroa_detected = (status_ai == "varroa"),
        bee_status = status_ai,
        detection_confidence = confianca
    )

    db.add(new_hive_analysis)
    db.commit()
    db.refresh(new_hive_analysis)

    return new_hive_analysis

@router.get('/all', response_model = list[HiveAnalysisResponse])
def get_all_hive_analyses(account: str, hive_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(HiveAnalysis).join(Hive).filter(Hive.account == account)
    
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