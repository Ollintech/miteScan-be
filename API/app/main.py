from fastapi import FastAPI, Depends
import uvicorn
from routes import user, hive, bee_type, analysis_backup, hive_analysis, access, company, sensor
from db.database import Base, engine, get_db
from core.middleware import ActiveUserMiddleware
from seed import seed_data
import asyncio
from mqtt_handler import run_mqtt_in_background
from routes.sensor import receber_dados
from sqlalchemy.orm import Session
from schemas.sensor import SensorRead
import os
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # seed_data()
    if not os.getenv("TESTING"): 
        await run_mqtt_in_background()
    yield
    print("Aplicação desligando...")
    
app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

app.add_middleware(ActiveUserMiddleware)

app.include_router(company.router)
app.include_router(user.router)
app.include_router(hive.router)
app.include_router(access.router)
app.include_router(bee_type.router)
app.include_router(analysis_backup.router)
app.include_router(hive_analysis.router)
app.include_router(sensor.router)

@app.post("/sensor")
async def receive_sensor_data(data: dict, db: Session = Depends(get_db)):
    print("Sensor:", data)

    try:
        sensor_data = SensorRead(**data)
        receber_dados(sensor_data, db)
        print(f"Dados recebidos e processados.")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
    
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
