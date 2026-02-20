from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class VacationPolicy(Base):
    __tablename__ = "vacation_policies"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        unique=True
    )

    base_days: Mapped[int] = mapped_column(Integer, default=12)
    max_days: Mapped[int] = mapped_column(Integer, default=20)

    company = relationship("Company", back_populates="policy")


