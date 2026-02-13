from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(company_data: CompanyCreate, db: Session = Depends(get_db)):
    
    # Verificar que no exista empresa con mismo nombre
    existing = db.query(Company).filter(Company.name == company_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")

    new_company = Company(
        name=company_data.name,
        bonus_percentage=company_data.bonus_percentage
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company
