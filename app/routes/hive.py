from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from schemas.hive import HiveCreate, HiveResponse, HiveUpdate

router = APIRouter(prefix = '/hives', tags = ['hives'])

# Rota para a criação de colmeias
@router.post('/create', response_model = HiveResponse, status_code = status.HTTP_201_CREATED)
def create_hive(hive: HiveCreate, db: Session = Depends(get_db)):
    if db.query(Hive).filter(
        Hive.location_lat == hive.location_lat,
        Hive.location_lng == hive.location_lng
    ).first():
        raise HTTPException(status_code = 400, detail = 'Uma colmeia já foi cadastrada nessa localização.')
    
    new_hive = Hive(
        user_id = hive.user_id,
        bee_type_id = hive.bee_type_id,
        location_lat = hive.location_lat,
        location_lng = hive.location_lng,
        size = hive.size,
        humidity = hive.humidity,
        temperature = hive.temperature
    )

    db.add(new_hive)
    db.commit()
    db.refresh(new_hive)

    return new_hive

# Rota para obter os dados da colmeia
@router.get('/get:{hive_id}', response_model = HiveResponse)
def get_hive(hive_id: int, db: Session = Depends(get_db)):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()

    if not hive:
        raise HTTPException(status_code = 404, detail = 'Colmeia não encontrada.')

    return hive

# Rota para atualizar os dados da colmeia
@router.put('/put:{hive_id}', response_model = HiveResponse)
def update_hive(hive_id: int, hive_update: HiveUpdate , db: Session = Depends(get_db)):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()

    if not hive:
        raise HTTPException(status_code = 404, detail = 'Colmeia não encontrada.')

    if hive_update.user_id:
        Hive.user_id == hive_update.user_id

    if hive_update.bee_type_id:
        Hive.bee_type_id == hive_update.bee_type_id

    if hive_update.location_lat:
        Hive.location_lat == hive_update.location_lat

    if hive_update.location_lng:
        Hive.location_lng == hive_update.location_lng

    if hive_update.size:
        Hive.size == hive_update.size

    if hive_update.humidity:
        Hive.humidity == hive_update.humidity

    if hive_update.temperature:
        Hive.temperature == hive_update.temperature

    db.commit()

    db.refresh(hive)
    
    return hive

# Rota para deletar uma colmeia
@router.delete('/delete:{hive_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_hive(hive_id: int, db: Session = Depends(get_db)):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()

    if not hive:
        raise HTTPException(status_code = 404, detail = 'Colmeia não encontrada.')
    
    db.delete(hive)
    db.commit()

    return {'message': 'Colmeia deletada com sucesso!'}