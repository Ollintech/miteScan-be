from models.user_root import UserRoot
from models.access import Access
from models.bee_type import BeeType
from models.hive import Hive
from core.auth import create_access_token
from sqlalchemy.orm import Session
import pytest

def create_user_and_bee_type(client, db: Session):
    # Criar acesso se não existir
    access = db.query(Access).filter_by(name="manager").first()
    if not access:
        access = Access(name="manager", description="Gerente do sistema")
        db.add(access)
        db.commit()
        db.refresh(access)

    # Criar usuário
    user = UserRoot(
        name="Usuário Teste",
        email="teste@teste.com",
        password_hash="hashed-password", # Em um cenário real, use get_password_hash
        status=True, 
        access_id=access.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Criar tipo de abelha
    bee_type = BeeType(name="Abelha Africana")
    db.add(bee_type)
    db.commit()
    db.refresh(bee_type)

    # Criar token JWT
    token = create_access_token({"sub": user.email, "id": user.id, "type": "root"})
    headers = {"Authorization": f"Bearer {token}"}

    return user, bee_type, headers


def test_create_hive_success(client, db):
    user, bee_type, headers = create_user_and_bee_type(client, db)

    # Criação de uma nova colmeia
    payload = {
        "bee_type_id": bee_type.id,
        "location_lat": -23.5505,  # Coordenadas válidas
        "location_lng": -46.6333,
        "size": "Média",
    }

    # A rota agora é aninhada sob o ID do usuário root
    response = client.post(f"/{user.id}/hives/create", json=payload, headers=headers)

    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())

    assert response.status_code == 201
    data = response.json()
    assert data["location_lat"] == payload["location_lat"]
    assert data["user_root_id"] == user.id


def test_create_hive_duplicate_location(client, db):
    user, bee_type, headers = create_user_and_bee_type(client, db)

    # Cria uma colmeia inicial com uma localização específica
    hive = Hive(
        user_root_id=user.id,
        bee_type_id=bee_type.id,
        location_lat=-10.0,
        location_lng=10.0,
        size="Grande",
        humidity=60.0,
        temperature=25.0
    )
    db.add(hive)
    db.commit()

    # Tenta criar outra colmeia com a mesma localização
    payload = {
        "bee_type_id": bee_type.id,
        "location_lat": -10.0,
        "location_lng": 10.0,
        "size": "Pequena",
    }
    response = client.post(f"/{user.id}/hives/create", json=payload, headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Uma colmeia já foi cadastrada nessa localização."


def test_get_hive_success(client, db):
    user, bee_type, headers = create_user_and_bee_type(client, db)

    # Criação de uma colmeia para teste
    hive = Hive(
        user_root_id=user.id, 
        bee_type_id=bee_type.id,
        location_lat=1.1,
        location_lng=2.2,
        size="Média",
        humidity=65.0,
        temperature=32.0
    )
    db.add(hive)
    db.commit()
    db.refresh(hive)

    # Requisição para obter a colmeia
    response = client.get(f"/{user.id}/hives/{hive.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["size"] == "Média"
    assert response.json()["location_lat"] == 1.1


def test_get_hive_not_found(client, db):
    user, _, headers = create_user_and_bee_type(client, db)

    # Tenta obter uma colmeia inexistente
    response = client.get(f"/{user.id}/hives/9999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Colmeia não encontrada."


def test_update_hive_success(client, db):
    user, bee_type, headers = create_user_and_bee_type(client, db)

    # Criação de uma colmeia para teste
    hive = Hive(
        user_root_id=user.id,
        bee_type_id=bee_type.id,
        location_lat=3.3,
        location_lng=4.4,
        size="Pequena",
        humidity=50.0,
        temperature=26.0
    )
    db.add(hive)
    db.commit()
    db.refresh(hive)

    # Atualização da colmeia
    response = client.put(f"/{user.id}/hives/{hive.id}", json={
        "size": "Grande",
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["size"] == "Grande"


def test_update_hive_not_found(client, db):
    user, _, headers = create_user_and_bee_type(client, db)

    # Tenta atualizar uma colmeia inexistente
    response = client.put(f"/{user.id}/hives/9999", json={"size": "Grande"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Colmeia não encontrada."


def test_delete_hive_success(client, db):
    user, bee_type, headers = create_user_and_bee_type(client, db)

    # Criação de uma colmeia para teste
    hive = Hive(
        user_root_id=user.id,
        bee_type_id=bee_type.id,
        location_lat=5.5,
        location_lng=6.6,
        size="Média",
        humidity=60.0,
        temperature=30.0
    )
    db.add(hive)
    db.commit()
    db.refresh(hive)

    # Exclusão da colmeia
    response = client.delete(f"/{user.id}/hives/{hive.id}", headers=headers)
    assert response.status_code == 204
    assert db.query(Hive).filter(Hive.id == hive.id).first() is None


def test_delete_hive_not_found(client, db):
    user, _, headers = create_user_and_bee_type(client, db)

    # Tenta excluir uma colmeia inexistente
    response = client.delete(f"/{user.id}/hives/9999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Colmeia não encontrada."
