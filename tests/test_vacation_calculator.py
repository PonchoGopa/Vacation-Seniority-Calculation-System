import pytest
from datetime import date
from unittest.mock import MagicMock
from app.services.vacation_calculator import (
    calculate_years_of_service,
    resolve_vacation_days_for_year,
    calculate_total_entitled_days,
    calculate_vacation_balance,
    VacationCalculationError
)


# --- Helpers ---

def make_rule(years_required, vacation_days):
    """Crea una regla mock para no depender de la DB"""
    rule = MagicMock()
    rule.years_required = years_required
    rule.vacation_days = vacation_days
    return rule


def make_employee(hire_date, employee_id=1):
    """Crea un empleado mock para no depender de la DB"""
    employee = MagicMock()
    employee.id = employee_id
    employee.hire_date = hire_date
    return employee


RULES = [
    make_rule(1, 12),
    make_rule(2, 14),
    make_rule(3, 16),
    make_rule(4, 18),
    make_rule(5, 20),
    make_rule(6, 22),
    make_rule(11, 24),
    make_rule(16, 26),
    make_rule(21, 28),
    make_rule(26, 30),
]


# --- Tests de calculate_years_of_service ---

def test_years_of_service_none_hire_date_raises():
    """hire_date None debe lanzar error"""
    with pytest.raises(VacationCalculationError):
        calculate_years_of_service(None)


def test_years_of_service_new_employee():
    """Empleado recién contratado debe tener 0 años"""
    result = calculate_years_of_service(date.today())
    assert result == 0


def test_years_of_service_returns_non_negative():
    """El resultado nunca debe ser negativo"""
    result = calculate_years_of_service(date.today())
    assert result >= 0


# --- Tests de resolve_vacation_days_for_year ---

def test_resolve_days_first_year():
    """1 año debe resolver 12 días"""
    assert resolve_vacation_days_for_year(1, RULES) == 12


def test_resolve_days_third_year():
    """3 años debe resolver 16 días"""
    assert resolve_vacation_days_for_year(3, RULES) == 16


def test_resolve_days_no_rules_raises():
    """Sin reglas debe lanzar error"""
    with pytest.raises(VacationCalculationError):
        resolve_vacation_days_for_year(1, [])


def test_resolve_days_zero_years():
    """0 años debe regresar 0 días"""
    assert resolve_vacation_days_for_year(0, RULES) == 0


# --- Tests de calculate_total_entitled_days ---

def test_total_entitled_one_year():
    """1 año completo debe acumular 12 días"""
    hire_date = date(date.today().year - 1, date.today().month, date.today().day)
    result = calculate_total_entitled_days(hire_date, RULES)
    assert result == 12


def test_total_entitled_two_years():
    """2 años completos debe acumular 12 + 14 = 26 días"""
    hire_date = date(date.today().year - 2, date.today().month, date.today().day)
    result = calculate_total_entitled_days(hire_date, RULES)
    assert result == 26


def test_total_entitled_three_years():
    """3 años completos debe acumular 12 + 14 + 16 = 42 días"""
    hire_date = date(date.today().year - 3, date.today().month, date.today().day)
    result = calculate_total_entitled_days(hire_date, RULES)
    assert result == 42


# --- Tests de calculate_vacation_balance ---

def test_balance_no_days_used():
    """Sin días usados el balance debe ser igual al total"""
    hire_date = date(date.today().year - 1, date.today().month, date.today().day)
    employee = make_employee(hire_date)

    result = calculate_vacation_balance(employee, RULES, days_used=0)

    assert result["days_used"] == 0
    assert result["total_days_entitled"] == 12
    assert result["remaining_balance"] == 12


def test_balance_with_days_used():
    """Con días usados el balance debe restar correctamente"""
    hire_date = date(date.today().year - 1, date.today().month, date.today().day)
    employee = make_employee(hire_date)

    result = calculate_vacation_balance(employee, RULES, days_used=5)

    assert result["days_used"] == 5
    assert result["remaining_balance"] == 7


def test_balance_never_negative():
    """El balance nunca debe ser negativo aunque se excedan los días"""
    hire_date = date(date.today().year - 1, date.today().month, date.today().day)
    employee = make_employee(hire_date)

    result = calculate_vacation_balance(employee, RULES, days_used=999)

    assert result["remaining_balance"] == 0


def test_balance_none_employee_raises():
    """Employee None debe lanzar error"""
    with pytest.raises(VacationCalculationError):
        calculate_vacation_balance(None, RULES, days_used=0)


def test_balance_negative_days_used_raises():
    """Días usados negativos debe lanzar error"""
    hire_date = date(date.today().year - 1, date.today().month, date.today().day)
    employee = make_employee(hire_date)

    with pytest.raises(VacationCalculationError):
        calculate_vacation_balance(employee, RULES, days_used=-1)


def test_balance_returns_correct_structure():
    """La respuesta debe tener todas las claves esperadas"""
    hire_date = date(date.today().year - 1, date.today().month, date.today().day)
    employee = make_employee(hire_date)

    result = calculate_vacation_balance(employee, RULES, days_used=0)

    assert "employee_id" in result
    assert "years_of_service" in result
    assert "total_days_entitled" in result
    assert "days_used" in result
    assert "remaining_balance" in result