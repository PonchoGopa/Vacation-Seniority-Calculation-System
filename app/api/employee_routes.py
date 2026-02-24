from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.company import Company
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)
from app.services.vacation_service import calculate_seniority_years

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

    db_employee = Employee(
        name=employee.name,
        hire_date=employee.hire_date,
        daily_salary=employee.daily_salary,
        company_id=employee.company_id
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

    if data.name is not None:
        employee.name = data.name

    if data.hire_date is not None:
        employee.hire_date = data.hire_date

    if data.daily_salary is not None:
        employee.daily_salary = data.daily_salary

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
    pass