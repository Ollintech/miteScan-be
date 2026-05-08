from sqlalchemy import text
from db.database import engine

def add_created_at_sensors():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE sensor_readings ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"))
            conn.commit()
            print("Coluna 'created_at' adicionada com sucesso na tabela 'sensor_readings'!")
        except Exception as e:
            print(f"Erro (talvez a coluna já exista): {e}")

if __name__ == "__main__":
    add_created_at_sensors()
