# from models.access import Access

# def test_get_access_success(client, db):
#     db.query(Access).delete()
#     db.commit()

#     access = Access(name="Admin", description="Acesso total ao sistema")
#     db.add(access)
#     db.commit()
#     db.refresh(access)

#     response = client.get(f"/access/{access.id}")

#     assert response.status_code == 200
#     assert response.json() == {
#         "id": access.id,
#         "name": "Admin",
#         "description": "Acesso total ao sistema"
#     }

# def test_get_access_not_found(client):
#     response = client.get("/access/9999")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Acesso não encontrado."
