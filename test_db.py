from app.db.database import get_engine

engine = get_engine()

try:
    with engine.connect() as connection:
        print("✅ Conectado ao banco de dados com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar ao banco: {e}")
