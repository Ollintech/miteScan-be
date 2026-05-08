from sqlalchemy import text
from db.database import engine

def add_bee_status_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE hive_analyses ADD COLUMN bee_status VARCHAR(50);"))
            conn.commit()
            print("Coluna 'bee_status' adicionada com sucesso na tabela 'hive_analyses'!")
        except Exception as e:
            print(f"Erro (talvez a coluna já exista): {e}")

if __name__ == "__main__":
    add_bee_status_column()
