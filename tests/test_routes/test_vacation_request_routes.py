from datetime import date, timedelta


def future_date(days=10):
    """Genera una fecha futura para tests"""
    return (date.today() + timedelta(days=days)).isoformat()


def test_create_vacation_request(client, employee):
    """Crear una solicitud válida"""
    response = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    })

    assert response.status_code == 200
    data = response.json()
    assert data["employee_id"] == employee["id"]
    assert data["status"] == "pending"
    assert data["days_requested"] > 0


def test_create_request_employee_not_found(client):
    """Empleado inexistente debe retornar 404"""
    response = client.post("/vacation-requests/", params={
        "employee_id": 999,
        "start_date": future_date(10),
        "end_date": future_date(15)
    })

    assert response.status_code == 404
    assert "Employee not found" in response.json()["detail"]


def test_create_request_past_date(client, employee):
    """Fecha en el pasado debe retornar 400"""
    response = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": "2024-01-01",
        "end_date": "2024-01-05"
    })

    assert response.status_code == 400
    assert "past" in response.json()["detail"].lower()


def test_create_request_insufficient_advance(client, employee):
    """Menos de 5 días de anticipación debe retornar 400"""
    response = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(2),
        "end_date": future_date(5)
    })

    assert response.status_code == 400
    assert "5 days" in response.json()["detail"]


def test_create_request_end_before_start(client, employee):
    """end_date antes que start_date debe retornar 400"""
    response = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(15),
        "end_date": future_date(10)
    })

    assert response.status_code == 400
    assert "End date cannot be before start date" in response.json()["detail"]


def test_create_request_overlapping(client, employee):
    """Solicitud solapada con una existente debe retornar 400"""
    client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    })

    response = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(12),
        "end_date": future_date(18)
    })

    assert response.status_code == 400
    assert "overlaps" in response.json()["detail"].lower()


def test_create_request_no_policy(client, company):
    """Empleado sin política debe retornar 400"""
    employee_no_policy = client.post("/employees/", json={
        "name": "Sin Política",
        "hire_date": "2022-01-01",
        "daily_salary": 400.0,
        "company_id": company["id"]
    }).json()

    response = client.post("/vacation-requests/", params={
        "employee_id": employee_no_policy["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    })

    assert response.status_code == 400
    assert "vacation policy" in response.json()["detail"].lower()


def test_approve_request(client, employee):
    """Aprobar una solicitud pendiente"""
    request = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    }).json()

    response = client.patch(
        f"/vacation-requests/{request['id']}/approve",
        params={"actor_id": 1}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "approved"


def test_approve_already_approved(client, employee):
    """Aprobar una solicitud ya aprobada debe retornar 400"""
    request = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    }).json()

    client.patch(
        f"/vacation-requests/{request['id']}/approve",
        params={"actor_id": 1}
    )

    response = client.patch(
        f"/vacation-requests/{request['id']}/approve",
        params={"actor_id": 1}
    )

    assert response.status_code == 400
    assert "pending" in response.json()["detail"].lower()


def test_reject_request(client, employee):
    """Rechazar una solicitud pendiente"""
    request = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    }).json()

    response = client.patch(
        f"/vacation-requests/{request['id']}/reject",
        params={"actor_id": 1}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


def test_cancel_request(client, employee):
    """Cancelar una solicitud pendiente"""
    request = client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(15)
    }).json()

    response = client.patch(
        f"/vacation-requests/{request['id']}/cancel",
        params={"actor_id": 1}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"


def test_list_pending_requests(client, employee):
    """Debe listar las solicitudes pendientes"""
    client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(12)
    })

    response = client.get("/vacation-requests/pending")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_list_requests_by_employee(client, employee):
    """Debe listar las solicitudes de un empleado"""
    client.post("/vacation-requests/", params={
        "employee_id": employee["id"],
        "start_date": future_date(10),
        "end_date": future_date(12)
    })

    response = client.get(f"/vacation-requests/employee/{employee['id']}")

    assert response.status_code == 200
    assert len(response.json()) >= 1