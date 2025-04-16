from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from schemas.sensor import SensorRead

router = APIRouter(prefix='/sensor', tags=['Sensor'])

#Essa rota atualiza os dados de temperatura e umidade da colmeia
@router.post("/")
def receber_dados(sensor: SensorRead, db: Session = Depends(get_db)):
    print(sensor)
    colmeia = db.query(Hive).filter(Hive.id == sensor.colmeia_id).first()

    if not colmeia: 
        raise HTTPException(status_code = 404, detail = "Colmeia não encontrada")
    
    colmeia.temperature = sensor.temperature
    colmeia.humidity = sensor.humidity

    db.commit()

    return {"message": "Leitura recebida com sucesso"}