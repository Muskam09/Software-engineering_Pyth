import pytest
from lab8 import (
    HourlyEmployee, FixedSalaryEmployee, FreelanceHourlyEmployee, SelfEmployedEmployee
)

@pytest.mark.parametrize(
    "employee_class, kwargs, expected_salary, expected_taxes",
    [
        # Hourly Employee (погодинна ставка)
        (HourlyEmployee, {"id_code": 1, "name": "John", "surname": "Smith", "hourly_rate": 100, "hours_worked": 160},
         16000, 16000 * 0.18 + 16000 * 0.015),

        # Fixed Salary Employee (фіксована ставка)
        (FixedSalaryEmployee, {"id_code": 2, "name": "Alice", "surname": "Johnson", "fixed_salary": 50000},
         50000, 50000 * 0.18 + 50000 * 0.015),

        # Freelance Hourly Employee (ФОП, бонус +10%)
        (FreelanceHourlyEmployee, {"id_code": 3, "name": "Emma", "surname": "Brown", "hourly_rate": 120, "hours_worked": 150},
         150 * 120 * 1.10, (150 * 120 * 1.10) * 0.05 + 1760),

        # Self-Employed Employee (оплата за рядки)
        (SelfEmployedEmployee, {"id_code": 4, "name": "Daniel", "surname": "Taylor", "rate_per_line": 20, "lines_written": 1000},
         20 * 1000, (20 * 1000) * 0.18 + (20 * 1000) * 0.015 + 1760),
    ]
)
def test_employee_salary_and_taxes(employee_class, kwargs, expected_salary, expected_taxes):
    employee = employee_class(**kwargs)
    assert employee.calculate_monthly_salary() == pytest.approx(expected_salary, 0.01)
    assert employee.calculate_taxes() == pytest.approx(expected_taxes, 0.01)

@pytest.mark.parametrize(
    "employees_data, expected_order",
    [
        (
            [
                HourlyEmployee(id_code=1, name="John", surname="Smith", hourly_rate=100, hours_worked=160),  # 16000
                FixedSalaryEmployee(id_code=2, name="Alice", surname="Johnson", fixed_salary=50000),         # 50000
                FreelanceHourlyEmployee(id_code=3, name="Emma", surname="Brown", hourly_rate=120, hours_worked=150),   # 19800
                SelfEmployedEmployee(id_code=4, name="Daniel", surname="Taylor", rate_per_line=20, lines_written=1000),  # 20000
            ],
            ["Johnson", "Taylor", "Brown", "Smith"],
        ),
        (
            [
                HourlyEmployee(id_code=1, name="Alex", surname="Adams", hourly_rate=200, hours_worked=100),  # 20000
                HourlyEmployee(id_code=2, name="Mark", surname="Clark", hourly_rate=200, hours_worked=100),  # 20000
                HourlyEmployee(id_code=3, name="Sophie", surname="Brown", hourly_rate=200, hours_worked=100),  # 20000
            ],
            ["Adams", "Brown", "Clark"],
        ),
    ]
)
def test_employee_sorting(employees_data, expected_order):
    employees_data.sort(key=lambda e: (-e.calculate_monthly_salary(), e.surname, e.name))
    sorted_surnames = [e.surname for e in employees_data]
    assert sorted_surnames == expected_order
