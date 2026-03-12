from sqlalchemy import Column, Integer, Date, ForeignKey, CheckConstraint, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.vacation_status import VacationStatus
from datetime import datetime


class VacationRequest(Base):
    __tablename__ = "vacation_requests"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    days_requested = Column(Integer, nullable=False)

    status = Column(
        Enum(VacationStatus),
        default=VacationStatus.pending,
        nullable=False
    )

    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, nullable=True)

    rejected_at = Column(DateTime, nullable=True)
    rejected_by = Column(Integer, nullable=True)

    cancelled_at = Column(DateTime, nullable=True)
    cancelled_by = Column(Integer, nullable=True)

    employee = relationship("Employee", back_populates="vacation_requests")

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="check_valid_date_range"),
        CheckConstraint("days_requested > 0", name="check_positive_days"),
    )