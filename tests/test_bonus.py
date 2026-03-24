import pytest
from app.core.bonus import calculate_vacation_bonus


def test_bonus_basic_calculation():
    """Cálculo básico: 12 días * $500 * 25% = $1,500"""
    result = calculate_vacation_bonus(
        vacation_days=12,
        daily_salary=500.0,
        bonus_percentage=0.25
    )
    assert result == 1500.0


def test_bonus_different_percentage():
    """Cálculo con porcentaje distinto al estándar"""
    result = calculate_vacation_bonus(
        vacation_days=12,
        daily_salary=500.0,
        bonus_percentage=0.50
    )
    assert result == 3000.0


def test_bonus_zero_days():
    """Con 0 días de vacaciones el bono debe ser 0"""
    result = calculate_vacation_bonus(
        vacation_days=0,
        daily_salary=500.0,
        bonus_percentage=0.25
    )
    assert result == 0.0


def test_bonus_zero_salary():
    """Con salario 0 el bono debe ser 0"""
    result = calculate_vacation_bonus(
        vacation_days=12,
        daily_salary=0.0,
        bonus_percentage=0.25
    )
    assert result == 0.0


def test_bonus_rounds_to_two_decimals():
    """El resultado debe estar redondeado a 2 decimales"""
    result = calculate_vacation_bonus(
        vacation_days=7,
        daily_salary=333.33,
        bonus_percentage=0.25
    )
    assert result == round(7 * 333.33 * 0.25, 2)


def test_bonus_high_seniority():
    """Empleado con 30 días de vacaciones y salario alto"""
    result = calculate_vacation_bonus(
        vacation_days=30,
        daily_salary=1500.0,
        bonus_percentage=0.25
    )
    assert result == 11250.0


def test_bonus_proportional_days():
    """Funciona correctamente con días proporcionales (float)"""
    result = calculate_vacation_bonus(
        vacation_days=6.5,
        daily_salary=500.0,
        bonus_percentage=0.25
    )
    assert result == round(6.5 * 500.0 * 0.25, 2)