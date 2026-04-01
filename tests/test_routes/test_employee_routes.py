def test_create_employee(client, company, policy):
    """Crear un empleado correctamente"""
    response = client.post("/employees/", json={
        "name": "Ana García",
        "hire_date": "2022-01-01",
        "daily_salary": 400.0,
        "company_id": company["id"],
        "vacation_policy_id": policy["id"]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ana García"
    assert data["vacation_policy_id"] == policy["id"]
    assert "id" in data


def test_create_employee_invalid_company(client):
    """Empresa inexistente debe retornar 400"""
    response = client.post("/employees/", json={
        "name": "Ana García",
        "hire_date": "2022-01-01",
        "daily_salary": 400.0,
        "company_id": 999
    })

    assert response.status_code == 400
    assert "Company does not exist" in response.json()["detail"]


def test_create_employee_invalid_policy(client, company):
    """Política inexistente debe retornar 400"""
    response = client.post("/employees/", json={
        "name": "Ana García",
        "hire_date": "2022-01-01",
        "daily_salary": 400.0,
        "company_id": company["id"],
        "vacation_policy_id": 999
    })

    assert response.status_code == 400
    assert "Vacation policy does not exist" in response.json()["detail"]


def test_create_employee_policy_wrong_company(client):
    """Política de otra empresa debe retornar 400"""
    company1 = client.post("/companies/", json={
        "name": "Empresa 1",
        "bonus_percentage": 0.25
    }).json()

    company2 = client.post("/companies/", json={
        "name": "Empresa 2",
        "bonus_percentage": 0.25
    }).json()

    policy = client.post("/policies/", json={
        "company_id": company1["id"],
        "name": "Política Empresa 1",
        "rules": [{"years_required": 1, "vacation_days": 12}]
    }).json()

    response = client.post("/employees/", json={
        "name": "Ana García",
        "hire_date": "2022-01-01",
        "daily_salary": 400.0,
        "company_id": company2["id"],
        "vacation_policy_id": policy["id"]
    })

    assert response.status_code == 400
    assert "does not belong to this company" in response.json()["detail"]


def test_get_employees_empty(client):
    """Lista vacía cuando no hay empleados"""
    response = client.get("/employees/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_employees(client, employee):
    """Debe retornar la lista de empleados"""
    response = client.get("/employees/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_employee_by_id(client, employee):
    """Debe retornar el empleado correcto por id"""
    response = client.get(f"/employees/{employee['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == employee["id"]
    assert response.json()["name"] == employee["name"]


def test_get_employee_not_found(client):
    """Empleado inexistente debe retornar 404"""
    response = client.get("/employees/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_employee(client, employee):
    """Actualizar nombre y salario del empleado"""
    response = client.put(f"/employees/{employee['id']}", json={
        "name": "Juan Actualizado",
        "daily_salary": 600.0
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Juan Actualizado"
    assert data["daily_salary"] == 600.0


def test_update_employee_not_found(client):
    """Actualizar empleado inexistente debe retornar 404"""
    response = client.put("/employees/999", json={
        "name": "No existe"
    })

    assert response.status_code == 404


def test_delete_employee(client, employee):
    """Eliminar empleado correctamente"""
    response = client.delete(f"/employees/{employee['id']}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Employee deleted"


def test_delete_employee_not_found(client):
    """Eliminar empleado inexistente debe retornar 404"""
    response = client.delete("/employees/999")

    assert response.status_code == 404


def test_get_seniority(client, employee):
    """Debe retornar la antigüedad correcta del empleado"""
    response = client.get(f"/employees/{employee['id']}/seniority")

    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == employee["id"]
    assert data["seniority_years"] >= 3


def test_get_vacation_balance(client, employee):
    """Debe retornar el balance de vacaciones correctamente"""
    response = client.get(f"/employees/{employee['id']}/vacation-balance")

    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == employee["id"]
    assert "total_days_entitled" in data
    assert "remaining_balance" in data
    assert "days_used" in data
    assert data["days_used"] == 0
    assert data["remaining_balance"] == data["total_days_entitled"]


def test_get_vacation_balance_no_policy(client, company):
    """Empleado sin política debe retornar 400"""
    employee_no_policy = client.post("/employees/", json={
        "name": "Sin Política",
        "hire_date": "2022-01-01",
        "daily_salary": 400.0,
        "company_id": company["id"]
    }).json()

    response = client.get(f"/employees/{employee_no_policy['id']}/vacation-balance")

    assert response.status_code == 400
    assert "vacation policy" in response.json()["detail"].lower()


def test_get_vacation_bonus(client, employee):
    """Debe retornar la prima vacacional correctamente"""
    response = client.get(f"/employees/{employee['id']}/vacation-bonus")

    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == employee["id"]
    assert "bonus_amount" in data
    assert "vacation_days" in data
    assert data["bonus_amount"] > 0