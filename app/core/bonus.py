def calculate_vacation_bonus(
    vacation_days: float,
    daily_salary: float,
    bonus_percentage: float
) -> float:
    """
    Calculate vacation bonus (prima vacacional).
    """

    return round(vacation_days * daily_salary * bonus_percentage, 2)
