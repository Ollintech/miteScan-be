from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.hive import Hive
from app.schemas.sensor import SensorRead

router = APIRouter()

@router.post("/sensor")
def receber_dados(sensor: SensorRead, db: Session = Depends(get_db)):
    colmeia = db.query(Hive).filter(Hive.id == sensor.colmeia_id).first()

    if not colmeia: 
        raise HTTPException(status_code = 404, detail = "Colmeia não encontrada")
    
    colmeia.temperature = sensor.temperature
    colmeia.humidity = sensor.humidity

    db.commit()

    return {"message": "Leitura recebida com sucesso"}