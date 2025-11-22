from fastapi import FastAPI, Depends
import uvicorn, os
from routes import user_root, hive, bee_type, analysis_backup, hive_analysis, access, user_associated, sensor, auth_routes
from db.database import Base, engine
from core.middleware import ActiveUserMiddleware
from mqtt_handler import run_mqtt_in_background
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
# from seed import seed_data

@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not os.getenv("TESTING"):
        await run_mqtt_in_background()
    yield
    print("Aplicação desligando...")

app = FastAPI(lifespan=lifespan)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://mitescan.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(ActiveUserMiddleware)

app.include_router(user_associated.router)
app.include_router(user_root.router)
app.include_router(hive.router)
app.include_router(access.router)
app.include_router(bee_type.router)
app.include_router(analysis_backup.router)
app.include_router(hive_analysis.router)
app.include_router(sensor.router)
app.include_router(auth_routes.router)

if __name__ == "__main__":
    # seed_data()
    import multiprocessing
    import sys
    if sys.platform.startswith("win"):
        import multiprocessing
        try:
            multiprocessing.set_start_method("spawn", force=True)
        except RuntimeError:
            pass
        
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
