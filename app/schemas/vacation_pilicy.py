from pydantic import BaseModel


class VacationPolicyBase(BaseModel):
    base_days: int
    max_days: int
    company_id: int


class VacationPolicyCreate(VacationPolicyBase):
    pass


class VacationPolicyResponse(VacationPolicyBase):
    id: int

    class Config:
        from_attributes = True