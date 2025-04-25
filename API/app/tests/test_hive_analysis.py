# from models.user import User
# from models.bee_type import BeeType
# from models.hive import Hive
# from models.hive_analysis import HiveAnalysis

# def create_user_and_hive_and_analysis(db):
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

#     hive = Hive(
#         user_id=user.id,
#         bee_type_id=bee_type.id,
#         location_lat=1.1,
#         location_lng=2.2,
#         size=10
#     )
#     db.add(hive)
#     db.commit()
#     db.refresh(hive)

#     analysis = HiveAnalysis(
#         hive_id=hive.id,
#         user_id=user.id,
#         image_path="images/hive1_analysis.jpg",
#         varroa_detected=True,
#         detection_confidence=0.95
#     )
#     db.add(analysis)
#     db.commit()
#     db.refresh(analysis)

#     return user, bee_type, hive, analysis


# def test_create_hive_analysis_success(client, db):
#     user, bee_type, hive, analysis = create_user_and_hive_and_analysis(db)

#     response = client.post("/hive_analyses/create", json={
#         "hive_id": hive.id,
#         "user_id": user.id,
#         "image_path": "images/hive2_analysis.jpg",
#         "varroa_detected": True,
#         "detection_confidence": 0.99
#     })

#     assert response.status_code == 201
#     assert "Análise da colmeia realizada com sucesso" in response.json()["message"]


# def test_get_hive_analysis_success(client, db):
#     user, bee_type, hive, analysis = create_user_and_hive_and_analysis(db)

#     response = client.get(f"/hive_analyses/{analysis.id}")
#     assert response.status_code == 200
#     assert response.json()["detection_confidence"] == 0.95
#     assert response.json()["varroa_detected"] is True


# def test_get_hive_analysis_not_found(client):
#     response = client.get("/hive_analyses/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Análise da colmeia não encontrada."


# def test_delete_hive_analysis_success(client, db):
#     user, bee_type, hive, analysis = create_user_and_hive_and_analysis(db)

#     response = client.delete(f"/hive_analyses/{analysis.id}")
#     assert response.status_code == 204
#     assert db.query(HiveAnalysis).filter(HiveAnalysis.id == analysis.id).first() is None


# def test_delete_hive_analysis_not_found(client):
#     response = client.delete("/hive_analyses/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Análise de colmeia não encontrada."
