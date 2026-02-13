from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class VacationPolicy(Base):
    __tablename__ = "vacation_policies"

    id: Mapped[int] = mapped_column(primary_key=True)
    min_year: Mapped[int] = mapped_column(Integer)
    max_year: Mapped[int] = mapped_column(Integer)
    days: Mapped[int] = mapped_column(Integer)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company = relationship("Company", back_populates="policies")
