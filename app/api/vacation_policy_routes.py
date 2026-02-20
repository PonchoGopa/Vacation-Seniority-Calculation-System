from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vacation_policy import VacationPolicy
from app.models.company import Company
from app.schemas.vacation_policy import (
    VacationPolicyCreate,
    VacationPolicyResponse
)

router = APIRouter(
    prefix="/policies",
    tags=["Vacation Policies"]
)


@router.post("/", response_model=VacationPolicyResponse)
def create_policy(policy: VacationPolicyCreate, db: Session = Depends(get_db)):

    company = db.query(Company).filter(
        Company.id == policy.company_id
    ).first()

    if not company:
        raise HTTPException(status_code=400, detail="Company does not exist")

    existing = db.query(VacationPolicy).filter(
        VacationPolicy.company_id == policy.company_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Policy already exists")

    db_policy = VacationPolicy(
        company_id=policy.company_id,
        base_days=policy.base_days,
        max_days=policy.max_days
    )

    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)

    return db_policy


@router.get("/", response_model=list[VacationPolicyResponse])
def get_policies(db: Session = Depends(get_db)):
    return db.query(VacationPolicy).all()