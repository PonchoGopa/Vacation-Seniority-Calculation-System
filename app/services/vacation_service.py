from datetime import date
from app.models.employee import Employee


def calculate_seniority_years(employee: Employee) -> int:
    today = date.today()
    years = today.year - employee.hire_date.year

    # Ajuste si aún no cumple aniversario este año
    if (today.month, today.day) < (employee.hire_date.month, employee.hire_date.day):
        years -= 1

    return max(years, 0)