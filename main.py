import csv
from datetime import datetime

FILE = "prices.csv"


# -------------------------------------------------------
# Choose category (fixed list)
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
        else:
            print("Invalid choice. Try again.")


def category_summary():
    category = choose_category()
    items = {}

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for row in reader:
                date, item, price, saved_category = row

                if saved_category == category:
                    items[item] = float(price)

    except FileNotFoundError:
        print("No data found.")
        return

    if not items:
        print(f"\nNo items found in category '{category}'.")
        return

    print(f"\nCategory: {category}")
    for item, price in items.items():
        print(f"{item:<12} → {price} birr")


# -------------------------------------------------------
# Get last price of an item
# -------------------------------------------------------
def get_last_price(item):
    last_price = None

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for row in reader:
                date, saved_item, saved_price, saved_category = row
                if saved_item == item:
                    last_price = float(saved_price)
    except FileNotFoundError:
        return None

    return last_price


def get_valid_item():
    while True:
        item = input("Item: ").strip().lower()

        if not item:
            print("Item name cannot be empty.")
            continue

        if not any(char.isalpha() for char in item):
            print("Item name must contain letters.")
            continue

        return item


def get_valid_price():
    while True:
        price_input = input("Price today: ").strip()
        try:
            price = float(price_input)
            if price <= 0:
                raise ValueError
            return price
        except ValueError:
            print("Please enter a positive number for the price.")


# -------------------------------------------------------
# Add a price
#

while True:
    item = input("Item: ").strip().lower()

    if not item:
        print("Item name cannot be empty.")
        continue

    if not any(char.isalpha() for char in item):
        print("Item name must contain letters.")
        continue

    break

    # Category selection
    category = choose_category()

    # Price validation
while True:
    price_input = input("Price today: ").strip()
    try:
        price = float(price_input)
        if price <= 0:
            raise ValueError
        break
    except ValueError:
        print("Please enter a positive number for the price.")

    # Get last price
    last_price = get_last_price(item)

    # Save date
    date = datetime.now().strftime("%Y-%m-%d")

    # Write to CSV
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, item, price, category])

    print("Saved!")

    # Compare prices
    if last_price is None:
        print(f"First record for {item}.")
    else:
        diff = price - last_price
        percent = (diff / last_price) * 100

        if diff > 0:
            print(
                f"{item.capitalize()} increased by {diff:.2f} birr (+{percent:.2f}%).")
        elif diff < 0:
            print(
                f"{item.capitalize()} decreased by {abs(diff):.2f} birr ({percent:.2f}%).")
        else:
            print(f"{item.capitalize()} has no change since last entry.")


# -------------------------------------------------------
# View recent entries
# -------------------------------------------------------
def view_report():
    data = []

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print("No data yet.")
        return

    if not data:
        print("No data yet.")
        return

    print("\nRecent Entries:")
    for date, item, price, category in data[-5:]:
        print(f"{date} | {item} | {price} | {category}")


# -------------------------------------------------------
# Main menu
# -------------------------------------------------------
def main():
    while True:
        print("\n--- Food Price Tracker ---")
        print("1. Add price")
        print("2. View category summary")
        print("3. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_price()
        elif choice == "2":
            category_summary()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# -------------------------------------------------------
# Start program
# -------------------------------------------------------


def search_by_category():
    category = choose_category()
    found = False

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            print(f"\nResults for category: {category}")
            print("-" * 40)

            for date, item, price, saved_category in reader:
                if saved_category == category:
                    print(f"{date} | {item} | {price}")
                    found = True

    except FileNotFoundError:
        print("No data found.")
        return

    if not found:
        print("No items found in this category.")


def category_summary():
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
        print("No data for this category.")
        return

    print(f"\nCategory: {category}")
    print(f"Items tracked: {len(prices)}")
    print(f"Average price: {sum(prices) / len(prices):.2f} birr")
    print(f"Highest price: {max(prices):.2f} birr")
    print(f"Lowest price: {min(prices):.2f} birr")


if __name__ == "__main__":
    main()
