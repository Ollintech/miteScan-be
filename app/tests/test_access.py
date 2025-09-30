from models.access import Access
from tests.mock_data import mock_access, mock_access_response


def test_get_access_success(client, db):
    db.query(Access).delete()
    db.commit()

    access_data = mock_access()
    access = Access(**access_data)
    db.add(access)
    db.commit()
    db.refresh(access)

    response = client.get(f"/access/{access.id}")

    expected_response = mock_access_response()
    expected_response["id"] = access.id

    assert response.status_code == 200
    assert response.json() == expected_response


def test_get_access_not_found(client):
    response = client.get("/access/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Acesso não encontrado."
