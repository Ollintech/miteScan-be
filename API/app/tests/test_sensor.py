import pytest
from fastapi.testclient import TestClient
from models.hive import Hive
from models.sensor import Sensor

# Fixture para criar uma colmeia no banco de dados de teste
@pytest.fixture
def create_hive(db):
    hive = Hive(
        id=1,
        user_id=1,
        bee_type_id=1,
        location_lat=12.34,
        location_lng=56.78,
        size=10
    )
    db.add(hive)
    db.commit()
    return hive

def test_receber_dados_sensor(client: TestClient, db, create_hive: Hive):
    sensor_data = {
        "colmeia_id": create_hive.id,
        "temperature": 25.5,
        "humidity": 60.0
    }

    response = client.post("/sensor/", json=sensor_data)

    assert response.status_code == 200
    data = response.json()
    assert data["colmeia_id"] == sensor_data["colmeia_id"]
    assert data["temperature"] == sensor_data["temperature"]
    assert data["humidity"] == sensor_data["humidity"]
    assert "id" in data  # Verifica se o id foi gerado
    assert "created_at" not in data  # Verifica que o campo created_at não está presente

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
