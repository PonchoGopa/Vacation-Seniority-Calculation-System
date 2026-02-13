from datetime import date


def calculate_proportional_days(
    hire_date: date,
    calculation_date: date,
    first_year_days: int
) -> float:
    """
    Calculate proportional vacation days for employees
    with less than one year of service.
    """

    first_anniversary = hire_date.replace(year=hire_date.year + 1)

    if calculation_date >= first_anniversary:
        return 0.0

    days_worked = (calculation_date - hire_date).days
    total_days_first_year = (first_anniversary - hire_date).days

    proportional = (days_worked / total_days_first_year) * first_year_days

    return round(proportional, 2)
