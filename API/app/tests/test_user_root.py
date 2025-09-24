import pytest
from API.app.models.user_root import User
from models.access import Access
from API.app.models.users_associated import Company
from core.auth import get_password_hash
from tests.mock_data import mock_user, mock_user_response, mock_user_with_hash, mock_access_response, mock_company_response


def test_register_user_success(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user_with_hash()

    response = client.post("/users/register", json={**user_data, "access_id": access_id, "company_id": company_id})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data


def test_register_user_email_duplicado(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user()
    password = "securePass123"
    user_data["password_hash"] = get_password_hash(password)

    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password_hash=user_data["password_hash"],
        access_id=access_id,
        company_id=company_id,
        status=False
    )
    db.add(user)
    db.commit()

    response = client.post("/users/register", json={**user_data, "access_id": access_id, "company_id": company_id})

    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado."


def test_login_success(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user()
    password = "securePass123"  
    user_data["password_hash"] = get_password_hash(password) 

    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password_hash=user_data["password_hash"],  
        access_id=access_id,
        company_id=company_id,
        status=True
    )
    db.add(user)
    db.commit()

    response = client.post("/users/login", data={
        "username": user_data["email"],
        "password": password  
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == user_data["email"]


def test_login_invalid_credentials(client, db):
    response = client.post("/users/login", data={
        "username": "naoexiste@email.com",
        "password": "senhaerrada"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


def test_create_user_success(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user_response()
    password = "securePass123"  
    user_data["password_hash"] = get_password_hash(password) 

    response = client.post("/users/create", json={**user_data, "access_id": access_id, "company_id": company_id})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["status"] is False
    assert "id" in data


def test_create_user_email_duplicado(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user_response()
    password = "securePass123"  
    user_data["password_hash"] = get_password_hash(password) 

    user = User(
        name="Usuário Existente",
        email=user_data["email"],
        password_hash=user_data["password_hash"],  
        status=False,
        access_id=access_id,
        company_id=company_id
    )
    db.add(user)
    db.commit()

    response = client.post("/users/create", json={**user_data, "access_id": access_id, "company_id": company_id})

    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado."


def test_get_user_success(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user_response()
    password = "securePass123"  
    user_data["password_hash"] = get_password_hash(password) 

    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password_hash=user_data["password_hash"],  
        status=True,
        access_id=access_id,
        company_id=company_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]
    assert response.json()["email"] == user_data["email"]


def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."


def test_update_user_success(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user_response()
    password = "securePass123"  
    user_data["password_hash"] = get_password_hash(password) 

    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password_hash=user_data["password_hash"],  
        status=False,
        access_id=access_id,
        company_id=company_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.put(f"/users/{user.id}", json={
        "name": "Carlos Atualizado",
        "status": True
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Carlos Atualizado"
    assert response.json()["status"] is True


def test_update_user_email_duplicado(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user1 = User(
        name="User1", email="email1@test.com",
        password_hash=get_password_hash("senha1"),
        status=False, access_id=access_id, company_id=company_id)
    user2 = User(
        name="User2", email="email2@test.com",
        password_hash=get_password_hash("senha2"),
        status=False, access_id=access_id, company_id=company_id)
    db.add_all([user1, user2])
    db.commit()

    response = client.put(f"/users/{user2.id}", json={"email": "email1@test.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado."


def test_delete_user_success(client, db):
    access_id = mock_access_response
    company_id = mock_company_response
    user_data = mock_user_response()
    password = "securePass123"  
    user_data["password_hash"] = get_password_hash(password) 

    user = User(
        name=user_data["name"],
        email=user_data["email"],
        password_hash=user_data["password_hash"],  
        status=False,
        access_id=access_id,
        company_id=company_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 204
    assert db.query(User).filter(User.id == user.id).first() is None


def test_delete_user_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado."
