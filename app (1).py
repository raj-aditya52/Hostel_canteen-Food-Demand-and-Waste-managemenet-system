FILE_NAME = "canteen_data.txt"
MEAL_SLOTS = ("Breakfast", "Lunch", "Snacks", "Dinner")
PEAK_SLOTS = ("Lunch", "Dinner")


def get_peak_status(meal):
    if meal in PEAK_SLOTS:
        return "Peak meal time"
    else:
        return "Normal meal time"


def get_advice(demand_pct, waste_pct, wasted):
    if wasted == 0:
        return "INCREASE quantity (finished completely)"
    elif waste_pct >= 35 and demand_pct < 40:
        return "REMOVE from menu"
    elif waste_pct >= 25:
        return "SERVE LESS OFTEN"
    elif waste_pct >= 12:
        return "REDUCE quantity"
    elif demand_pct >= 80:
        return "INCREASE quantity"
    else:
        return "KEEP same"


def make_record(name, meal, present, cooked, eaten):
    wasted = cooked - eaten

    if present > 0:
        demand_pct = round((eaten / present) * 100, 1)
    else:
        demand_pct = 0.0

    waste_pct = round((wasted / cooked) * 100, 1)
    next_qty = round(eaten * 1.05)
    peak = get_peak_status(meal)
    advice = get_advice(demand_pct, waste_pct, wasted)

    return {
        "name": name.strip().title(),
        "meal": meal,
        "peak": peak,
        "present": present,
        "cooked": cooked,
        "eaten": eaten,
        "wasted": wasted,
        "demand_pct": demand_pct,
        "waste_pct": waste_pct,
        "next_qty": next_qty,
        "advice": advice,
    }


def save_to_file(records):
    f = open(FILE_NAME, "w")
    for r in records:
        line = (
            r["name"] + "|"
            + r["meal"] + "|"
            + str(r["present"]) + "|"
            + str(r["cooked"]) + "|"
            + str(r["eaten"]) + "\n"
        )
        f.write(line)
    f.close()
    print("Data saved to " + FILE_NAME)


