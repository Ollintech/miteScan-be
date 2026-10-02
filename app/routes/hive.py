from fastapi import Depends, APIRouter, HTTPException, status, Query, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from models.sensor_readings import Sensor
from models.hive_analysis import HiveAnalysis
from models.analysis_backup import AnalysisBackup
from models.user_root import UserRoot
from models.user_associated import UserAssociated
from schemas.hive import HiveResponse
from typing import List, Optional, Union
from core.auth import (
    get_current_user_root,
    get_current_user_root_optional,
    get_current_user_associated_optional
)
from supabase import create_client, Client
import os
import re

router = APIRouter(prefix='/{account}/hives', tags=['Hives'])

# Inicializa o cliente do Supabase usando as variáveis do .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def sanitize_filename(name: str) -> str:
    """Remove caracteres inválidos para nomes de arquivos."""
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_")

def check_permission(account: str, current_user: Union[UserRoot, UserAssociated]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    if current_user.account != account:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não permitida para esta conta")

async def upload_image_to_supabase(image: UploadFile, account: str, hive_name: str) -> Optional[str]:
    """Faz o upload da imagem para o bucket do Supabase e retorna a URL pública."""
    if not image or not image.filename or not supabase:
        return None
    
    try:
        safe_hive_name = sanitize_filename(hive_name)
        safe_file_name = sanitize_filename(image.filename)
        file_path = f"hives/{account}_{safe_hive_name}_{safe_file_name}"
        
        contents = await image.read()
        
        bucket_name = "images-mitescan" 
        
        supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=contents,
            file_options={"content-type": image.content_type, "upsert": "true"}
        )
        
        public_url_res = supabase.storage.from_(bucket_name).get_public_url(file_path)
        return public_url_res
    except Exception as e:
        print(f"Erro ao enviar imagem para o Supabase: {e}")
        return None

@router.post('/create', response_model=HiveResponse, status_code=status.HTTP_201_CREATED)
async def create_hive(
    account: str = Path(...),
    name: str = Form(...),
    bee_type_id: str = Form(...),
    location_lat: str = Form(...),
    location_lng: str = Form(...),
    size: str = Form(...),
    humidity: Optional[str] = Form(None),
    temperature: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db), 
    current_user_root: Optional[UserRoot] = Depends(get_current_user_root_optional),
    current_user_associated: Optional[UserAssociated] = Depends(get_current_user_associated_optional)
):
    current_user = current_user_root or current_user_associated
    check_permission(account, current_user) 
    
    if db.query(Hive).filter(Hive.name == name, Hive.account == account).first():
        raise HTTPException(status_code=400, detail='Uma colmeia com esse nome já foi cadastrada.')

    try:
        b_id = int(bee_type_id)
        lat = float(location_lat)
        lng = float(location_lng)
        s_size = int(size)
        hum = float(humidity) if humidity and humidity not in ['null', 'undefined', ''] else None
        temp = float(temperature) if temperature and temperature not in ['null', 'undefined', ''] else None
    except ValueError:
        raise HTTPException(status_code=422, detail="Dados numéricos inválidos")

    image_path = await upload_image_to_supabase(image, account, name)

    new_hive = Hive(
        name=name, account=account, bee_type_id=b_id,
        location_lat=lat, location_lng=lng, size=s_size,
        humidity=hum, temperature=temp, image_path=image_path
    )

    db.add(new_hive)
    db.commit()
    db.refresh(new_hive)
    return new_hive

@router.get('/all', response_model=List[HiveResponse])
def get_all_hives(account: str = Path(...), db: Session = Depends(get_db)):
    hives = db.query(Hive).filter(Hive.account == account).all()
    if not hives:
        raise HTTPException(status_code=404, detail='Não existem colmeias cadastradas para este usuário.')
    return hives

@router.get('/{hive_id}', response_model=HiveResponse)
def get_hive(account: str = Path(...), hive_id: int = Path(...), db: Session = Depends(get_db)):
    hive = db.query(Hive).filter(Hive.id == hive_id, Hive.account == account).first()
    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')
    return hive

@router.put('/{hive_id}', response_model=HiveResponse)
async def update_hive(
    account: str = Path(...),
    hive_id: int = Path(...),
    name: Optional[str] = Form(None),
    bee_type_id: Optional[str] = Form(None),
    location_lat: Optional[str] = Form(None),
    location_lng: Optional[str] = Form(None),
    size: Optional[str] = Form(None),
    humidity: Optional[str] = Form(None),
    temperature: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user_root: Optional[UserRoot] = Depends(get_current_user_root_optional),
    current_user_associated: Optional[UserAssociated] = Depends(get_current_user_associated_optional)
):
    current_user = current_user_root or current_user_associated
    check_permission(account, current_user) 

    hive = db.query(Hive).filter(Hive.id == hive_id, Hive.account == account).first()
    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')
    
    target_name = name if name else hive.name
    if name:
        duplicate = db.query(Hive).filter(Hive.name == name, Hive.account == account, Hive.id != hive_id).first()
        if duplicate:
            raise HTTPException(status_code=400, detail='Uma colmeia com esse nome já foi cadastrada.')
        hive.name = name

    try:
        if bee_type_id: hive.bee_type_id = int(bee_type_id)
        if location_lat: hive.location_lat = float(location_lat)
        if location_lng: hive.location_lng = float(location_lng)
        if size: hive.size = int(size)
        if humidity is not None: hive.humidity = float(humidity) if humidity not in ['null', 'undefined', ''] else None
        if temperature is not None: hive.temperature = float(temperature) if temperature not in ['null', 'undefined', ''] else None
    except ValueError:
        raise HTTPException(status_code=422, detail="Dados numéricos inválidos")

    if image and image.filename:
        new_image_path = await upload_image_to_supabase(image, account, target_name)
        if new_image_path:
            hive.image_path = new_image_path

    db.commit()
    db.refresh(hive)
    return hive

@router.delete('/{hive_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_hive(
    account: str = Path(...),
    hive_id: int = Path(...), 
    db: Session = Depends(get_db), 
    current_user_root: Optional[UserRoot] = Depends(get_current_user_root_optional),
    current_user_associated: Optional[UserAssociated] = Depends(get_current_user_associated_optional),
    confirm: Optional[bool] = Query(False) 
):
    current_user = current_user_root or current_user_associated
    check_permission(account, current_user) 

    hive = db.query(Hive).filter(Hive.id == hive_id, Hive.account == account).first()
    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')
    
    sensores = db.query(Sensor).filter(Sensor.hive_id == hive_id).all()
    analyses = db.query(HiveAnalysis).filter(HiveAnalysis.hive_id == hive_id).all()

    if (sensores or analyses) and not confirm:
        details = []
        if sensores: details.append(f"{len(sensores)} leituras de sensores")
        if analyses: details.append(f"{len(analyses)} análises")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A colmeia {hive_id} possui {' e '.join(details)} associados. Envie 'confirm=true' na query para excluí-la mesmo assim."
        )
    
    try:
        for analysis in analyses:
            db.query(AnalysisBackup).filter(AnalysisBackup.analysis_id == analysis.id).delete()
        
        db.query(HiveAnalysis).filter(HiveAnalysis.hive_id == hive_id).delete()
        db.query(Sensor).filter(Sensor.hive_id == hive_id).delete()
        
        db.delete(hive)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        print(f"Erro ao excluir colmeia: {e}")
        raise HTTPException(status_code=500, detail=f'Erro ao excluir colmeia: {str(e)}')