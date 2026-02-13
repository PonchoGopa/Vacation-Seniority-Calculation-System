from datetime import date, datetime
from sqlalchemy import ForeignKey, Date, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class VacationCalculation(Base):
    __tablename__ = "vacation_calculations"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    calculation_date: Mapped[date] = mapped_column(Date)

    years_completed: Mapped[int] = mapped_column(Integer)
    vacation_days: Mapped[float] = mapped_column(Float)
    bonus_amount: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="calculations")