def load_from_file():
    records = []
    try:
        f = open(FILE_NAME, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            clean = line.strip()
            if clean == "":
                continue
            parts = clean.split("|")
            if len(parts) == 5:
                name = parts[0]
                meal = parts[1]
                present = int(parts[2])
                cooked = int(parts[3])
                eaten = int(parts[4])
                if cooked > 0 and present >= 0 and eaten >= 0 and eaten <= cooked:
                    records.append(make_record(name, meal, present, cooked, eaten))
    except FileNotFoundError:
        records = []
    return records


def show_records(records):
    if len(records) == 0:
        print("No records found.")
        return

    print("\n--- ALL FOOD RECORDS ---")
    i = 1
    for r in records:
        print(
            str(i) + ". " + r["name"] + " (" + r["meal"] + " - " + r["peak"] + ")"
            + " | Cooked: " + str(r["cooked"])
            + " | Eaten: " + str(r["eaten"])
            + " | Wasted: " + str(r["wasted"])
            + " | Demand: " + str(r["demand_pct"]) + "%"
            + " | Waste: " + str(r["waste_pct"]) + "%"
            + " | Next Qty: " + str(r["next_qty"])
            + " | Advice: " + r["advice"]
        )
        i = i + 1


def waste_key(row):
    return row["waste_pct"]


def demand_key(row):
    return row["demand_pct"]


def show_rankings(records):
    if len(records) == 0:
        print("No records to rank.")
        return

    by_waste = sorted(records, key=waste_key, reverse=True)
    print("\n--- RANKED BY WASTE % (HIGH TO LOW) ---")
    for r in by_waste:
        print(r["name"] + " (" + r["meal"] + "): " + str(r["waste_pct"]) + "% waste -> " + r["advice"])

    by_demand = sorted(records, key=demand_key, reverse=True)
    print("\n--- RANKED BY DEMAND % (HIGH TO LOW) ---")
    for r in by_demand:
        print(r["name"] + " (" + r["meal"] + "): " + str(r["demand_pct"]) + "% demand -> Next Qty: " + str(r["next_qty"]))


def show_patterns(records):
    if len(records) == 0:
        print("No data for pattern analysis.")
        return

    print("\n--- SLOT-WISE FOOD PATTERN ANALYSIS ---")

    for slot in MEAL_SLOTS:
        slot_rows = []
        for r in records:
            if r["meal"] == slot:
                slot_rows.append(r)

        if len(slot_rows) == 0:
            continue

        peak_tag = get_peak_status(slot)
        total_waste_pct = 0.0
        total_demand_pct = 0.0
        high_waste_foods = []
        good_foods = []

        for item in slot_rows:
            total_waste_pct = total_waste_pct + item["waste_pct"]
            total_demand_pct = total_demand_pct + item["demand_pct"]

            if item["waste_pct"] >= 12 and item["name"] not in high_waste_foods:
                high_waste_foods.append(item["name"] + " (" + str(item["waste_pct"]) + "%)")

            if (item["wasted"] == 0 or item["demand_pct"] >= 50) and item["name"] not in good_foods:
                good_foods.append(item["name"] + " (" + str(item["demand_pct"]) + "% demand)")

        avg_waste = round(total_waste_pct / len(slot_rows), 1)
        avg_demand = round(total_demand_pct / len(slot_rows), 1)

        print("\n[" + slot + " - " + peak_tag + "]")
        print("Entries in slot: " + str(len(slot_rows)) + " | Avg Demand: " + str(avg_demand) + "% | Avg Waste: " + str(avg_waste) + "%")

        for item in slot_rows:
            print(
                "  * " + item["name"]
                + " -> Demand: " + str(item["demand_pct"]) + "%"
                + ", Waste: " + str(item["waste_pct"]) + "%"
                + " (" + str(item["wasted"]) + " wasted)"
                + " | Suggestion: " + item["advice"]
            )

        if len(high_waste_foods) > 0:
            print("  Slot High-Waste Foods (>=12%): " + ", ".join(high_waste_foods) + " -> Reduce prep in " + slot + ".")
        if len(good_foods) > 0:
            print("  Slot Popular / Low-Waste Foods: " + ", ".join(good_foods) + " -> Maintain stock in " + slot + ".")
        if avg_waste >= 15:
            print("  Slot Pattern Suggestion: Overall waste in " + slot + " is high (" + str(avg_waste) + "%). Cook in smaller batches.")
        else:
            print("  Slot Pattern Suggestion: Overall waste in " + slot + " is under control (" + str(avg_waste) + "%).")


def show_food_details(records):
    if len(records) == 0:
        print("No records available in past history.")
        return

    search_name = input("Enter Food Item Name to inspect: ").strip().lower()
    if search_name == "":
        print("Error: Food name cannot be blank.")
        return

    matched = []
    for r in records:
        if r["name"].lower() == search_name:
            matched.append(r)

    if len(matched) == 0:
        print("No past records found for '" + search_name.title() + "'.")
        return

    total_present = 0
    total_cooked = 0
    total_eaten = 0
    total_wasted = 0
    meals_used = []

    print("\n--- PAST RECORDS FOR " + matched[0]["name"].upper() + " ---")
    idx = 1
    for m in matched:
        total_present = total_present + m["present"]
        total_cooked = total_cooked + m["cooked"]
        total_eaten = total_eaten + m["eaten"]
        total_wasted = total_wasted + m["wasted"]
        if m["meal"] not in meals_used:
            meals_used.append(m["meal"])

        print(
            str(idx) + ". Meal: " + m["meal"] + " (" + m["peak"] + ")"
            + " | Present: " + str(m["present"])
            + " | Cooked: " + str(m["cooked"])
            + " | Eaten: " + str(m["eaten"])
            + " | Wasted: " + str(m["wasted"])
            + " | Demand: " + str(m["demand_pct"]) + "%"
            + " | Waste: " + str(m["waste_pct"]) + "%"
        )
        idx = idx + 1

    if total_present > 0:
        avg_demand = round((total_eaten / total_present) * 100, 1)
    else:
        avg_demand = 0.0

    avg_waste = round((total_wasted / total_cooked) * 100, 1)
    suggested_next = round(total_eaten * 1.05)
    overall_advice = get_advice(avg_demand, avg_waste, total_wasted)

    print("\n--- SUMMARY & SPECIFICATIONS ---")
    print("Food Item: " + matched[0]["name"])
    print("Total Past Entries: " + str(len(matched)))
    print("Served In Meals: " + ", ".join(meals_used))
    print("Total Students Present (sum): " + str(total_present))
    print("Total Portions Cooked: " + str(total_cooked))
    print("Total Portions Eaten: " + str(total_eaten))
    print("Total Portions Wasted: " + str(total_wasted))
    print("Overall Demand %: " + str(avg_demand) + "%")
    print("Overall Waste %: " + str(avg_waste) + "%")
    print("Suggested Next Quantity: " + str(suggested_next))
    print("Overall Recommendation: " + overall_advice)


def add_new_record(records):
    name = input("Enter Food Item Name: ").strip()
    if name == "":
        print("Error: Food name cannot be blank.")
        return

    print("Choose Meal Time: 1. Breakfast  2. Lunch  3. Snacks  4. Dinner")
    choice = input("Enter choice (1-4): ").strip()
    if choice == "1":
        meal = "Breakfast"
    elif choice == "2":
        meal = "Lunch"
    elif choice == "3":
        meal = "Snacks"
    elif choice == "4":
        meal = "Dinner"
    else:
        print("Error: Invalid meal choice.")
        return

    try:
        present = int(input("Enter Students Present: "))
        cooked = int(input("Enter Portions Cooked: "))
        eaten = int(input("Enter Portions Eaten: "))
    except ValueError:
        print("Error: Please enter whole numbers only.")
        return

    if present < 0 or cooked <= 0 or eaten < 0:
        print("Error: Present/eaten must be >= 0 and cooked must be > 0.")
        return
    if eaten > cooked:
        print("Error: Portions eaten cannot be more than portions cooked.")
        return

    rec = make_record(name, meal, present, cooked, eaten)
    records.append(rec)
    print("Added! Wasted portions = " + str(rec["wasted"]) + " | Advice: " + rec["advice"])


def main():
    records = load_from_file()

    while True:
        print("\n=== HOSTEL/CANTEEN FOOD DEMAND & WASTE SYSTEM ===")
        print("1. Add Food Record")
        print("2. View All Records")
        print("3. View Rankings (Waste % & Demand %)")
        print("4. View Pattern Suggestions (Slot-wise with Food)")
        print("5. Food Details (Past Record Analysis)")
        print("6. Save Records to File")
        print("7. Exit")

        opt = input("Enter your choice (1-7): ").strip()

        if opt == "1":
            add_new_record(records)
        elif opt == "2":
            show_records(records)
        elif opt == "3":
            show_rankings(records)
        elif opt == "4":
            show_patterns(records)
        elif opt == "5":
            show_food_details(records)
        elif opt == "6":
            save_to_file(records)
        elif opt == "7":
            save_to_file(records)
            print("Exiting program. Bye!")
            break
        else:
            print("Invalid option. Choose between 1 and 7.")


if __name__ == "__main__":
    main()