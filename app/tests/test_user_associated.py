import pytest
from sqlalchemy.orm import Session
from models.user_root import UserRoot
from models.user_associated import UserAssociated
from models.access import Access
from core.auth import get_password_hash, create_access_token

@pytest.fixture(scope="function")
def setup_data(db: Session):
    """Cria um usuário root e um nível de acesso para os testes."""
    # Limpa dados de testes anteriores para evitar conflitos
    db.query(UserAssociated).delete()
    db.query(UserRoot).delete()
    db.query(Access).delete()
    db.commit()

    # Cria Nível de Acesso
    access_employee = Access(name="employee", description="Funcionário")
    access_root = Access(name="owner", description="Dono")
    db.add_all([access_employee, access_root])
    db.commit()

    # Cria Usuário Root
    user_root = UserRoot(
        name="Dono Teste",
        email="dono@teste.com",
        account="dono_teste",
        password_hash=get_password_hash("senha123"),
        access_id=access_root.id,
        status=True
    )
    db.add(user_root)
    db.commit()
    db.refresh(user_root)

    # Cria Token para o Root
    token = create_access_token({"sub": user_root.email, "account": user_root.account, "type": "root"})
    headers = {"Authorization": f"Bearer {token}"}

    return user_root, access_employee, headers

def test_create_user_associated_success(client, db: Session, setup_data):
    user_root, access_employee, headers = setup_data

    user_associated_data = {
        "name": "Funcionário Teste",
        "email": "func@teste.com",
        "password": "outrasenha",
        "access_id": access_employee.id,
        "account": user_root.account
    }

    response = client.post(f"/{user_root.account}/users_associated/register", json=user_associated_data, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_associated_data["name"]
    assert data["email"] == user_associated_data["email"]
    assert data["account"] == user_root.account
    assert "id" in data

def test_create_user_associated_duplicate_email(client, db: Session, setup_data):
    user_root, access_employee, headers = setup_data

    # Cria um usuário associado primeiro
    existing_user = UserAssociated(
        name="Usuário Existente",
        email="existente@teste.com",
        password_hash=get_password_hash("senha"),
        access_id=access_employee.id,
        account=user_root.account
    )
    db.add(existing_user)
    db.commit()

    # Tenta criar outro com o mesmo email
    user_associated_data = {
        "name": "Outro Funcionário",
        "email": "existente@teste.com",
        "password": "outrasenha",
        "access_id": access_employee.id,
        "account": user_root.account
    }

    response = client.post(f"/{user_root.account}/users_associated/register", json=user_associated_data, headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email já cadastrado."

def test_get_user_associated_success(client, db: Session, setup_data):
    user_root, access_employee, headers = setup_data

    user_associated = UserAssociated(
        name="Funcionário para Buscar",
        email="buscar@teste.com",
        password_hash=get_password_hash("senha"),
        access_id=access_employee.id,
        account=user_root.account
    )
    db.add(user_associated)
    db.commit()
    db.refresh(user_associated)

    # A rota para listar todos os usuários associados de uma conta
    response = client.get(f"/{user_root.account}/users_associated/", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["email"] == "buscar@teste.com"

def test_delete_user_associated_success(client, db: Session, setup_data):
    user_root, access_employee, headers = setup_data

    user_to_delete = UserAssociated(
        name="Funcionário para Deletar",
        email="deletar@teste.com",
        password_hash=get_password_hash("senha"),
        access_id=access_employee.id,
        account=user_root.account
    )
    db.add(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)

    # Rota de deleção
    response = client.delete(f"/{user_root.account}/users_associated/{user_to_delete.id}", headers=headers)
    assert response.status_code == 204
