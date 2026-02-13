from app.core.seniority import calculate_seniority
from app.core.vacation_policy import get_vacation_days
from app.core.proportional import calculate_proportional_days
from app.core.bonus import calculate_vacation_bonus


def calculate_employee_vacation(
    hire_date,
    calculation_date,
    daily_salary,
    policy,
    bonus_percentage
):
    seniority = calculate_seniority(hire_date, calculation_date)

    years_completed = seniority["years_completed"]

    vacation_days = get_vacation_days(years_completed, policy)

    proportional_days = 0.0
    if years_completed == 0:
        first_year_days = policy[0]["days"]
        proportional_days = calculate_proportional_days(
            hire_date,
            calculation_date,
            first_year_days
        )

    effective_days = vacation_days if years_completed > 0 else proportional_days

    bonus = calculate_vacation_bonus(
        effective_days,
        daily_salary,
        bonus_percentage
    )

    return {
        "years_completed": years_completed,
        "total_days_worked": seniority["total_days"],
        "vacation_days": effective_days,
        "bonus_amount": bonus
    }
