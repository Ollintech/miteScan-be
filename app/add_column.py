from sqlalchemy import text
from db.database import engine

def add_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE hives ADD COLUMN image_path VARCHAR(255);"))
            conn.commit()
            print("Coluna 'image_path' adicionada com sucesso!")
        except Exception as e:
            print(f"Erro (talvez a coluna já exista): {e}")

if __name__ == "__main__":
    add_column()
