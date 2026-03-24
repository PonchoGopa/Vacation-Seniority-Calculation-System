import pytest
from app.core.vacation_policy import get_vacation_days


POLICY = [
    {"min_year": 1, "max_year": 1, "days": 12},
    {"min_year": 2, "max_year": 2, "days": 14},
    {"min_year": 3, "max_year": 3, "days": 16},
    {"min_year": 4, "max_year": 4, "days": 18},
    {"min_year": 5, "max_year": 5, "days": 20},
    {"min_year": 6, "max_year": 10, "days": 22},
    {"min_year": 11, "max_year": 15, "days": 24},
    {"min_year": 16, "max_year": 20, "days": 26},
    {"min_year": 21, "max_year": 25, "days": 28},
    {"min_year": 26, "max_year": 30, "days": 30},
]


def test_policy_first_year():
    """1 año completo debe dar 12 días"""
    assert get_vacation_days(1, POLICY) == 12


def test_policy_second_year():
    """2 años completos debe dar 14 días"""
    assert get_vacation_days(2, POLICY) == 14


def test_policy_fifth_year():
    """5 años completos debe dar 20 días"""
    assert get_vacation_days(5, POLICY) == 20


def test_policy_range_six_to_ten():
    """Entre 6 y 10 años debe dar 22 días"""
    assert get_vacation_days(6, POLICY) == 22
    assert get_vacation_days(8, POLICY) == 22
    assert get_vacation_days(10, POLICY) == 22


def test_policy_range_eleven_to_fifteen():
    """Entre 11 y 15 años debe dar 24 días"""
    assert get_vacation_days(11, POLICY) == 24
    assert get_vacation_days(15, POLICY) == 24


def test_policy_zero_years_returns_zero():
    """Menos de 1 año completo debe regresar 0"""
    assert get_vacation_days(0, POLICY) == 0


def test_policy_no_rules_raises():
    """Sin reglas debe lanzar error"""
    with pytest.raises(ValueError):
        get_vacation_days(5, [])


def test_policy_out_of_range_raises():
    """Años fuera del rango definido debe lanzar error"""
    with pytest.raises(ValueError):
        get_vacation_days(31, POLICY)

