from abc import ABC, abstractmethod
from typing import List
from faker import Faker
import random


class Employee(ABC):
    def __init__(self, id_code: int, name: str, surname: str):
        self.id_code = id_code
        self.name = name
        self.surname = surname

    @abstractmethod
    def calculate_monthly_salary(self) -> float:
        pass

    @abstractmethod
    def calculate_taxes(self) -> float:
        pass


class HourlyEmployee(Employee):
    def __init__(self, id_code: int, name: str, surname: str, hourly_rate: float, hours_worked: int = 160):
        super().__init__(id_code, name, surname)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_monthly_salary(self) -> float:
        return self.hours_worked * self.hourly_rate

    def calculate_taxes(self) -> float:
        salary = self.calculate_monthly_salary()
        return salary * 0.18 + salary * 0.015


class FixedSalaryEmployee(Employee):
    def __init__(self, id_code: int, name: str, surname: str, fixed_salary: float):
        super().__init__(id_code, name, surname)
        self.fixed_salary = fixed_salary

    def calculate_monthly_salary(self) -> float:
        return self.fixed_salary

    def calculate_taxes(self) -> float:
        salary = self.calculate_monthly_salary()
        return salary * 0.18 + salary * 0.015


class FreelanceHourlyEmployee(Employee):
    def __init__(self, id_code: int, name: str, surname: str, hourly_rate: float, hours_worked: int = 160):
        super().__init__(id_code, name, surname)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_monthly_salary(self) -> float:
        return self.hours_worked * self.hourly_rate * 1.10

    def calculate_taxes(self) -> float:
        salary = self.calculate_monthly_salary()
        return salary * 0.05 + 1760


class SelfEmployedEmployee(Employee):
    def __init__(self, id_code: int, name: str, surname: str, rate_per_line: float, lines_written: int):
        super().__init__(id_code, name, surname)
        self.rate_per_line = rate_per_line
        self.lines_written = lines_written

    def calculate_monthly_salary(self) -> float:
        return self.rate_per_line * self.lines_written

    def calculate_taxes(self) -> float:
        salary = self.calculate_monthly_salary()
        return salary * 0.18 + salary * 0.015 + 1760


faker = Faker()


def generate_employees(num_employees: int) -> List[Employee]:
    employees = []
    for _ in range(num_employees):
        id_code = faker.random_number(digits=6, fix_len=True)
        name = faker.first_name()
        surname = faker.last_name()
        employee_type = random.choice([HourlyEmployee, FixedSalaryEmployee,
                                       FreelanceHourlyEmployee, SelfEmployedEmployee])

        if employee_type == HourlyEmployee:
            employees.append(HourlyEmployee(id_code, name, surname, random.randint(50, 200),
                                            random.randint(80, 200)))

        elif employee_type == FixedSalaryEmployee:
            employees.append(FixedSalaryEmployee(id_code, name, surname, random.randint(20000, 80000)))

        elif employee_type == FreelanceHourlyEmployee:
            employees.append(FreelanceHourlyEmployee(id_code, name, surname, random.randint(50, 200),
                                                     random.randint(80, 200)))

        elif employee_type == SelfEmployedEmployee:
            employees.append(SelfEmployedEmployee(id_code, name, surname, random.randint(10, 50),
                                                  random.randint(500, 3000)))
    return employees


def main():
    employees = generate_employees(10)
    employees.sort(key=lambda e: (-e.calculate_monthly_salary(), e.surname, e.name))

    print(f"{'ID':<10}{'Name':<15}{'Surname':<20}{'Salary':<14}{'Taxes':<10}")
    print("-" * 65)
    for employee in employees:
        print(f"{employee.id_code:<10}{employee.name:<15}{employee.surname:<20}"
              f"{employee.calculate_monthly_salary():<12.2f}{employee.calculate_taxes():<10.2f}")


if __name__ == "__main__":
    main()
