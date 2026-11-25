Hostel/Canteen Food Demand & Waste Management System
A beginner-friendly, terminal-based Python application built for Computational Thinking and Programming (2026CSAE100) to help hostel and canteen staff track food preparation, calculate food waste automatically, spot slot-wise food patterns, inspect past records for specific dishes, and make data-backed cooking recommendations.

Problem Statement
Hostels and canteens often cook food in fixed or estimated batches without tracking actual consumption against student attendance. Cooking too much leads to food wastage and higher costs, while cooking too little causes popular items to run out early. This system calculates waste automatically (cooked - eaten), computes demand and waste percentages, ranks items, analyzes slot-wise dish patterns, and suggests next-batch quantities using simple rule-based logic.

Key Features
Add Food Record (with Input Validation): Accepts food item name, meal slot (Breakfast, Lunch, Snacks, Dinner), students present, portions cooked, and portions eaten. Validates against blank names, negative values, non-positive cooked portions, and eaten quantities exceeding cooked quantities.
Automatic Waste & Percentage Calculation: Computes wasted portions as cooked - eaten, calculates Demand % ((eaten / present) * 100) and Waste % ((wasted / cooked) * 100), identifies peak meal slots (Lunch, Dinner), and estimates Suggested Next Qty (round(eaten * 1.05)).
Rule-Based Recommendations: Classifies each entry into actionable advice (REMOVE from menu, SERVE LESS OFTEN, REDUCE quantity, INCREASE quantity, or KEEP same).
View All Food Records: Displays all logged food entries with calculated metrics and recommendations.
Rankings (Waste % & Demand %): Sorts food records from highest to lowest Waste % and Demand %.
Pattern Analysis of Each Slot with Food: Breaks down each meal slot (Breakfast, Lunch, Snacks, Dinner), lists every dish logged in that slot with its demand/waste/suggestion, and shows slot-level averages and batch/stock advice.
Food Details (Past Record Analysis): Searches past entries for a specific food item and summarizes total entries, slots served, total cooked/eaten/wasted portions, overall demand %, overall waste %, suggested next quantity, and final advice.
Plain Text File Persistence: Saves and loads records using canteen_data.txt with pipe-separated (|) lines via standard open().
Recommendation Rules
Zero Waste (wasted == 0): INCREASE quantity (finished completely)
High Waste & Low Demand (waste_pct >= 35 and demand_pct < 40): REMOVE from menu
Very High Waste (waste_pct >= 25): SERVE LESS OFTEN
Moderate Waste (waste_pct >= 12): REDUCE quantity
High Demand (demand_pct >= 80): INCREASE quantity
Otherwise: KEEP same
Python Concepts Used
Variables & Data Types: Strings, integers, floats, booleans, lists, dictionaries, and tuples (MEAL_SLOTS, PEAK_SLOTS).
Conditional Statements (if-elif-else): Input checks, peak meal slot detection, percentage division guards, and recommendation rules.
Loops (for and while): Main interactive menu loop (while True), iterating over records, slot-wise grouping, past-item aggregation, and file reading/writing.
Functions: Modular functions for calculations, validation, file handling, display, rankings, slot patterns, and dish history analysis.
File Handling: Standard open("canteen_data.txt", "w") and open("canteen_data.txt", "r") with try...except FileNotFoundError.
Project Structure
canteen-food-demand-waste/
├── canteen_terminal.py   # Main terminal application
├── canteen_data.txt      # Auto-created text file storing records (pipe-separated)
└── README.md             # Project documentation
Course: Computational Thinking and Programming (2026CSAE100)

Team Members: Aman Kumar Sah (Leader)
              Aditya Raj, Parth Panchariya, Manish Singh Kirola
