from models.company import Company
from tests.mock_data import mock_company, mock_company_response


def test_create_company_success(client, db):
    db.query(Company).delete()
    db.commit()

    company_data = mock_company()

    response = client.post("/companies/create", json=company_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == company_data["name"]
    assert data["cnpj"] == company_data["cnpj"]
    assert "id" in data


def test_create_company_duplicate_cnpj(client, db):
    company_data = mock_company()
    company = Company(**company_data)
    db.add(company)
    db.commit()

    response = client.post("/companies/create", json={
        "name": "Outra Empresa",
        "cnpj": company_data["cnpj"]
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "CNPJ já cadastrado."


def test_get_company_success(client, db):
    company_data = {"name": "Empresa Teste", "cnpj": "98765432000199"}
    company = Company(**company_data)
    db.add(company)
    db.commit()
    db.refresh(company)

    response = client.get(f"/companies/{company.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": company.id,
        **company_data
    }


def test_get_company_not_found(client):
    response = client.get("/companies/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Empresa não encontrada."


def test_update_company_success(client, db):
    company = Company(name="Antigo Nome", cnpj="11111111111111")
    db.add(company)
    db.commit()
    db.refresh(company)

    response = client.put(f"/companies/{company.id}", json={
        "name": "Novo Nome"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Novo Nome"
    assert response.json()["cnpj"] == "11111111111111"


def test_update_company_duplicate_cnpj(client, db):
    db.query(Company).delete()
    db.commit()

    company1 = Company(name="Empresa 1", cnpj="12345678900001")
    company2 = Company(name="Empresa 2", cnpj="22222222222222")
    db.add_all([company1, company2])
    db.commit()

    response = client.put(f"/companies/{company2.id}", json={
        "cnpj": company1.cnpj
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "CNPJ já cadastrado."


def test_delete_company_success(client, db):
    company = Company(name="Empresa Excluir", cnpj="33333333333333")
    db.add(company)
    db.commit()
    db.refresh(company)

    response = client.delete(f"/companies/{company.id}")
    assert response.status_code == 204

    deleted = db.query(Company).filter_by(id=company.id).first()
    assert deleted is None


def test_delete_company_not_found(client):
    response = client.delete("/companies/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Empresa não encontrada."
