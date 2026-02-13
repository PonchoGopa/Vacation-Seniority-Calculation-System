from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    bonus_percentage: float = Field(default=0.25, ge=0.25)


class CompanyResponse(BaseModel):
    id: int
    name: str
    bonus_percentage: float

    class Config:
        from_attributes = True
