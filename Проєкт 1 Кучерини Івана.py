import json
import os
from datetime import datetime

DATA_FILE = "finance_data.json"

def load_data():
    """Завантажує дані з JSON файлу або створює нові."""
    if not os.path.exists(DATA_FILE):
        return {"budget": 0.0, "expenses": []}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    """Зберігає дані у JSON файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ===============================
# ОСНОВНІ ФУНКЦІЇ БОТА
# ===============================

def show_help():
    """Виводить список команд."""
    print("\nДоступні команди:")
    print("допомога")
    print("встановити бюджет")
    print("додати витрату")
    print("показати витрати")
    print("витрати за дату")
    print("витрати за період")
    print("витрати за категорією")
    print("залишок")
    print("звіт за категоріями")
    print("вийти\n")


def set_budget(data):
    """Встановлює бюджет."""
    try:
        amount = float(input("Введіть суму бюджету: "))
        data["budget"] = amount
        save_data(data)
        print("Бюджет встановлено.")
    except ValueError:
        print("Помилка! Введіть коректне число.")


def add_expense(data):
    """Додає нову витрату."""
    try:
        amount = float(input("Сума: "))
        category = input("Категорія: ")
        date = input("Дата (YYYY-MM-DD): ")

        # Перевірка формату дати
        datetime.strptime(date, "%Y-%m-%d")

        expense = {
            "amount": amount,
            "category": category,
            "date": date
        }

        data["expenses"].append(expense)
        save_data(data)

        print("Витрату додано.")
        check_budget(data)

    except ValueError:
        print("Помилка! Перевірте правильність введених даних.")


def show_expenses(data):
    """Показує всі витрати."""
    if not data["expenses"]:
        print("Список витрат порожній.")
        return

    for i, exp in enumerate(data["expenses"], start=1):
        print(f"{i}. {exp['date']} | {exp['category']} | {exp['amount']} грн")


def expenses_by_date(data):
    """Показує витрати за конкретну дату."""
    date = input("Введіть дату (YYYY-MM-DD): ")

    found = False
    for exp in data["expenses"]:
        if exp["date"] == date:
            print(f"{exp['date']} | {exp['category']} | {exp['amount']} грн")
            found = True

    if not found:
        print("Витрат за цю дату не знайдено.")


def expenses_by_period(data):
    """Показує витрати за період між двома датами."""
    try:
        start_date = datetime.strptime(input("Початкова дата (YYYY-MM-DD): "), "%Y-%m-%d")
        end_date = datetime.strptime(input("Кінцева дата (YYYY-MM-DD): "), "%Y-%m-%d")

        found = False
        for exp in data["expenses"]:
            exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
            if start_date <= exp_date <= end_date:
                print(f"{exp['date']} | {exp['category']} | {exp['amount']} грн")
                found = True

        if not found:
            print("Витрат за цей період не знайдено.")

    except ValueError:
        print("Неправильний формат дати.")


def expenses_by_category(data):
    """Показує витрати за категорією."""
    category = input("Введіть категорію: ")

    found = False
    for exp in data["expenses"]:
        if exp["category"].lower() == category.lower():
            print(f"{exp['date']} | {exp['category']} | {exp['amount']} грн")
            found = True

    if not found:
        print("Витрат у цій категорії не знайдено.")


def calculate_total_expenses(data):
    """Обчислює загальну суму витрат."""
    return sum(exp["amount"] for exp in data["expenses"])


def show_balance(data):
    """Показує залишок бюджету."""
    total = calculate_total_expenses(data)
    balance = data["budget"] - total
    print(f"Залишок бюджету: {balance} грн")


def check_budget(data):
    """Перевіряє перевищення бюджету."""
    total = calculate_total_expenses(data)
    if total > data["budget"]:
        print("УВАГА! Бюджет перевищено!")
    else:
        print(f"Поточні витрати: {total} грн з {data['budget']} грн")


def report_by_category(data):
    """Звіт по категоріях."""
    report = {}

    for exp in data["expenses"]:
        category = exp["category"]
        report[category] = report.get(category, 0) + exp["amount"]

    if not report:
        print("Немає витрат для формування звіту.")
        return

    print("\nЗвіт за категоріями:")
    for category, total in report.items():
        print(f"{category}: {total} грн")


# ===============================
# ГОЛОВНА ФУНКЦІЯ
# ===============================

def main():
    data = load_data()

    print("Вітаємо у боті 'Фінансовий трекер студента'!")
    print("Введіть 'допомога' для перегляду команд.")

    while True:
        command = input("\nВведіть команду: ").lower()

        if command == "допомога":
            show_help()
        elif command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data)
        elif command == "витрати за дату":
            expenses_by_date(data)
        elif command == "витрати за період":
            expenses_by_period(data)
        elif command == "витрати за категорією":
            expenses_by_category(data)
        elif command == "залишок":
            show_balance(data)
        elif command == "звіт за категоріями":
            report_by_category(data)
        elif command == "вийти":
            print("До побачення!")
            break
        else:
            print("Невідома команда. Введіть 'допомога'.")


if __name__ == "__main__":
    main()