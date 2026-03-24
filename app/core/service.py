from datetime import date
from app.core.seniority import calculate_seniority
from app.core.bonus import calculate_vacation_bonus


def calculate_vacation_bonus_for_employee(
    hire_date: date,
    calculation_date: date,
    daily_salary: float,
    vacation_days: float,
    bonus_percentage: float
) -> dict:
    """
    Calcula la prima vacacional de un empleado dado sus días
    de vacaciones ya resueltos y su salario diario.
    """
    seniority = calculate_seniority(hire_date, calculation_date)

    bonus = calculate_vacation_bonus(
        vacation_days,
        daily_salary,
        bonus_percentage
    )

    return {
        "years_completed": seniority["years_completed"],
        "total_days_worked": seniority["total_days"],
        "vacation_days": vacation_days,
        "bonus_amount": bonus
    }
