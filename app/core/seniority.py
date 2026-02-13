from datetime import date

def calculate_seniority(hire_date: date, calculation_date: date = None):
    if calculation_date is None:
        calculation_date = date.today()

    if hire_date > calculation_date:
        raise ValueError("Hire date cannot be in the future.")

    total_days = (calculation_date - hire_date).days

    years_completed = calculation_date.year - hire_date.year

    # Ajuste si aún no ha llegado el aniversario
    anniversary_passed = (
        (calculation_date.month, calculation_date.day) >=
        (hire_date.month, hire_date.day)
    )

    if not anniversary_passed:
        years_completed -= 1

    return {
        "total_days": total_days,
        "years_completed": years_completed
    }
