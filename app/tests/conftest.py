import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.database import Base, get_db
from fastapi.testclient import TestClient
from main import app
import os

os.environ["TESTING"] = "1"

# Banco em memória: super rápido, não cria arquivos no disco
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Engine especial para SQLite em memória (StaticPool é obrigatório para manter conexão viva)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Session para testes
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas UMA VEZ no início dos testes
Base.metadata.create_all(bind=engine)

# Fixture para a sessão de banco
@pytest.fixture(scope="function")
def db():
    """Cria uma sessão de banco para cada teste, isolada, com rollback."""
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# Fixture para o client de testes
@pytest.fixture(scope="function")
def client(db):
    """Cria um client que usa a sessão de teste."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
