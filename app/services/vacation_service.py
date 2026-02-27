from datetime import date
from app.models.employee import Employee
from sqlalchemy.orm import Session
from app.models.vacation_request import VacationRequest
from app.services.vacation_calculator import calculate_vacation_balance


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

    employee = db.query(Employee).filter(
        Employee.id == request.employee_id
    ).first()

    # 🔎 Calcular balance actual
    balance_data = calculate_vacation_balance(db, employee.id)
    remaining_balance = balance_data["remaining_balance"]

    if request.days_requested > remaining_balance:
        raise ValueError("Insufficient vacation balance at approval time")

    request.status = "approved"
    request.approved_at = datetime.utcnow()

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

