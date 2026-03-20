from pydantic import BaseModel
from typing import List


class VacationPolicyRuleCreate(BaseModel):
    years_required: int
    vacation_days: int


class VacationPolicyRuleResponse(BaseModel):
    id: int
    years_required: int
    vacation_days: int

    class Config:
        from_attributes = True


class VacationPolicyCreate(BaseModel):
    company_id: int
    name: str
    rules: List[VacationPolicyRuleCreate]


class VacationPolicyResponse(BaseModel):
    id: int
    name: str
    company_id: int
    rules: List[VacationPolicyRuleResponse]

    class Config:
        from_attributes = True