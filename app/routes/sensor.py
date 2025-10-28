from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.hive import Hive
from models.sensor_readings import Sensor
from schemas.sensor import SensorRead, SensorResponse

router = APIRouter(prefix='/sensors', tags=['Sensors'])

@router.post("/", response_model=SensorResponse)
def receive_data(sensor_data: SensorRead, db: Session = Depends(get_db)):
    hive = db.query(Hive).filter(Hive.id == sensor_data.hive_id).first() 

    if not hive: 
        raise HTTPException(status_code=404, detail=f"Colmeia com ID '{sensor_data.hive_id}' não encontrada")
    
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
        raise HTTPException(status_code=500, detail=f"Erro ao salvar os dados no banco: {str(e)}")

    return new_sensor_reading
