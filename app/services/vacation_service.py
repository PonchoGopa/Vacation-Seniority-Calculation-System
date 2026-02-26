from datetime import date
from app.models.employee import Employee
from sqlalchemy.orm import Session
from app.models.vacation_request import VacationRequest


def calculate_seniority_years(employee: Employee) -> int:
    today = date.today()
    years = today.year - employee.hire_date.year

    # Ajuste si aún no cumple aniversario este año
    if (today.month, today.day) < (employee.hire_date.month, employee.hire_date.day):
        years -= 1

    return max(years, 0)

def approve_vacation_request(db: Session, request_id: int):
    request = db.query(VacationRequest).filter(
        VacationRequest.id == request_id
    ).first()

    if not request:
        raise ValueError("Request not found")

    if request.status != "pending":
        raise ValueError("Only pending requests can be approved")

    request.status = "approved"

    db.commit()
    db.refresh(request)

    return request

def reject_vacation_request(db: Session, request_id: int):
    request = db.query(VacationRequest).filter(
        VacationRequest.id == request_id
    ).first()

    if not request:
        raise ValueError("Request not found")

    if request.status != "pending":
        raise ValueError("Only pending requests can be rejected")

    request.status = "rejected"

    db.commit()
    db.refresh(request)

    return request

