from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vacation_policy import VacationPolicy
from app.models.vacation_policy_rule import VacationPolicyRule
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
        raise HTTPException(status_code=400, detail="Policy already exists for this company")

    db_policy = VacationPolicy(
        company_id=policy.company_id,
        name=policy.name
    )

    db.add(db_policy)
    db.flush()  # genera el id sin hacer commit aún

    for rule in policy.rules:
        db_rule = VacationPolicyRule(
            policy_id=db_policy.id,
            years_required=rule.years_required,
            vacation_days=rule.vacation_days
        )
        db.add(db_rule)

    db.commit()
    db.refresh(db_policy)

    return db_policy


@router.get("/", response_model=list[VacationPolicyResponse])
def get_policies(db: Session = Depends(get_db)):
    return db.query(VacationPolicy).all()


@router.get("/{policy_id}", response_model=VacationPolicyResponse)
def get_policy(policy_id: int, db: Session = Depends(get_db)):

    policy = db.query(VacationPolicy).filter(
        VacationPolicy.id == policy_id
    ).first()

    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    return policy