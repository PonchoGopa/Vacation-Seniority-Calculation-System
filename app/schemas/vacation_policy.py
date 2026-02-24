from pydantic import BaseModel

class VacationPolicyBase(BaseModel):
    base_days: int
    max_days: int
    company_id: int


class VacationPolicyCreate(BaseModel):
    pass

class VacationPolicyRuleCreate(BaseModel):
    pass

class VacationPolicyResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True