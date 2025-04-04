# importando o framework para a criação da API em Python
from fastapi import FastAPI 
# importando o servidor web
import uvicorn
# importando as rotas 
from routes import access
from routes import user, hive, bee_type, analysis_backup, hive_analysis
# importando
from db.database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(hive.router)
app.include_router(access.router)
app.include_router(bee_type.router)
app.include_router(analysis_backup.router)
app.include_router(hive_analysis.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)