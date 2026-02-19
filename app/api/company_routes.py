from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# CREATE
@router.post("/", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):

    existing = db.query(Company).filter(Company.name == company.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")

    db_company = Company(
        name=company.name,
        bonus_percentage=company.bonus_percentage
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


# READ ALL
@router.get("/", response_model=list[CompanyResponse])
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()


# READ ONE
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):

    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


# UPDATE
@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db)
):

    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    if company_data.name is not None:
        company.name = company_data.name

    if company_data.bonus_percentage is not None:
        company.bonus_percentage = company_data.bonus_percentage

    db.commit()
    db.refresh(company)

    return company


# DELETE
@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):

    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company)
    db.commit()

    return {"detail": "Company deleted"}
