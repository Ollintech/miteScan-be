from fastapi import FastAPI
from routes import user, hive

app = FastAPI()

app.include_router(user.router, prefix = '/users', tags = ['Users'])
app.include_router(hive.router, prefix = '/hives', tags = ['Hives'])
app.include_router(role.router, prefix = '/roles', tags = ['Roles'])
app.include_router(bee_type.router, prefix = '/bee_types', tags = ['BeeTypes'])
app.include_router(analysis_backup.router, prefix = '/analysis_backups', tags = ['AnalysisBackups'])
app.include_router(hive_analyse.router, prefix = '/hive_analyses', tags = ['HiveAnalyses'])