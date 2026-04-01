from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class EmployeeBase(BaseModel):
    name: str = Field(..., max_length=100)
    hire_date: date
    daily_salary: float
    company_id: int
    vacation_policy_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    hire_date: Optional[date] = None
    daily_salary: Optional[float] = None
    vacation_policy_id: Optional[int] = None


class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)