import os
import csv
from datetime import datetime

FILE = "applications.csv"


def add_application():
    print("\n--- Add New Application ---")

    # Company name
    while True:
        company = input("Company name: ").strip()
        if company:
            break
        print("Company name cannot be empty.")

    # Position
    while True:
        position = input("Position: ").strip()
        if position:
            break
        print("Position cannot be empty.")

    # Status selection
    statuses = ["applied", "interview", "rejected", "offer"]
    print("\nApplication status:")
    for i, status in enumerate(statuses, start=1):
        print(f"{i}. {status}")

    while True:
        choice = input("Choose status number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(statuses):
            status = statuses[int(choice) - 1]
            break
        print("Invalid choice. Try again.")

    # Notes (optional)
    notes = input("Notes (optional): ").strip()

    # Date
    date = datetime.now().strftime("%Y-%m-%d")

    # Save to CSV
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, company, position, status, notes])

    print("\n✅ Application saved successfully!")


def view_applications():
    print("\n--- All Job Applications ---")

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            rows = list(reader)

    except FileNotFoundError:
        print("No applications found yet.")
        return

    if not rows:
        print("No applications found yet.")
        return

    print(f"\n{'Date':<12} | {'Company':<20} | {'Position':<20} | {'Status':<10}")
    print("-" * 70)

    for date, company, position, status, notes in rows:
        print(f"{date:<12} | {company:<20} | {position:<20} | {status:<10}")


def search_by_status():
    statuses = ["applied", "interview", "rejected", "offer"]

    print("\nSearch applications by status:")
    for i, status in enumerate(statuses, start=1):
        print(f"{i}. {status}")

    while True:
        choice = input("Choose status number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(statuses):
            selected_status = statuses[int(choice) - 1]
            break
        print("Invalid choice. Try again.")

    found = False

    try:
        with open(FILE) as f:
            reader = csv.reader(f)

            print(f"\n--- Applications with status: {selected_status} ---")
            print(f"{'Date':<12} | {'Company':<20} | {'Position':<20}")
            print("-" * 60)

            for date, company, position, status, notes in reader:
                if status == selected_status:
                    print(f"{date:<12} | {company:<20} | {position:<20}")
                    found = True

    except FileNotFoundError:
        print("No applications found.")
        return

    if not found:
        print("No applications match this status.")


def summary():
    statuses = ["applied", "interview", "rejected", "offer"]
    counts = {status: 0 for status in statuses}
    total = 0

    try:
        with open(FILE) as f:
            reader = csv.reader(f)
            for date, company, position, status, notes in reader:
                total += 1
                if status in counts:
                    counts[status] += 1

    except FileNotFoundError:
        print("No applications found yet.")
        return

    if total == 0:
        print("No applications found yet.")
        return

    print("\n--- Application Summary ---")
    print(f"Total applications: {total}\n")

    for status in statuses:
        print(f"{status.capitalize():<10}: {counts[status]}")

    print("---------------------------")


def ensure_csv_header():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "date",
                "company",
                "position",
                "status",
                "notes"
            ])


def main():
    ensure_csv_header()
    while True:
        print("\n--- Job Application Tracker ---")
        print("1. Add new application")
        print("2. View all applications")
        print("3. Search by status")
        print("4. View summary")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            if choice == "1":
                add_application()
        elif choice == "2":
            view_applications()

        elif choice == "3":
            search_by_status()
        elif choice == "4":
            summary()
        elif choice == "5":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
