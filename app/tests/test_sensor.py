import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.hive import Hive
from models.sensor_readings import Sensor
from models.user_root import UserRoot
from models.bee_type import BeeType
from models.access import Access

# Fixture para criar uma colmeia no banco de dados de teste
@pytest.fixture
def create_hive(db: Session):
    # Garante que as dependências existam
    access = db.query(Access).first() or Access(name="owner")
    user = db.query(UserRoot).first() or UserRoot(name="Test Root", email="root@test.com", password_hash="123", access=access)
    bee_type = db.query(BeeType).first() or BeeType(name="Test Bee")
    db.add_all([access, user, bee_type])
    db.commit()

    hive = Hive(
        user_root_id=user.id,
        bee_type_id=bee_type.id,
        location_lat=12.34,
        location_lng=56.78,
        size="Média"
    )
    db.add(hive)
    db.commit()
    db.refresh(hive)
    return hive

def test_receber_dados_sensor(client: TestClient, db: Session, create_hive: Hive):
    # Limpa leituras anteriores para este teste
    db.query(Sensor).delete()
    db.commit()

    # A rota de sensor espera um `colmeia_id` no corpo, não `hive_id`
    # Vamos assumir que o endpoint é /sensor/ e o schema espera `colmeia_id`
    # Se o schema mudou para `hive_id`, o payload deve ser ajustado.
    # Baseado no seu .env.example, a URL é http://localhost:8000/sensor
    # Vamos assumir que o endpoint está registrado no app principal com o prefixo /sensor
    # O teste original usa "colmeia_id", vamos manter isso.

    sensor_data = {
        "colmeia_id": create_hive.id,
        "temperature": 25.5,
        "humidity": 60.0
    }

    response = client.post("/sensor/", json=sensor_data)

    assert response.status_code == 200

    data = response.json()
    assert data["hive_id"] == sensor_data["colmeia_id"] # O response model usa hive_id
    assert data["temperature"] == sensor_data["temperature"]
    assert data["humidity"] == sensor_data["humidity"]
    assert "id" in data  # Verifica se o id foi gerado

    # Verifica se a leitura foi salva no banco
    sensor_db = db.query(Sensor).filter(Sensor.id == data["id"]).first()
    assert sensor_db is not None
    assert sensor_db.temperature == sensor_data["temperature"]
    assert sensor_db.humidity == sensor_data["humidity"]

def test_colmeia_nao_encontrada(client: TestClient):
    sensor_data = {
        "colmeia_id": 999,
        "temperature": 25.5,
        "humidity": 60.0
    }

    response = client.post("/sensor/", json=sensor_data)

    assert response.status_code == 404
    assert response.json() == {"detail": "Colmeia não encontrada"}
