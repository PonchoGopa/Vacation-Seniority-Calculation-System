from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class VacationPolicyRule(Base):
    __tablename__ = "vacation_policy_rules"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("vacation_policies.id"), nullable=False)
    years_required = Column(Integer, nullable=False)
    vacation_days = Column(Integer, nullable=False)

    policy = relationship("VacationPolicy", back_populates="rules")