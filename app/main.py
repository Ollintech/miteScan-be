from fastapi import FastAPI
import uvicorn
from routes import user, hive, role, bee_type, analysis_backup, hive_analysis

app = FastAPI()

app.include_router(user.router)
app.include_router(hive.router)
app.include_router(role.router)
app.include_router(bee_type.router)
# app.include_router(analysis_backup.router)
app.include_router(hive_analysis.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)