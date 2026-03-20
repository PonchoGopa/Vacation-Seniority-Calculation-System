from datetime import date, datetime
from app.models.employee import Employee
from sqlalchemy.orm import Session
from app.models.vacation_request import VacationRequest
from app.services.vacation_calculator import calculate_vacation_balance
from typing import Optional
from app.models.vacation_status import VacationStatus


def calculate_seniority_years(employee: Employee) -> int:
    today = date.today()
    years = today.year - employee.hire_date.year

    # Ajuste si aún no cumple aniversario este año
    if (today.month, today.day) < (employee.hire_date.month, employee.hire_date.day):
        years -= 1

    return max(years, 0)

def approve_vacation_request(db: Session, request_id: int, actor_id: int):
    request = db.query(VacationRequest).filter(
        VacationRequest.id == request_id
    ).first()

    if not request:
        raise ValueError("Request not found")

    if request.status != VacationStatus.pending:
        raise ValueError("Only pending requests can be approved")

    request.status = VacationStatus.approved
    request.approved_at = datetime.utcnow()
    request.approved_by = actor_id

    db.commit()
    db.refresh(request)

    return request

def reject_vacation_request(db: Session, request_id: int, actor_id: int):

    request = db.query(VacationRequest).filter(
        VacationRequest.id == request_id
    ).first()

    if not request:
        raise ValueError("Request not found")

    if request.status != VacationStatus.pending:
        raise ValueError("Only pending requests can be rejected")

    request.status = VacationStatus.rejected
    request.rejected_at = datetime.utcnow()
    request.rejected_by = actor_id

    db.commit()
    db.refresh(request)

    return request


def get_pending_requests(db: Session):
    return (
        db.query(VacationRequest)
        .filter(VacationRequest.status == "pending")
        .order_by(VacationRequest.start_date.asc())
        .all()
    )

def cancel_vacation_request(db: Session, request_id: int, actor_id: int):

    request = db.query(VacationRequest).filter(
        VacationRequest.id == request_id
    ).first()

    if not request:
        raise ValueError("Request not found")

    if request.status != VacationStatus.pending:
        raise ValueError("Only pending requests can be cancelled")

    request.status = VacationStatus.cancelled
    request.cancelled_at = datetime.utcnow()
    request.cancelled_by = actor_id

    db.commit()
    db.refresh(request)

    return request

def get_requests_by_employee(
    db: Session,
    employee_id: int,
    status: Optional[str] = None
):
    query = db.query(VacationRequest).filter(
        VacationRequest.employee_id == employee_id
    )

    if status:
        query = query.filter(VacationRequest.status == status)

    return query.order_by(
        VacationRequest.start_date.desc()
    ).all()

def get_pending_requests(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(VacationRequest).filter(
        VacationRequest.status == VacationStatus.pending
    )

    total = query.count()

    data = (
        query.order_by(VacationRequest.start_date.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": data
    }

def get_requests_by_employee(
    db: Session,
    employee_id: int,
    status: Optional[VacationStatus] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(VacationRequest).filter(
        VacationRequest.employee_id == employee_id
    )

    if status:
        query = query.filter(VacationRequest.status == status)

    return (
        query.order_by(VacationRequest.start_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

