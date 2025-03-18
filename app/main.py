from fastapi import FastAPI
from routes import user, hive

app = FastAPI()

app.include_router(user.router, prefix = '/users', tags = ['Users'])
app.include_router(hive.router, prefix = '/hives', tags = ['Hives'])