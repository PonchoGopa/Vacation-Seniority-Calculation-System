from datetime import date, timedelta


def calculate_business_days(start_date: date, end_date: date) -> int:
    """
    Calcula días laborales (lunes a viernes) entre dos fechas inclusive.
    """

    if end_date < start_date:
        raise ValueError("end_date cannot be before start_date")

    total_days = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:  # 0=Monday, 6=Sunday
            total_days += 1
        current_date += timedelta(days=1)

    return total_days