from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from API.app.models.sensor_readings import Sensor
from schemas.sensor import SensorRead, SensorResponse

router = APIRouter(prefix='/sensors', tags=['Sensors'])

@router.post("/", response_model=SensorResponse)
def receive_data(sensor_data: SensorRead, db: Session = Depends(get_db)):
    hive = db.query(Hive).order_by(Hive.id.desc()).first()

    if not hive: 
        raise HTTPException(status_code=404, detail="Colmeia não encontrada")
    
    new_sensor_reading = Sensor(
        hive_id=hive.id,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity
    )

    try:
        db.add(new_sensor_reading)
        db.commit()
        db.refresh(new_sensor_reading)

        hive.humidity = sensor_data.humidity
        hive.temperature = sensor_data.temperature

        db.commit()
        db.refresh(hive)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao salvar os dados no banco")

    return new_sensor_reading
