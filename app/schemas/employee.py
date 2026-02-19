from datetime import date
from pydantic import BaseModel, Field


class EmployeeBase(BaseModel):
    name: str = Field(..., max_length=100)
    hire_date: date
    daily_salary: float
    company_id: int


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: str | None = None
    hire_date: date | None = None
    daily_salary: float | None = None


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
