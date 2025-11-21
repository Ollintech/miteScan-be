from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.hive import Hive
from models.sensor_readings import Sensor
from schemas.sensor import SensorDataCreate, SensorResponse

router = APIRouter(prefix='/sensors', tags=['Sensors'])

@router.post("/", response_model=SensorResponse)
def receive_data(sensor_data: SensorDataCreate, db: Session = Depends(get_db)):
    hive = db.query(Hive).filter(
        Hive.account == sensor_data.account_name,
        Hive.name == sensor_data.hive_name
    ).first()

    if not hive: 
        raise HTTPException(status_code=404, detail=f"Colmeia '{sensor_data.hive_name}' não encontrada para a conta '{sensor_data.account_name}'")
    
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

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao salvar os dados no banco: {str(e)}")

    return new_sensor_reading

@router.get("/{hive_id}", response_model=List[SensorResponse])
def get_sensor_readings_for_hive(
    hive_id: int, 
    db: Session = Depends(get_db)
):
    hive = db.query(Hive).filter(Hive.id == hive_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail=f"Colmeia com ID '{hive_id}' não encontrada.")

    readings = db.query(Sensor)\
        .filter(Sensor.hive_id == hive_id)\
        .order_by(Sensor.created_at.desc())\
        .all()
    
    return readings
