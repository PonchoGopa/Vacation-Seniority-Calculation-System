from datetime import date
from sqlalchemy import ForeignKey, Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    hire_date: Mapped[date] = mapped_column(Date)
    daily_salary: Mapped[float] = mapped_column(Float)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company = relationship("Company", back_populates="employees")

    calculations = relationship("VacationCalculation", back_populates="employee")
