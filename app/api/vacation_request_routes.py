from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vacation_request import VacationRequest
from app.models.employee import Employee
from app.services.date_utils import calculate_business_days
from app.services.vacation_calculator import calculate_vacation_balance
from app.services.vacation_service import (
    approve_vacation_request,
    reject_vacation_request,
    cancel_vacation_request,
    get_pending_requests,
    get_requests_by_employee
)
from typing import Optional
from app.models.vacation_status import VacationStatus
from datetime import date, timedelta

router = APIRouter(prefix="/vacation-requests", tags=["Vacation Requests"])


@router.post("/")
def create_vacation_request(
    employee_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    # Validar que el empleado existe
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Validar que el empleado tiene política asignada
    if not employee.vacation_policy:
        raise HTTPException(
            status_code=400,
            detail="Employee does not have a vacation policy assigned"
        )

    # Validar que la fecha de inicio no sea en el pasado
    today = date.today()
    if start_date < today:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be in the past"
        )

    # Validar anticipación mínima de 5 días
    min_start_date = today + timedelta(days=5)
    if start_date < min_start_date:
        raise HTTPException(
            status_code=400,
            detail=f"Vacation requests must be submitted at least 5 days in advance. Earliest allowed date: {min_start_date}"
        )

    # Validar que end_date no sea antes que start_date
    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    # Validar solapamiento con solicitudes existentes
    overlapping_request = (
        db.query(VacationRequest)
        .filter(
            VacationRequest.employee_id == employee_id,
            VacationRequest.status.in_(
                [VacationStatus.pending, VacationStatus.approved]
            ),
            VacationRequest.start_date <= end_date,
            VacationRequest.end_date >= start_date
        )
        .first()
    )

    if overlapping_request:
        raise HTTPException(
            status_code=400,
            detail="Vacation request overlaps with an existing request"
        )

    # Calcular días hábiles solicitados
    days_requested = calculate_business_days(start_date, end_date)

    # Obtener días ya usados
    approved_requests = (
        db.query(VacationRequest)
        .filter(
            VacationRequest.employee_id == employee_id,
            VacationRequest.status == VacationStatus.approved
        )
        .all()
    )

    total_days_used = sum(req.days_requested for req in approved_requests)

    # Calcular balance disponible
    balance = calculate_vacation_balance(
        employee=employee,
        policy_rules=employee.vacation_policy.rules,
        days_used=total_days_used
    )

    remaining_balance = balance["remaining_balance"]

    # Validar que no exceda el balance
    if days_requested > remaining_balance:
        raise HTTPException(
            status_code=400,
            detail=f"Request exceeds available balance. Available: {remaining_balance} days, Requested: {days_requested} days"
        )

    # Crear solicitud
    new_request = VacationRequest(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        days_requested=days_requested,
        status=VacationStatus.pending
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.patch("/{request_id}/approve")
def approve_request(
    request_id: int,
    actor_id: int,
    db: Session = Depends(get_db)
):
    try:
        return approve_vacation_request(db, request_id, actor_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{request_id}/reject")
def reject_request(
    request_id: int,
    actor_id: int,
    db: Session = Depends(get_db)
):
    try:
        return reject_vacation_request(db, request_id, actor_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{request_id}/cancel")
def cancel_request(
    request_id: int,
    actor_id: int,
    db: Session = Depends(get_db)
):
    try:
        return cancel_vacation_request(db, request_id, actor_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/pending")
def list_pending_requests(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_pending_requests(db, skip=skip, limit=limit)


@router.get("/employee/{employee_id}")
def list_requests_by_employee(
    employee_id: int,
    status: Optional[VacationStatus] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_requests_by_employee(
        db=db,
        employee_id=employee_id,
        status=status,
        skip=skip,
        limit=limit
    )