from datetime import date

def calculate_vacation_balance(employee, policy_rules):
    years = calculate_years_of_service(employee.hire_date)
    days = resolve_vacation_days(years, policy_rules)

    return {
        "employee_id": employee.id,
        "years_of_service": years,
        "vacation_days_entitled": days
    }
calculate_years_of_service()
resolve_vacation_days()
calculate_vacation_balance()