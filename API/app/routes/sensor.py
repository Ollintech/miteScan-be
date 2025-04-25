from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from models.sensor import Sensor
from schemas.sensor import SensorRead, SensorResponse

router = APIRouter(prefix='/sensor', tags=['Sensor'])

@router.post("/", response_model=SensorResponse)
def receber_dados(sensor: SensorRead, db: Session = Depends(get_db)):
    colmeia = db.query(Hive).filter(Hive.id == sensor.colmeia_id).first()

    if not colmeia: 
        raise HTTPException(status_code=404, detail="Colmeia não encontrada")
    
    new_sensor_reading = Sensor(
        colmeia_id=sensor.colmeia_id,
        temperature=sensor.temperature,
        humidity=sensor.humidity
    )

    try:
        db.add(new_sensor_reading)
        db.commit()
        db.refresh(new_sensor_reading)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao salvar os dados no banco")

    return new_sensor_reading
