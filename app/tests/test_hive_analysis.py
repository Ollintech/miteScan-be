# import pytest
# from datetime import datetime, timezone
# from models import User, BeeType, Hive, HiveAnalysis, Access

# # --- Fixture para gerar headers autenticados ---
# @pytest.fixture
# def auth_headers(client, db):
#     db.query(User).delete()
#     db.query(Access).delete()
#     db.commit()

#     access = Access(id=1, name="owner", description="acesso comum")
#     db.add(access)
#     db.commit()

#     # Criar usuário direto no banco
#     user = User(
#         name="Test User",
#         email="test@example.com",
#         password_hash="$2b$12$123456789012345678901uC9bPwKaI0pE3G1hvBWT0KYk2xE2Pi6",  # Hash fictício
#         access_id=1,
#         company_id=1,
#         status=True
#     )
#     db.add(user)
#     db.commit()

#     # Agora faça o login para gerar token
#     response = client.post("/auth/login", data={
#         "username": "test@example.com",
#         "password": "12345678"
#     })

#     assert response.status_code == 200
#     token = response.json()["access_token"]
#     return {"Authorization": f"Bearer {token}"}

# # --- Função auxiliar para criar dados de teste ---
# def create_user_and_hive_and_analysis(db):
#     user = db.query(User).filter_by(email="test@example.com").first()
#     if not user:
#         raise Exception("Usuário de teste não encontrado no banco.")

#     bee_type = BeeType(
#         name="European Bee",
#         description="Apis mellifera",
#         user_root_id=user.id 
#     )
#     db.add(bee_type)
#     db.commit()
#     db.refresh(bee_type)

#     hive = Hive(
#         bee_type_id=bee_type.id,
#         user_root_id=user.id,
#         location_lat=-23.5505,  # Exemplo: latitude de São Paulo
#         location_lng=-46.6333,  # Exemplo: longitude de São Paulo
#         size=10,
#         humidity=55.0,
#         temperature=30.0
#     )
#     db.add(hive)
#     db.commit()
#     db.refresh(hive)

#     analysis = HiveAnalysis(
#         hive_id=hive.id,
#         user_root_id=user.id,
#         image_path="images/test.jpg",
#         varroa_detected=False,
#         detection_confidence=0.85,
#         created_at=datetime.now(timezone.utc)  # >>> Corrigido warning
#     )
#     db.add(analysis)
#     db.commit()
#     db.refresh(analysis)

#     return user, bee_type, hive, analysis

# # --- Testes ---

# def test_create_hive_analysis_success(client, db, auth_headers):
#     user, bee_type, hive, analysis = create_user_and_hive_and_analysis(db)

#     response = client.post("/hive_analyses/create", json={
#         "hive_id": hive.id,
#         "user_root_id": user.id,
#         "image_path": "images/hive2_analysis.jpg",
#         "varroa_detected": True,
#         "detection_confidence": 0.99
#     }, headers=auth_headers)

#     assert response.status_code == 201

# def test_get_hive_analysis_success(client, db, auth_headers):
#     user, bee_type, hive, analysis = create_user_and_hive_and_analysis(db)

#     response = client.get(f"/hive_analyses/{analysis.id}", headers=auth_headers)

#     assert response.status_code == 200
#     data = response.json()
#     assert data["hive_id"] == hive.id
#     assert data["user_root_id"] == user.id

# def test_get_hive_analysis_not_found(client, auth_headers):
#     response = client.get("/hive_analyses/9999", headers=auth_headers)

#     assert response.status_code == 404

# def test_delete_hive_analysis_success(client, db, auth_headers):
#     user, bee_type, hive, analysis = create_user_and_hive_and_analysis(db)

#     response = client.delete(f"/hive_analyses/{analysis.id}", headers=auth_headers)

#     assert response.status_code == 204

# def test_delete_hive_analysis_not_found(client, auth_headers):
#     response = client.delete("/hive_analyses/9999", headers=auth_headers)

#     assert response.status_code == 404
