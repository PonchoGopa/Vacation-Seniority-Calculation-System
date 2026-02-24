from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class VacationPolicy(Base):
    __tablename__ = "vacation_policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    company = relationship("Company", back_populates="policies")
    rules = relationship("VacationPolicyRule", back_populates="policy", cascade="all, delete")
