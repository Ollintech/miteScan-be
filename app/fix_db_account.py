from sqlalchemy import text
from db.database import engine

def fix_database():
    with engine.connect() as conn:
        try:
            print("Tentando adicionar coluna 'account' em 'users_associated'...")
            # Usando text().execution_options(autocommit=True) para garantir a execucao
            conn.execute(text("ALTER TABLE users_associated ADD COLUMN IF NOT EXISTS account VARCHAR(50);"))
            conn.commit()
            print("Sucesso: Coluna 'account' adicionada ou ja existente!")
        except Exception as e:
            print(f"Erro ao atualizar tabela users_associated: {e}")

if __name__ == "__main__":
    fix_database()
