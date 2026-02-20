from pydantic import BaseModel, Field


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

    class Config:
        from_attributes = True

policy = relationship(
    "policy",
    back_populates="company",
    uselist=False
)