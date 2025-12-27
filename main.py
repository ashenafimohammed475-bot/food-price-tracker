import os
import csv
from datetime import datetime

FILE = "prices.csv"


def ensure_csv_header():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "item", "price", "category"])

# -------------------------------------------------------
# Choose category
# -------------------------------------------------------


def choose_category():
    categories = ["grains", "food", "household", "drinks", "other"]

    print("\nChoose a category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    while True:
        choice = input("Category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print("Invalid choice. Try again.")


# -------------------------------------------------------
# Validation helpers
# -------------------------------------------------------
def get_valid_item():
    while True:
        item = input("Item: ").strip().lower()
        if not item:
            print("Item name cannot be empty.")
        elif not any(char.isalpha() for char in item):
            print("Item name must contain letters.")
        else:
            return item


def get_valid_price():
    while True:
        try:
            price = float(input("Price today: ").strip())
            if price <= 0:
                raise ValueError
            return price
        except ValueError:
            print("Please enter a positive number.")


# -------------------------------------------------------
# Get last price of an item
# -------------------------------------------------------
def get_last_price(item):
    last_price = None

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for date, saved_item, price, category in reader:
                if saved_item == item:
                    last_price = float(price)
    except FileNotFoundError:
        pass

    return last_price


# -------------------------------------------------------
# Add price
# -------------------------------------------------------
def add_price():
    item = get_valid_item()
    category = choose_category()
    price = get_valid_price()

    last_price = get_last_price(item)
    date = datetime.now().strftime("%Y-%m-%d")

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, item, price, category])

    print("\nSaved!")

    if last_price is None:
        print(f"First record for {item}.")
    else:
        diff = price - last_price
        percent = (diff / last_price) * 100

        if diff > 0:
            print(
                f"{item.capitalize()} increased by {diff:.2f} birr (+{percent:.2f}%)")
        elif diff < 0:
            print(
                f"{item.capitalize()} decreased by {abs(diff):.2f} birr ({percent:.2f}%)")
        else:
            print(f"{item.capitalize()} has no change.")


# -------------------------------------------------------
# Category report
# -------------------------------------------------------
def category_report():
    category = choose_category()
    prices = []

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for date, item, price, saved_category in reader:
                if saved_category == category:
                    prices.append(float(price))
    except FileNotFoundError:
        print("No data found.")
        return

    if not prices:
        print("No records for this category.")
        return

    print("\n--- Category Report ---")
    print(f"Category: {category}")
    print(f"Records: {len(prices)}")
    print(f"Average: {sum(prices) / len(prices):.2f} birr")
    print(f"Highest: {max(prices):.2f} birr")
    print(f"Lowest: {min(prices):.2f} birr")


# -------------------------------------------------------
# Item trend
# -------------------------------------------------------
def item_trend():
    item = input("Item name (e.g. rice): ").strip().lower()
    records = []

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for date, saved_item, price, category in reader:
                if saved_item == item:
                    records.append((date, float(price)))
    except FileNotFoundError:
        print("No data found.")
        return

    if len(records) < 2:
        print(f"Not enough data to show trend for '{item}'.")
        return

    records.sort()
    first_date, first_price = records[0]
    last_date, last_price = records[-1]

    change = last_price - first_price
    percent = (change / first_price) * 100

    print("\n--- Price Trend ---")
    print(f"{item.capitalize()}: {first_date} → {last_date}")
    print(f"Start: {first_price:.2f} birr")
    print(f"Latest: {last_price:.2f} birr")

    if change > 0:
        print(f"📈 Increased by {change:.2f} birr (+{percent:.2f}%)")
    elif change < 0:
        print(f"📉 Decreased by {abs(change):.2f} birr ({percent:.2f}%)")
    else:
        print("No price change.")


# -------------------------------------------------------
# Main menu
# -------------------------------------------------------
def main():
    ensure_csv_header()
    while True:
        print("\n--- Food Price Tracker ---")
        print("1. Add price")
        print("2. View category report")
        print("3. View item trend")
        print("4. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_price()
        elif choice == "2":
            category_report()
        elif choice == "3":
            item_trend()
        elif choice == "4":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
