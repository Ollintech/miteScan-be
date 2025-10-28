from API.app.models.user_root import User
from models.bee_type import BeeType

def create_user(db):
    user = User(
        name="Responsável",
        email="responsavel@teste.com",
        password_hash="hashqualquer",
        status=True,
        access_id=1,
        company_id=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user.id

def test_create_bee_type_success(client, db):
    user_root_id = create_user(db)

    response = client.post("/bee_types/create", json={
        "name": "Apis Mellifera",
        "description": "Abelha europeia comum",
        "user_root_id": user_root_id
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Apis Mellifera"
    assert data["description"] == "Abelha europeia comum"
    assert data["user_root_id"] == user_root_id
    assert "id" in data

def test_create_bee_type_name_duplicado(client, db):
    user_root_id = create_user(db)

    bee_type = BeeType(name="Jataí", description="Abelha sem ferrão", user_root_id=user_root_id)
    db.add(bee_type)
    db.commit()

    response = client.post("/bee_types/create", json={
        "name": "Jataí",
        "description": "Outra descrição",
        "user_root_id": user_root_id
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Abelha já cadastrada."

def test_get_bee_type_success(client, db):
    user_root_id = create_user(db)

    bee_type = BeeType(name="Mandaguari", description="Abelha nativa", user_root_id=user_root_id)
    db.add(bee_type)
    db.commit()
    db.refresh(bee_type)

    response = client.get(f"/bee_types/{bee_type.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Mandaguari"

def test_get_bee_type_not_found(client):
    response = client.get("/bee_types/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Abelha não encontrada."

def test_update_bee_type_success(client, db):
    user_root_id = create_user(db)

    bee_type = BeeType(name="Abelha Antiga", description="Descrição", user_root_id=user_root_id)
    db.add(bee_type)
    db.commit()
    db.refresh(bee_type)

    response = client.put(f"/bee_types/{bee_type.id}", json={
        "name": "Nova Abelha",
        "description": "Nova descrição"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Nova Abelha"
    assert response.json()["description"] == "Nova descrição"

def test_update_bee_type_not_found(client):
    response = client.put("/bee_types/9999", json={
        "name": "Qualquer coisa"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Abelha não encontrada."

def test_delete_bee_type_success(client, db):
    user_root_id = create_user(db)

    bee_type = BeeType(name="Para Deletar", description="Descrição qualquer", user_root_id=user_root_id)
    db.add(bee_type)
    db.commit()
    db.refresh(bee_type)

    response = client.delete(f"/bee_types/{bee_type.id}")
    assert response.status_code == 204
    assert db.query(BeeType).filter(BeeType.id == bee_type.id).first() is None

def test_delete_bee_type_not_found(client):
    response = client.delete("/bee_types/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Abelha não encontrada."
