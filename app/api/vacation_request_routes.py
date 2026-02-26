from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vacation_request import VacationRequest
from app.models.employee import Employee
from app.services.date_utils import calculate_business_days
from app.services.vacation_calculator import calculate_vacation_balance
from app.services.vacation_service import approve_vacation_request

router = APIRouter(prefix="/vacation-requests", tags=["Vacation Requests"])


@router.post("/")
def create_vacation_request(
    employee_id: int,
    start_date,
    end_date,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    overlapping_request = (
        db.query(VacationRequest)
        .filter(
            VacationRequest.employee_id == employee_id,
            VacationRequest.status.in_(["pending", "approved"]),
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
    days_requested = calculate_business_days(start_date, end_date)

    # Obtener días ya usados (solo approved)
    approved_requests = (
        db.query(VacationRequest)
        .filter(
            VacationRequest.employee_id == employee_id,
            VacationRequest.status == "approved"
        )
        .all()
    )

    total_days_used = sum(req.days_requested for req in approved_requests)

    # Calcular balance actual
    balance = calculate_vacation_balance(
        employee=employee,
        policy_rules=employee.vacation_policy.rules,
        days_used=total_days_used
    )

    remaining_balance = balance["remaining_balance"]

    # Validar que no exceda
    if days_requested > remaining_balance:
        raise HTTPException(
            status_code=400,
            detail=f"Request exceeds available balance. Available: {remaining_balance} days"
        )

    # Crear solicitud
    new_request = VacationRequest(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date,
        days_requested=days_requested,
        status="pending"
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request

@router.patch("/{request_id}/approve")
def approve_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    try:
        updated_request = approve_vacation_request(db, request_id)
        return {
            "message": "Vacation request approved successfully",
            "data": updated_request
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{request_id}/reject")
def reject_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    try:
        updated_request = reject_vacation_request(db, request_id)
        return {
            "message": "Vacation request rejected successfully",
            "data": updated_request
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))