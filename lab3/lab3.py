from decimal import Decimal


initial_amount = Decimal(input("Введіть початкову суму депозиту: "))
annual_interest_rate = Decimal(input("Введіть річну відсоткову ставку (%): "))
deposit_term = 2

monthly_interest_rate = annual_interest_rate / Decimal(12) / Decimal(100)

current_balance = initial_amount
print("\nМісяць | Баланс на рахунку")
print("---------------------------")

for month in range(1, deposit_term * 12 + 1):
    current_balance += current_balance * monthly_interest_rate
    print(f"{month:6} | {current_balance:,.2f} грн")

print(f"\nСума на рахунку після {deposit_term} років: {current_balance:,.2f} грн")
