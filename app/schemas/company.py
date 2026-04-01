from pydantic import BaseModel, Field
from pydantic import ConfigDict

class CompanyBase(BaseModel):
    name: str = Field(..., max_length=100)
    bonus_percentage: float = 0.25


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    bonus_percentage: float | None = None


class CompanyResponse(CompanyBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
