import pytest


def test_create_company(client):
    """Crear una empresa correctamente"""
    response = client.post("/companies/", json={
        "name": "Empresa Test",
        "bonus_percentage": 0.25
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Empresa Test"
    assert data["bonus_percentage"] == 0.25
    assert "id" in data


def test_create_duplicate_company(client):
    """No debe permitir empresas con el mismo nombre"""
    client.post("/companies/", json={
        "name": "Empresa Test",
        "bonus_percentage": 0.25
    })

    response = client.post("/companies/", json={
        "name": "Empresa Test",
        "bonus_percentage": 0.25
    })

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_get_companies_empty(client):
    """Lista vacía cuando no hay empresas"""
    response = client.get("/companies/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_companies(client, company):
    """Debe retornar la lista de empresas"""
    response = client.get("/companies/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_company_by_id(client, company):
    """Debe retornar la empresa correcta por id"""
    response = client.get(f"/companies/{company['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == company["id"]
    assert response.json()["name"] == company["name"]


def test_get_company_not_found(client):
    """Empresa inexistente debe retornar 404"""
    response = client.get("/companies/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_company(client, company):
    """Actualizar nombre y porcentaje de bono"""
    response = client.put(f"/companies/{company['id']}", json={
        "name": "Empresa Actualizada",
        "bonus_percentage": 0.30
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Empresa Actualizada"
    assert data["bonus_percentage"] == 0.30


def test_update_company_partial(client, company):
    """Actualización parcial solo debe cambiar el campo enviado"""
    response = client.put(f"/companies/{company['id']}", json={
        "bonus_percentage": 0.50
    })

    assert response.status_code == 200
    data = response.json()
    assert data["bonus_percentage"] == 0.50
    assert data["name"] == company["name"]


def test_update_company_not_found(client):
    """Actualizar empresa inexistente debe retornar 404"""
    response = client.put("/companies/999", json={
        "name": "No existe"
    })

    assert response.status_code == 404


def test_delete_company(client, company):
    """Eliminar empresa correctamente"""
    response = client.delete(f"/companies/{company['id']}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Company deleted"


def test_delete_company_not_found(client):
    """Eliminar empresa inexistente debe retornar 404"""
    response = client.delete("/companies/999")

    assert response.status_code == 404