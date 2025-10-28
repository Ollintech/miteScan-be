from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from models.sensor_readings import Sensor
from models.user_root import UserRoot
from models.users_associated import UserAssociated
from schemas.hive import HiveCreate, HiveResponse, HiveUpdate
from typing import List, Optional
from core.auth import (
    get_current_user_root,
    get_current_user_root_optional,
    get_current_user_associated_optional
)

router = APIRouter(prefix='/{user_root_id}/hives', tags=['Hives'])

def get_viewer_access(
    user_root_id: int,
    current_user_root: UserRoot = Depends(get_current_user_root_optional),
    current_user_associated: UserAssociated = Depends(get_current_user_associated_optional)
):
    """Verifica se o usuário logado é o Root dono ou um Associado dele."""
    
    if current_user_root and current_user_root.id == user_root_id:
        return current_user_root 

    if current_user_associated and current_user_associated.user_root_id == user_root_id:
        return current_user_associated 

    if not current_user_root and not current_user_associated:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado para este recurso")


def check_root_permission(user_root_id: int, current_user_root: UserRoot):
    """Verifica se o root logado é o mesmo da URL (para CUD)."""
    if not current_user_root:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado como usuário root")
    if current_user_root.id != user_root_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação não permitida")
    

@router.post('/create', response_model=HiveResponse, status_code=status.HTTP_201_CREATED)
def create_hive(
    user_root_id: int,
    hive: HiveCreate, 
    db: Session = Depends(get_db), 
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    check_root_permission(user_root_id, current_user_root) 

    if db.query(Hive).filter(
        Hive.location_lat == hive.location_lat,
        Hive.location_lng == hive.location_lng
    ).first():
        raise HTTPException(status_code=400, detail='Uma colmeia já foi cadastrada nessa localização.')

    new_hive = Hive(
        user_root_id = user_root_id, 
        bee_type_id=hive.bee_type_id,
        location_lat=hive.location_lat,
        location_lng=hive.location_lng,
        size=hive.size,
        humidity=hive.humidity,
        temperature=hive.temperature
    )

    db.add(new_hive)
    db.commit()
    db.refresh(new_hive)

    return new_hive


@router.get('/all', response_model=List[HiveResponse])
def get_all_hives(
    user_root_id: int,
    db: Session = Depends(get_db), 
    user_principal = Depends(get_viewer_access)
):
    hives = db.query(Hive).filter(Hive.user_root_id == user_root_id).all()

    if not hives:
        raise HTTPException(status_code=404, detail='Não existem colmeias cadastradas para este usuário.')

    return hives


@router.get('/{hive_id}', response_model=HiveResponse)
def get_hive(
    user_root_id: int,
    hive_id: int, 
    db: Session = Depends(get_db), 
    user_principal = Depends(get_viewer_access)
):
    hive = db.query(Hive).filter(
        Hive.id == hive_id,
        Hive.user_root_id == user_root_id
    ).first()

    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')

    return hive


@router.put('/{hive_id}', response_model=HiveResponse)
def update_hive(
    user_root_id: int,
    hive_id: int, 
    hive_update: HiveUpdate, 
    db: Session = Depends(get_db), 
    current_user_root: UserRoot = Depends(get_current_user_root)
):
    check_root_permission(user_root_id, current_user_root) 

    hive = db.query(Hive).filter(
        Hive.id == hive_id,
        Hive.user_root_id == user_root_id
    ).first()

    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')

    if hive_update.bee_type_id:
        hive.bee_type_id = hive_update.bee_type_id
    if hive_update.location_lat:
        hive.location_lat = hive_update.location_lat
    if hive_update.location_lng:
        hive.location_lng = hive_update.location_lng
    if hive_update.size:
        hive.size = hive_update.size
    if hive_update.humidity:
        hive.humidity = hive_update.humidity
    if hive_update.temperature:
        hive.temperature = hive_update.temperature

    db.commit()
    db.refresh(hive)

    return hive


@router.delete('/{hive_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_hive(
    user_root_id: int,
    hive_id: int, 
    db: Session = Depends(get_db), 
    current_user_root: UserRoot = Depends(get_current_user_root), 
    confirm: Optional[bool] = Query(False) 
):
    check_root_permission(user_root_id, current_user_root) 

    hive = db.query(Hive).filter(
        Hive.id == hive_id,
        Hive.user_root_id == user_root_id
    ).first()

    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')
    
    sensores = db.query(Sensor).filter(Sensor.hive_id == hive_id).all()

    if sensores and not confirm:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A colmeia {hive_id} possui {len(sensores)} leituras de sensores associados. Envie 'confirm=true' na query para excluí-la mesmo assim."
        )
    
    try:
        if sensores:
            for sensor in sensores:
                db.delete(sensor)
            
        db.delete(hive)
        db.commit()
        
        return None
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Erro ao excluir colmeia: {str(e)}')