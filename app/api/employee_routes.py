from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.employee import Employee
from app.models.company import Company
from app.models.vacation_request import VacationRequest
from app.models.vacation_policy import VacationPolicy
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)
from app.services.vacation_service import calculate_seniority_years
from app.services.vacation_calculator import calculate_vacation_balance
from app.core.service import calculate_vacation_bonus_for_employee

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

    company = db.query(Company).filter(
        Company.id == employee.company_id
    ).first()

    if not company:
        raise HTTPException(status_code=400, detail="Company does not exist")

    if employee.vacation_policy_id is not None:
        policy = db.query(VacationPolicy).filter(
            VacationPolicy.id == employee.vacation_policy_id
        ).first()

        if not policy:
            raise HTTPException(status_code=400, detail="Vacation policy does not exist")

        if policy.company_id != employee.company_id:
            raise HTTPException(
                status_code=400,
                detail="Vacation policy does not belong to this company"
            )

    db_employee = Employee(
        name=employee.name,
        hire_date=employee.hire_date,
        daily_salary=employee.daily_salary,
        company_id=employee.company_id,
        vacation_policy_id=employee.vacation_policy_id
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if data.vacation_policy_id is not None:
        policy = db.query(VacationPolicy).filter(
            VacationPolicy.id == data.vacation_policy_id
        ).first()

        if not policy:
            raise HTTPException(status_code=400, detail="Vacation policy does not exist")

        if policy.company_id != employee.company_id:
            raise HTTPException(
                status_code=400,
                detail="Vacation policy does not belong to this company"
            )

    if data.name is not None:
        employee.name = data.name

    if data.hire_date is not None:
        employee.hire_date = data.hire_date

    if data.daily_salary is not None:
        employee.daily_salary = data.daily_salary

    if data.vacation_policy_id is not None:
        employee.vacation_policy_id = data.vacation_policy_id

    db.commit()
    db.refresh(employee)

    return employee


@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"detail": "Employee deleted"}


@router.get("/{employee_id}/seniority")
def get_employee_seniority(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    years = calculate_seniority_years(employee)

    return {
        "employee_id": employee.id,
        "seniority_years": years
    }


@router.get("/{employee_id}/vacation-balance")
def get_vacation_balance(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not employee.vacation_policy:
        raise HTTPException(
            status_code=400,
            detail="Employee does not have a vacation policy assigned"
        )

    approved_requests = (
        db.query(VacationRequest)
        .filter(
            VacationRequest.employee_id == employee_id,
            VacationRequest.status == "approved"
        )
        .all()
    )

    total_days_used = sum(req.days_requested for req in approved_requests)

    result = calculate_vacation_balance(
        employee=employee,
        policy_rules=employee.vacation_policy.rules,
        days_used=total_days_used
    )

    return result


@router.get("/{employee_id}/vacation-bonus")
def get_vacation_bonus(employee_id: int, db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    if not employee.vacation_policy:
        raise HTTPException(
            status_code=400,
            detail="Employee does not have a vacation policy assigned"
        )

    if not employee.company:
        raise HTTPException(
            status_code=400,
            detail="Employee does not have a company assigned"
        )

    approved_requests = (
        db.query(VacationRequest)
        .filter(
            VacationRequest.employee_id == employee_id,
            VacationRequest.status == "approved"
        )
        .all()
    )

    total_days_used = sum(req.days_requested for req in approved_requests)

    balance = calculate_vacation_balance(
        employee=employee,
        policy_rules=employee.vacation_policy.rules,
        days_used=total_days_used
    )

    vacation_days = balance["total_days_entitled"]

    result = calculate_vacation_bonus_for_employee(
        hire_date=employee.hire_date,
        calculation_date=date.today(),
        daily_salary=employee.daily_salary,
        vacation_days=vacation_days,
        bonus_percentage=employee.company.bonus_percentage
    )

    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        "daily_salary": employee.daily_salary,
        "bonus_percentage": employee.company.bonus_percentage,
        **result
    }