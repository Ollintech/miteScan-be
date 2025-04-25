# import pytest
# from fastapi.testclient import TestClient
# from models.hive import Hive
# from schemas.sensor import SensorRead

# def test_receber_dados_sensor(client: TestClient, init_db):
#     sensor_data = {
#         "colmeia_id": 1,
#         "temperature": 25.5,
#         "humidity": 60.0
#     }

#     hive = Hive(
#         id=1,
#         user_id=1,
#         bee_type_id=1,
#         location_lat=12.34,
#         location_lng=56.78,
#         size=10
#     )
#     init_db.add(hive)
#     init_db.commit()

#     response = client.post("/sensor/", json=sensor_data)

#     assert response.status_code == 200
#     assert response.json() == {"message": "Leitura recebida com sucesso"}

#     updated_hive = init_db.query(Hive).filter(Hive.id == 1).first()
#     assert updated_hive.temperature == 25.5
#     assert updated_hive.humidity == 60.0

# def test_colmeia_nao_encontrada(client: TestClient, init_db):
#     sensor_data = {
#         "colmeia_id": 999,
#         "temperature": 25.5,
#         "humidity": 60.0
#     }

#     response = client.post("/sensor/", json=sensor_data)

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Colmeia não encontrada"}
