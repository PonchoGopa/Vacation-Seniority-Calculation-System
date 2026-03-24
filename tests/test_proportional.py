from datetime import date
from app.core.proportional import calculate_proportional_days


def test_proportional_half_year():
    """A mitad del primer año debe dar aproximadamente la mitad de los días"""
    hire_date = date(2024, 1, 1)
    calculation_date = date(2024, 7, 1)
    result = calculate_proportional_days(hire_date, calculation_date, 12)

    assert 5.5 <= result <= 6.5


def test_proportional_first_day():
    """El primer día de trabajo debe dar 0 días proporcionales"""
    hire_date = date(2024, 1, 1)
    calculation_date = date(2024, 1, 1)
    result = calculate_proportional_days(hire_date, calculation_date, 12)

    assert result == 0.0


def test_proportional_one_day_before_anniversary():
    """Un día antes del aniversario debe dar casi los días completos"""
    hire_date = date(2024, 1, 1)
    calculation_date = date(2024, 12, 31)
    result = calculate_proportional_days(hire_date, calculation_date, 12)

    assert result > 11.0
    assert result < 12.0


def test_proportional_returns_zero_after_anniversary():
    """Después del primer aniversario debe regresar 0"""
    hire_date = date(2023, 1, 1)
    calculation_date = date(2024, 6, 1)
    result = calculate_proportional_days(hire_date, calculation_date, 12)

    assert result == 0.0


def test_proportional_three_months():
    """A los 3 meses debe dar aproximadamente una cuarta parte"""
    hire_date = date(2024, 1, 1)
    calculation_date = date(2024, 4, 1)
    result = calculate_proportional_days(hire_date, calculation_date, 12)

    assert 2.5 <= result <= 3.5


def test_proportional_respects_first_year_days():
    """El cálculo debe escalar correctamente con distintos días base"""
    hire_date = date(2024, 1, 1)
    calculation_date = date(2024, 7, 1)

    result_12 = calculate_proportional_days(hire_date, calculation_date, 12)
    result_24 = calculate_proportional_days(hire_date, calculation_date, 24)

    assert round(result_24, 1) == round(result_12 * 2, 1)

