# from models.user import User
# from models.access import Access
# from models.company import Company
# from core.auth import get_password_hash

# def create_dependencies(db):
#     access = Access(name="Padrão", description="Acesso comum")
#     company = Company(name="Empresa X", cnpj="11223344556677")
#     db.add_all([access, company])
#     db.commit()
#     db.refresh(access)
#     db.refresh(company)
#     return access.id, company.id

# def test_create_user_success(client, db):
#     access_id, company_id = create_dependencies(db)

#     response = client.post("/users/create", json={
#         "name": "João Silva",
#         "email": "joao@email.com",
#         "password": "minhasenha",
#         "access_id": access_id,
#         "company_id": company_id
#     })

#     assert response.status_code == 201
#     data = response.json()
#     assert data["name"] == "João Silva"
#     assert data["email"] == "joao@email.com"
#     assert data["status"] is False
#     assert "id" in data

# def test_create_user_email_duplicado(client, db):
#     access_id, company_id = create_dependencies(db)
#     user = User(
#         name="Usuário Existente",
#         email="joao@email.com",
#         password_hash=get_password_hash("senhaforte"),
#         status=False,
#         access_id=access_id,
#         company_id=company_id
#     )
#     db.add(user)
#     db.commit()

#     response = client.post("/users/create", json={
#         "name": "Novo",
#         "email": "joao@email.com",
#         "password": "senhaforte",
#         "access_id": access_id,
#         "company_id": company_id
#     })

#     assert response.status_code == 400
#     assert response.json()["detail"] == "Email já cadastrado."

# def test_get_user_success(client, db):
#     access_id, company_id = create_dependencies(db)
#     user = User(
#         name="Maria",
#         email="maria@email.com",
#         password_hash=get_password_hash("senha123"),
#         status=True,
#         access_id=access_id,
#         company_id=company_id
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     response = client.get(f"/users/{user.id}")
#     assert response.status_code == 200
#     assert response.json()["name"] == "Maria"
#     assert response.json()["email"] == "maria@email.com"

# def test_get_user_not_found(client):
#     response = client.get("/users/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Usuário não encontrado."

# def test_update_user_success(client, db):
#     access_id, company_id = create_dependencies(db)
#     user = User(
#         name="Carlos",
#         email="carlos@email.com",
#         password_hash=get_password_hash("senhaforte"),
#         status=False,
#         access_id=access_id,
#         company_id=company_id
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     response = client.put(f"/users/{user.id}", json={
#         "name": "Carlos Atualizado",
#         "status": True
#     })

#     assert response.status_code == 200
#     assert response.json()["name"] == "Carlos Atualizado"
#     assert response.json()["status"] is True

# def test_update_user_email_duplicado(client, db):
#     access_id, company_id = create_dependencies(db)
#     user1 = User(
#         name="User1", email="email1@test.com",
#         password_hash=get_password_hash("senha1"),
#         status=False, access_id=access_id, company_id=company_id)
#     user2 = User(
#         name="User2", email="email2@test.com",
#         password_hash=get_password_hash("senha2"),
#         status=False, access_id=access_id, company_id=company_id)
#     db.add_all([user1, user2])
#     db.commit()

#     response = client.put(f"/users/{user2.id}", json={"email": "email1@test.com"})
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Email já cadastrado."

# def test_delete_user_success(client, db):
#     access_id, company_id = create_dependencies(db)
#     user = User(
#         name="Apagar", email="apagar@email.com",
#         password_hash=get_password_hash("senha123"),
#         status=False, access_id=access_id, company_id=company_id
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     response = client.delete(f"/users/{user.id}")
#     assert response.status_code == 204

#     assert db.query(User).filter(User.id == user.id).first() is None

# def test_delete_user_not_found(client):
#     response = client.delete("/users/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Usuário não encontrado."
