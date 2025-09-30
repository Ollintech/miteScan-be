# from models.user import User
# from models.hive_analysis import HiveAnalysis
# from models.analysis_backup import AnalysisBackup

# def create_user_and_analysis_and_backup(db):
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

#     hive_analysis = HiveAnalysis(
#         hive_id=1,
#         user_id=user.id,
#         image_path="images/hive1_analysis.jpg",
#         varroa_detected=True,
#         detection_confidence=0.95
#     )
#     db.add(hive_analysis)
#     db.commit()
#     db.refresh(hive_analysis)

#     backup = AnalysisBackup(
#         analysis_id=hive_analysis.id,
#         user_id=user.id,
#         file_path="backups/analysis_backup_1.zip"
#     )
#     db.add(backup)
#     db.commit()
#     db.refresh(backup)

#     return user, hive_analysis, backup


# def test_create_analysis_backup_success(client, db):
#     user, hive_analysis, backup = create_user_and_analysis_and_backup(db)

#     response = client.post("/analysis_backup/create", json={
#         "analysis_id": hive_analysis.id,
#         "user_id": user.id,
#         "file_path": "backups/analysis_backup_2.zip",
#         "created_at": "2025-04-24T10:00:00Z"
#     })

#     assert response.status_code == 201
#     assert "file_path" in response.json()
#     assert response.json()["file_path"] == "backups/analysis_backup_2.zip"


# def test_get_analysis_backup_success(client, db):
#     user, hive_analysis, backup = create_user_and_analysis_and_backup(db)

#     response = client.get(f"/analysis_backup/{backup.id}")
#     assert response.status_code == 200
#     assert response.json()["file_path"] == "backups/analysis_backup_1.zip"


# def test_get_analysis_backup_not_found(client):
#     response = client.get("/analysis_backup/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Análise de Backup não encontrada."


# def test_delete_analysis_backup_success(client, db):
#     user, hive_analysis, backup = create_user_and_analysis_and_backup(db)

#     response = client.delete(f"/analysis_backup/{backup.id}")
#     assert response.status_code == 204
#     assert db.query(AnalysisBackup).filter(AnalysisBackup.id == backup.id).first() is None


# def test_delete_analysis_backup_not_found(client):
#     response = client.delete("/analysis_backup/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Análise de Backup não encontrada."
