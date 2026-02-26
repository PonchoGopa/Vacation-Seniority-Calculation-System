from sqlalchemy import Column, Integer, Date, ForeignKey, String, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class VacationRequest(Base):
    __tablename__ = "vacation_requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    days_requested = Column(Integer, nullable=False)

    status = Column(String(20), nullable=False, default="pending")

    employee = relationship("Employee", back_populates="vacation_requests")

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_valid_date_range"),
        CheckConstraint("days_requested > 0", name="check_positive_days"),
    )