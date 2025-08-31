from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from models.sensor import Sensor
from schemas.hive import HiveCreate, HiveResponse, HiveUpdate
from core.auth import require_access

router = APIRouter(prefix='/hives', tags=['Hives'])

@router.post('/create', response_model=HiveResponse, status_code=status.HTTP_201_CREATED)
def create_hive(hive: HiveCreate, db: Session = Depends(get_db), user=Depends(require_access("owner", "manager"))):
    if db.query(Hive).filter(
        Hive.location_lat == hive.location_lat,
        Hive.location_lng == hive.location_lng
    ).first():
        raise HTTPException(status_code=400, detail='Uma colmeia já foi cadastrada nessa localização.')

    new_hive = Hive(
        user_id=hive.user_id,
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

@router.get('/all', response_model= list[HiveResponse])
def get_all_hives(db: Session = Depends(get_db), user=Depends(require_access("owner", "manager", "employee"))):
    hive = db.query(Hive).filter(Hive.user_id == user.id).all()

    if not hive:
        raise HTTPException(status_code=404, detail='Não existem colmeias cadastradas.')

    return hive

@router.get('/{hive_id}', response_model=HiveResponse)
def get_hive(hive_id: int, db: Session = Depends(get_db), user=Depends(require_access("owner", "manager", "employee"))):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()

    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')

    return hive

@router.put('/{hive_id}', response_model=HiveResponse)
def update_hive(hive_id: int, hive_update: HiveUpdate, db: Session = Depends(get_db), user=Depends(require_access("owner", "manager"))):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()

    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')

    if hive_update.user_id:
        hive.user_id = hive_update.user_id

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
def delete_hive(hive_id: int, db: Session = Depends(get_db), user=Depends(require_access("owner", "manager"))):

    hive = db.query(Hive).filter(Hive.id == hive_id).first()

    if not hive:
        raise HTTPException(status_code=404, detail='Colmeia não encontrada.')
    
    sensores = db.query(Sensor).filter(Sensor.hive_id == hive_id).all()

    if sensores and not confirm:
        return {
            "message": f"A colmeia {hive_id} possui {len(sensores)} leituras de sensores associados. Deseja excluí-la mesmo assim?",
            "require_confirmation": True
        }
    
    try:
        if confirm and sensores:
            for sensor in sensores:
                db.delete(sensor)
            
        db.delete(hive)
        db.commit()
        
        return {'message': f'Colmeia {hive_id} e as leituras de sensores associadas foram excluídas com sucesso!'}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f'Erro ao excluir colmeia: {str(e)}')
