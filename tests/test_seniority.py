import pytest
from datetime import date
from app.core.seniority import calculate_seniority


def test_seniority_exact_one_year():
    """Empleado que cumple exactamente 1 año hoy"""
    hire_date = date(2024, 3, 24)
    calculation_date = date(2025, 3, 24)
    result = calculate_seniority(hire_date, calculation_date)

    assert result["years_completed"] == 1
    assert result["total_days"] == 365


def test_seniority_three_years():
    """Empleado con 3 años completos"""
    hire_date = date(2021, 1, 1)
    calculation_date = date(2024, 1, 1)
    result = calculate_seniority(hire_date, calculation_date)

    assert result["years_completed"] == 3


def test_seniority_anniversary_not_yet_passed():
    """Empleado que aún no cumple aniversario este año"""
    hire_date = date(2023, 12, 1)
    calculation_date = date(2024, 11, 1)
    result = calculate_seniority(hire_date, calculation_date)

    assert result["years_completed"] == 0


def test_seniority_anniversary_passed_this_year():
    """Empleado que ya pasó su aniversario este año"""
    hire_date = date(2023, 1, 1)
    calculation_date = date(2024, 6, 1)
    result = calculate_seniority(hire_date, calculation_date)

    assert result["years_completed"] == 1


def test_seniority_same_day():
    """Empleado recién contratado"""
    hire_date = date(2024, 3, 24)
    calculation_date = date(2024, 3, 24)
    result = calculate_seniority(hire_date, calculation_date)

    assert result["years_completed"] == 0
    assert result["total_days"] == 0


def test_seniority_future_hire_date_raises():
    """Fecha de contratación en el futuro debe lanzar error"""
    hire_date = date(2027, 1, 1)
    calculation_date = date(2024, 1, 1)

    with pytest.raises(ValueError, match="Hire date cannot be in the future"):
        calculate_seniority(hire_date, calculation_date)


def test_seniority_uses_today_by_default():
    """Sin fecha de cálculo usa today() por defecto"""
    hire_date = date(2020, 1, 1)
    result = calculate_seniority(hire_date)

    assert result["years_completed"] >= 4

