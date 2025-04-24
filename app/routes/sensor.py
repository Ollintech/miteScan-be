from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from schemas.sensor import SensorRead

router = APIRouter(prefix='/sensor', tags=['Sensor'])

#Essa rota atualiza os dados de temperatura e umidade da colmeia
@router.post("/")
def receber_dados(sensor: SensorRead, db: Session = Depends(get_db)):
    colmeia = db.query(Hive).filter(Hive.id == sensor.colmeia_id).first()

    if not colmeia: 
        raise HTTPException(status_code = 404, detail = "Colmeia não encontrada")
    
    colmeia.humidity = sensor.humidity
    colmeia.temperature = sensor.temperature

    try:
        db.commit()
        db.refresh(colmeia)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao salvar os dados no banco")

    return {"message": "Leitura recebida com sucesso"}