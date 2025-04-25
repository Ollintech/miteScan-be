# from models.user import User
# from models.bee_type import BeeType
# from models.hive import Hive

# def create_user_and_bee_type(db):
#     user = User(
#         name="Zelador",
#         email="zelador@teste.com",
#         password_hash="senha123",
#         status=True,
#         access_id=1,
#         company_id=1
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     bee_type = BeeType(
#         name="Abelha Jataí",
#         description="Abelha sem ferrão",
#         user_id=user.id
#     )
#     db.add(bee_type)
#     db.commit()
#     db.refresh(bee_type)

#     return user, bee_type

# def test_create_hive_success(client, db):
#     user, bee_type = create_user_and_bee_type(db)

#     response = client.post("/hives/create", json={
#         "user_id": user.id,
#         "bee_type_id": bee_type.id,
#         "location_lat": -23.5505,
#         "location_lng": -46.6333,
#         "size": 10
#     })

#     assert response.status_code == 201
#     assert "Colmeia criada com sucesso" in response.json()["message"]

# def test_create_hive_duplicate_location(client, db):
#     user, bee_type = create_user_and_bee_type(db)

#     hive = Hive(
#         user_id=user.id,
#         bee_type_id=bee_type.id,
#         location_lat=-10.0,
#         location_lng=10.0,
#         size=5
#     )
#     db.add(hive)
#     db.commit()

#     response = client.post("/hives/create", json={
#         "user_id": user.id,
#         "bee_type_id": bee_type.id,
#         "location_lat": -10.0,
#         "location_lng": 10.0,
#         "size": 5
#     })

#     assert response.status_code == 400
#     assert response.json()["detail"] == "Uma colmeia já foi cadastrada nessa localização."

# def test_get_hive_success(client, db):
#     user, bee_type = create_user_and_bee_type(db)

#     hive = Hive(
#         user_id=user.id,
#         bee_type_id=bee_type.id,
#         location_lat=1.1,
#         location_lng=2.2,
#         size=15
#     )
#     db.add(hive)
#     db.commit()
#     db.refresh(hive)

#     response = client.get(f"/hives/{hive.id}")
#     assert response.status_code == 200
#     assert response.json()["size"] == 15
#     assert response.json()["location_lat"] == 1.1

# def test_get_hive_not_found(client):
#     response = client.get("/hives/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Colmeia não encontrada."

# def test_update_hive_success(client, db):
#     user, bee_type = create_user_and_bee_type(db)

#     hive = Hive(
#         user_id=user.id,
#         bee_type_id=bee_type.id,
#         location_lat=3.3,
#         location_lng=4.4,
#         size=8
#     )
#     db.add(hive)
#     db.commit()
#     db.refresh(hive)

#     response = client.put(f"/hives/{hive.id}", json={
#         "size": 20,
#         "humidity": 55.5
#     })

#     assert response.status_code == 200
#     assert response.json()["size"] == 20
#     assert response.json()["humidity"] == 55.5

# def test_update_hive_not_found(client):
#     response = client.put("/hives/9999", json={"size": 10})
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Colmeia não encontrada."

# def test_delete_hive_success(client, db):
#     user, bee_type = create_user_and_bee_type(db)

#     hive = Hive(
#         user_id=user.id,
#         bee_type_id=bee_type.id,
#         location_lat=5.5,
#         location_lng=6.6,
#         size=12
#     )
#     db.add(hive)
#     db.commit()
#     db.refresh(hive)

#     response = client.delete(f"/hives/{hive.id}")
#     assert response.status_code == 204
#     assert db.query(Hive).filter(Hive.id == hive.id).first() is None

# def test_delete_hive_not_found(client):
#     response = client.delete("/hives/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Colmeia não encontrada."
