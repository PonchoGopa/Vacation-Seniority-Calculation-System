from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    bonus_percentage: Mapped[float] = mapped_column(Float, default=0.25)

    employees = relationship("Employee", back_populates="company")
    policies = relationship("VacationPolicy", back_populates="company")

policy = relationship(
    "policy",
    back_populates="company",
    uselist=False
)