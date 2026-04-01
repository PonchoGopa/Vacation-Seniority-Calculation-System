from pydantic import BaseModel, ConfigDict
from typing import List


class VacationPolicyRuleCreate(BaseModel):
    years_required: int
    vacation_days: int


class VacationPolicyRuleResponse(BaseModel):
    id: int
    years_required: int
    vacation_days: int

    model_config = ConfigDict(from_attributes=True)


class VacationPolicyCreate(BaseModel):
    company_id: int
    name: str
    rules: List[VacationPolicyRuleCreate]


class VacationPolicyResponse(BaseModel):
    id: int
    name: str
    company_id: int
    rules: List[VacationPolicyRuleResponse]

    model_config = ConfigDict(from_attributes=True)