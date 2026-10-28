import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.push_subscription import PushSubscription
from core.config import settings

def test_get_vapid_public_key(client: TestClient):
    response = client.get("/notifications/vapid-public-key")
    assert response.status_code == 200
    data = response.json()
    assert "public_key" in data
    assert len(data["public_key"]) > 20

def test_get_alert_thresholds(client: TestClient):
    response = client.get("/notifications/thresholds")
    assert response.status_code == 200
    data = response.json()
    assert "temp_min" in data
    assert "temp_max" in data
    assert "humidity_min" in data
    assert "humidity_max" in data
    assert data["temp_min"] == settings.temp_min_alert
    assert data["temp_max"] == settings.temp_max_alert

def test_subscribe_and_unsubscribe(client: TestClient, db: Session):
    endpoint = "https://fcm.googleapis.com/fcm/send/test-endpoint-desktop-123"
    
    # Limpa caso já exista
    db.query(PushSubscription).filter(PushSubscription.endpoint == endpoint).delete()
    db.commit()

    sub_payload = {
        "endpoint": endpoint,
        "keys": {
            "p256dh": "BNcRdreALRFXTkOOUHK1EtK2wtaz5Ry4YfYCA_0QT9t0A37",
            "auth": "tBHItJI5svbpez7KI4CCXg"
        },
        "account": "teste_conta",
        "user_email": "usuario@teste.com"
    }

    # 1. Registra inscrição
    response = client.post("/notifications/subscribe", json=sub_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["endpoint"] == endpoint
    assert data["account"] == "teste_conta"

    # Verifica no banco
    db_sub = db.query(PushSubscription).filter(PushSubscription.endpoint == endpoint).first()
    assert db_sub is not None
    assert db_sub.auth == "tBHItJI5svbpez7KI4CCXg"

    # 2. Reenvia para testar idempotência/atualização
    sub_payload["keys"]["auth"] = "novo_auth_secret"
    response_update = client.post("/notifications/subscribe", json=sub_payload)
    assert response_update.status_code == 200
    db_sub_updated = db.query(PushSubscription).filter(PushSubscription.endpoint == endpoint).first()
    assert db_sub_updated.auth == "novo_auth_secret"

    # 3. Remove inscrição
    unsub_response = client.post("/notifications/unsubscribe", json={"endpoint": endpoint})
    assert unsub_response.status_code == 200
    assert db.query(PushSubscription).filter(PushSubscription.endpoint == endpoint).first() is None
