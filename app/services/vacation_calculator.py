from datetime import date
from typing import List


class VacationCalculationError(Exception):
    pass


def calculate_years_of_service(hire_date: date) -> int:
    if hire_date is None:
        raise VacationCalculationError("Employee hire_date is required")

    today = date.today()
    years = today.year - hire_date.year

    if (today.month, today.day) < (hire_date.month, hire_date.day):
        years -= 1

    return max(years, 0)


def resolve_vacation_days_for_year(years_of_service: int, policy_rules: List) -> int:
    if not policy_rules:
        raise VacationCalculationError("No vacation policy rules configured")

    sorted_rules = sorted(policy_rules, key=lambda r: r.years_required)

    applicable_days = 0

    for rule in sorted_rules:
        if years_of_service >= rule.years_required:
            applicable_days = rule.vacation_days
        else:
            break

    return applicable_days


def calculate_proportional_days_from_rules(
    hire_date: date,
    policy_rules: List
) -> float:
    """
    Para empleados con menos de 1 año, calcula días proporcionales
    basado en la primera regla de la política.
    """
    if not policy_rules:
        raise VacationCalculationError("No vacation policy rules configured")

    sorted_rules = sorted(policy_rules, key=lambda r: r.years_required)
    first_year_days = sorted_rules[0].vacation_days

    today = date.today()
    first_anniversary = hire_date.replace(year=hire_date.year + 1)

    days_worked = (today - hire_date).days
    total_days_first_year = (first_anniversary - hire_date).days

    proportional = (days_worked / total_days_first_year) * first_year_days

    return round(proportional, 2)


def calculate_total_entitled_days(hire_date: date, policy_rules: List) -> float:
    """
    Calcula todos los días acumulados desde el inicio laboral hasta hoy.
    Incluye días proporcionales si el empleado tiene menos de 1 año.
    """
    years_of_service = calculate_years_of_service(hire_date)

    if years_of_service == 0:
        return calculate_proportional_days_from_rules(hire_date, policy_rules)

    total_days = 0
    for year in range(1, years_of_service + 1):
        days_for_year = resolve_vacation_days_for_year(year, policy_rules)
        total_days += days_for_year

    return total_days


def calculate_vacation_balance(employee, policy_rules: List, days_used: int) -> dict:
    if employee is None:
        raise VacationCalculationError("Employee is required")

    if days_used < 0:
        raise VacationCalculationError("days_used cannot be negative")

    total_entitled = calculate_total_entitled_days(
        employee.hire_date,
        policy_rules
    )

    remaining_balance = total_entitled - days_used

    return {
        "employee_id": employee.id,
        "years_of_service": calculate_years_of_service(employee.hire_date),
        "total_days_entitled": total_entitled,
        "days_used": days_used,
        "remaining_balance": max(remaining_balance, 0)
    }