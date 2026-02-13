def get_vacation_days(years_completed: int, policy: list[dict]) -> int:
    """
    Determine vacation days based on company policy rules.
    """

    if years_completed < 1:
        return 0

    for rule in policy:
        if rule["min_year"] <= years_completed <= rule["max_year"]:
            return rule["days"]

    raise ValueError("No vacation rule defined for this seniority range.")
