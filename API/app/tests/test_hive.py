from models.user import User
from models.access import Access
from models.bee_type import BeeType
from models.hive import Hive
from core.auth import create_access_token, get_password_hash  # Certifique-se de que está usando sua função JWT correta
from sqlalchemy.orm import Session


def create_user_and_bee_type(client, db: Session):
    # Criar acesso se não existir
    access = db.query(Access).filter_by(name="manager").first()
    if not access:
        access = Access(name="manager", description="Gerente do sistema")
        db.add(access)
        db.commit()
        db.refresh(access)

    # Criar usuário
    user = User(
        name="Usuário Teste",
        email="teste@teste.com",
        password_hash="hashed-password",
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
    token = create_access_token({"sub": user.email, "id": user.id})
    headers = {"Authorization": f"Bearer {token}"}

    return user, bee_type.id, headers


def test_create_hive_success(client, db):
    user, bee_type_id, headers = create_user_and_bee_type(client, db)

    # Criação de uma nova colmeia
    payload = {
        "user_id": user.id,  # Verifique se o ID do usuário está correto
        "bee_type_id": bee_type_id,  # Verifique se o ID da abelha está correto
        "location_lat": -23.5505,  # Coordenadas válidas
        "location_lng": -46.6333,
        "size": "Média",
        "humidity": 60.0,
        "temperature": 30.0
    }

    response = client.post("/hives/create", json=payload, headers=headers)  # Ajustado para /hives/create

    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())

    assert response.status_code == 201  # Se esperar 201 como sucesso
    assert response.json()["message"] == f"Colmeia criada com sucesso pelo usuário {user.name} com o acesso {user.access.name}"


def test_create_hive_duplicate_location(client, db):
    user, bee_type_id, headers = create_user_and_bee_type(client, db)

    # Cria uma colmeia inicial com uma localização específica
    hive = Hive(
        user_id=user.id,
        bee_type_id=bee_type_id,
        location_lat=-10.0,
        location_lng=10.0,
        size="Grande",
        humidity=60.0,
        temperature=25.0
    )
    db.add(hive)
    db.commit()

    # Tenta criar uma colmeia com a mesma localização
    response = client.post("/hives/create", json={
        "user_id": user.id,
        "bee_type_id": bee_type_id,
        "location_lat": -10.0,
        "location_lng": 10.0,
        "size": "Pequena",
        "humidity": 50.0,
        "temperature": 28.0
    }, headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Uma colmeia já foi cadastrada nessa localização."


def test_get_hive_success(client, db):
    user, bee_type_id, headers = create_user_and_bee_type(client, db)

    # Criação de uma colmeia para teste
    hive = Hive(
        user_id=user.id,
        bee_type_id=bee_type_id,
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
    response = client.get(f"/hives/{hive.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["size"] == "Média"
    assert response.json()["location_lat"] == 1.1


def test_get_hive_not_found(client, db):
    user, _, headers = create_user_and_bee_type(client, db)

    # Tenta obter uma colmeia inexistente
    response = client.get("/hives/9999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Colmeia não encontrada."


def test_update_hive_success(client, db):
    user, bee_type_id, headers = create_user_and_bee_type(client, db)

    # Criação de uma colmeia para teste
    hive = Hive(
        user_id=user.id,
        bee_type_id=bee_type_id,
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
    response = client.put(f"/hives/{hive.id}", json={
        "size": "Grande",
        "humidity": 55.5,
        "temperature": 28.0
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["size"] == "Grande"
    assert response.json()["humidity"] == 55.5
    assert response.json()["temperature"] == 28.0


def test_update_hive_not_found(client, db):
    user, _, headers = create_user_and_bee_type(client, db)

    # Tenta atualizar uma colmeia inexistente
    response = client.put("/hives/9999", json={"size": "Grande"}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Colmeia não encontrada."


def test_delete_hive_success(client, db):
    user, bee_type_id, headers = create_user_and_bee_type(client, db)

    # Criação de uma colmeia para teste
    hive = Hive(
        user_id=user.id,
        bee_type_id=bee_type_id,
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
    response = client.delete(f"/hives/{hive.id}", headers=headers)
    assert response.status_code == 204
    assert db.query(Hive).filter(Hive.id == hive.id).first() is None


def test_delete_hive_not_found(client, db):
    user, _, headers = create_user_and_bee_type(client, db)

    # Tenta excluir uma colmeia inexistente
    response = client.delete("/hives/9999", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Colmeia não encontrada."
