# ============================================================
# FITNESS GOAL TRACKER
# PHASE 4 - 100% COMPLETE (FULL VERSION)
# ============================================================

import json
import os
import sys
from datetime import datetime, date, timedelta

# Ensure UTF-8 output if supported on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ------------------------------------------------------------
# CONSTANTS & MET MULTIPLIERS FOR CALORIE CALCULATION
# ------------------------------------------------------------

DATA_FILE = "fitness_data.json"
REPORT_FILE = "fitness_report.txt"

# MET (Metabolic Equivalent of Task) values for workout types
ACTIVITY_MET = {
    "1": ("Walking (Moderate, ~5 km/h)", 3.5),
    "2": ("Running / Jogging (~8 km/h)", 8.0),
    "3": ("Cycling (Moderate, ~16 km/h)", 6.8),
    "4": ("Strength Training / Gym", 5.0),
    "5": ("HIIT / Circuit Training", 8.0),
    "6": ("Yoga / Stretching", 2.5),
    "7": ("Swimming (Freestyle)", 7.0),
    "8": ("Custom / General Workout", 4.5)
}


# ------------------------------------------------------------
# GLOBAL DATA STRUCTURES
# ------------------------------------------------------------

profile = {}
goals = {}
daily_logs = {}
achievements = []


# ------------------------------------------------------------
# HELPER: GET TODAY'S DATE STRING
# ------------------------------------------------------------

def get_today_str():
    return str(date.today())


# ------------------------------------------------------------
# HELPER: INITIALIZE OR GET TODAY'S PROGRESS LOG
# ------------------------------------------------------------

def get_today_progress():
    today = get_today_str()
    if today not in daily_logs:
        daily_logs[today] = {
            "Steps": 0,
            "Water": 0.0,
            "Workout": 0,
            "CaloriesBurned": 0,
            "CaloriesConsumed": 0,
            "Workouts": []
        }
    return daily_logs[today]


# ------------------------------------------------------------
# FILE HANDLING: SAVE DATA TO JSON
# ------------------------------------------------------------

def save_data(silent=True):
    data = {
        "profile": profile,
        "goals": goals,
        "daily_logs": daily_logs,
        "achievements": achievements
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        if not silent:
            print("\nData saved successfully to", DATA_FILE)
    except Exception as e:
        if not silent:
            print(f"\nError saving data: {e}")


# ------------------------------------------------------------
# FILE HANDLING: LOAD DATA FROM JSON
# ------------------------------------------------------------

def load_data():
    global profile, goals, daily_logs, achievements
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                profile = data.get("profile", {})
                goals = data.get("goals", {})
                daily_logs = data.get("daily_logs", {})
                achievements = data.get("achievements", [])
        except Exception:
            profile = {}
            goals = {}
            daily_logs = {}
            achievements = []


# ------------------------------------------------------------
# PAUSE FUNCTION
# ------------------------------------------------------------

def pause():
    input("\nPress Enter to continue...")


# ------------------------------------------------------------
# WELCOME SCREEN
# ------------------------------------------------------------

def welcome():
    print("=" * 60)
    print("                FITNESS GOAL TRACKER")
    print("             PHASE 4 - 100% COMPLETE")
    print("=" * 60)
    if len(profile) > 0:
        print(f" Welcome back, {profile.get('Name', 'User')}! [Data loaded]")
    else:
        print(" Welcome! Please set up your User Profile to get started.")
    print("=" * 60)


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

def menu():
    print("\n" + "=" * 35)
    print("             MAIN MENU")
    print("=" * 35)
    print(" 1. User Profile & Health Metrics")
    print(" 2. Daily Goals Management")
    print(" 3. Log Activity & Nutrition")
    print(" 4. View Today's Progress Dashboard")
    print(" 5. History & Weekly Analytics")
    print(" 6. Streaks & Achievement Badges")
    print(" 7. Export Fitness Summary Report")
    print(" 8. Data & Storage Settings")
    print(" 9. Exit")
    print("-" * 35)


# ------------------------------------------------------------
# 1. USER PROFILE & HEALTH METRICS SUBMENU
# ------------------------------------------------------------

def profile_menu():
    while True:
        print("\n" + "-" * 35)
        print("  User Profile & Health Metrics")
        print("-" * 35)
        print("1. Create / Setup Profile")
        print("2. View Profile")
        print("3. Edit Profile")
        print("4. Calculate BMI (Body Mass Index)")
        print("5. Calculate BMR & TDEE (Calorie Needs)")
        print("6. Calculate Target Heart Rate Zones")
        print("7. Ideal Body Weight & Goal Projection")
        print("8. Back to Main Menu")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            create_profile()
        elif choice == "2":
            view_profile()
        elif choice == "3":
            edit_profile()
        elif choice == "4":
            calculate_bmi()
        elif choice == "5":
            calculate_bmr_tdee()
        elif choice == "6":
            calculate_heart_rate_zones()
        elif choice == "7":
            ideal_weight_and_goals()
        elif choice == "8":
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()


# ------------------------------------------------------------
# CREATE USER PROFILE
# ------------------------------------------------------------

def create_profile():
    print("\nCreate User Profile")
    print("-" * 30)

    name = input("Enter Name : ").strip()
    while name == "":
        print("Name cannot be empty.")
        name = input("Enter Name : ").strip()
    profile["Name"] = name

    # AGE
    while True:
        try:
            age = int(input("Enter Age : "))
            if 0 < age <= 120:
                profile["Age"] = age
                break
            else:
                print("Age must be between 1 and 120.")
        except ValueError:
            print("Enter a valid age.")

    # GENDER
    while True:
        gender = input("Enter Gender (Male/Female/Other) : ").strip().capitalize()
        if gender in ["Male", "Female", "Other"]:
            profile["Gender"] = gender
            break
        else:
            print("Please enter 'Male', 'Female', or 'Other'.")

    # HEIGHT
    while True:
        try:
            height = float(input("Enter Height (cm) : "))
            if 50 <= height <= 260:
                profile["Height"] = height
                break
            else:
                print("Height must be between 50 cm and 260 cm.")
        except ValueError:
            print("Enter a valid height.")

    # WEIGHT
    while True:
        try:
            weight = float(input("Enter Weight (kg) : "))
            if 20 <= weight <= 350:
                profile["Weight"] = weight
                break
            else:
                print("Weight must be between 20 kg and 350 kg.")
        except ValueError:
            print("Enter a valid weight.")

    # ACTIVITY LEVEL
    print("\nSelect Activity Level:")
    print("1. Sedentary (little to no exercise)")
    print("2. Lightly Active (light exercise 1-3 days/week)")
    print("3. Moderately Active (moderate exercise 3-5 days/week)")
    print("4. Very Active (hard exercise 6-7 days/week)")
    print("5. Extra Active (very hard exercise & physical job)")

    activity_map = {
        "1": "Sedentary",
        "2": "Lightly Active",
        "3": "Moderately Active",
        "4": "Very Active",
        "5": "Extra Active"
    }
    while True:
        act_choice = input("Enter Activity Level (1-5) [Default 3]: ").strip()
        if act_choice == "":
            act_choice = "3"
        if act_choice in activity_map:
            profile["ActivityLevel"] = activity_map[act_choice]
            break
        else:
            print("Invalid selection. Please choose 1 to 5.")

    save_data()
    check_and_unlock_badges()
    print("\nProfile Created Successfully & Saved.")
    pause()


# ------------------------------------------------------------
# VIEW PROFILE
# ------------------------------------------------------------

def view_profile():
    if len(profile) == 0:
        print("\nNo profile found. Please create your profile first.")
        pause()
        return

    print("\nUser Profile")
    print("-" * 35)
    print("Name           :", profile.get("Name", "N/A"))
    print("Age            :", profile.get("Age", "N/A"))
    print("Gender         :", profile.get("Gender", "N/A"))
    print("Height         :", profile.get("Height", "N/A"), "cm")
    print("Weight         :", profile.get("Weight", "N/A"), "kg")
    print("Activity Level :", profile.get("ActivityLevel", "Moderately Active"))
    pause()


# ------------------------------------------------------------
# EDIT PROFILE
# ------------------------------------------------------------

def edit_profile():
    if len(profile) == 0:
        print("\nPlease create your profile first.")
        pause()
        return

    print("\nEdit Profile")
    print("-" * 35)
    print("Press Enter to keep the existing value.")

    # NAME
    name = input("Name [" + str(profile.get("Name", "")) + "] : ").strip()
    if name != "":
        profile["Name"] = name

    # AGE
    while True:
        age_input = input("Age [" + str(profile.get("Age", "")) + "] : ").strip()
        if age_input == "":
            break
        try:
            age = int(age_input)
            if 0 < age <= 120:
                profile["Age"] = age
                break
            else:
                print("Age must be between 1 and 120.")
        except ValueError:
            print("Enter a valid age.")

    # GENDER
    while True:
        gender_input = input("Gender [" + str(profile.get("Gender", "")) + "] : ").strip().capitalize()
        if gender_input == "":
            break
        if gender_input in ["Male", "Female", "Other"]:
            profile["Gender"] = gender_input
            break
        else:
            print("Please enter 'Male', 'Female', or 'Other'.")

    # HEIGHT
    while True:
        height_input = input("Height [" + str(profile.get("Height", "")) + " cm] : ").strip()
        if height_input == "":
            break
        try:
            height = float(height_input)
            if 50 <= height <= 260:
                profile["Height"] = height
                break
            else:
                print("Height must be between 50 cm and 260 cm.")
        except ValueError:
            print("Enter a valid height.")

    # WEIGHT
    while True:
        weight_input = input("Weight [" + str(profile.get("Weight", "")) + " kg] : ").strip()
        if weight_input == "":
            break
        try:
            weight = float(weight_input)
            if 20 <= weight <= 350:
                profile["Weight"] = weight
                break
            else:
                print("Weight must be between 20 kg and 350 kg.")
        except ValueError:
            print("Enter a valid weight.")

    # ACTIVITY LEVEL
    curr_act = profile.get("ActivityLevel", "Moderately Active")
    print(f"\nCurrent Activity Level: {curr_act}")
    print("1. Sedentary | 2. Lightly Active | 3. Moderately Active | 4. Very Active | 5. Extra Active")
    act_input = input("Activity Level (1-5 or press Enter to keep): ").strip()
    activity_map = {
        "1": "Sedentary",
        "2": "Lightly Active",
        "3": "Moderately Active",
        "4": "Very Active",
        "5": "Extra Active"
    }
    if act_input in activity_map:
        profile["ActivityLevel"] = activity_map[act_input]

    save_data()
    print("\nProfile Updated Successfully & Saved.")
    pause()


# ------------------------------------------------------------
# BMI CALCULATOR
# ------------------------------------------------------------

def calculate_bmi():
    if len(profile) == 0:
        print("\nPlease create your profile first.")
        pause()
        return

    height_m = profile["Height"] / 100
    weight = profile["Weight"]
    bmi = weight / (height_m * height_m)

    print("\n" + "=" * 35)
    print("          BMI CALCULATOR")
    print("=" * 35)
    print("Name   :", profile["Name"])
    print("Height :", profile["Height"], "cm")
    print("Weight :", profile["Weight"], "kg")
    print("\nBMI    :", round(bmi, 2))

    # BMI CATEGORY
    if bmi < 18.5:
        category = "Underweight (< 18.5)"
        advice = "Consider a nutrient-dense diet to reach a healthy weight."
    elif bmi < 25:
        category = "Normal Weight (18.5 - 24.9)"
        advice = "Great job! Keep maintaining your balanced diet and workout routine."
    elif bmi < 30:
        category = "Overweight (25.0 - 29.9)"
        advice = "Incorporate regular cardio & a moderate calorie deficit to improve health."
    else:
        category = "Obese (>= 30.0)"
        advice = "Focus on structured exercise, hydration, and a sustainable nutrition plan."

    print("Category :", category)
    print("Advice   :", advice)
    print("-" * 35)
    pause()


# ------------------------------------------------------------
# BMR & TDEE CALCULATOR (Mifflin-St Jeor)
# ------------------------------------------------------------

def calculate_bmr_tdee():
    if len(profile) == 0:
        print("\nPlease create your profile first.")
        pause()
        return

    weight = profile["Weight"]
    height = profile["Height"]
    age = profile["Age"]
    gender = profile.get("Gender", "Male")
    activity = profile.get("ActivityLevel", "Moderately Active")

    # Mifflin-St Jeor Equation
    if gender.lower() == "female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    multiplier = activity_multipliers.get(activity, 1.55)
    tdee = bmr * multiplier

    print("\n" + "=" * 45)
    print("      METABOLIC RATE & CALORIE NEEDS")
    print("=" * 45)
    print(f"Basal Metabolic Rate (BMR) : {round(bmr, 1)} kcal/day")
    print("  (Calories burned at complete rest)")
    print(f"Activity Level              : {activity} (x{multiplier})")
    print(f"Total Daily Energy Exp (TDEE): {round(tdee, 1)} kcal/day")
    print("  (Estimated calories to maintain current weight)")
    print("-" * 45)
    print("Calorie Targets by Goal:")
    print(f"  * Weight Loss (-500 kcal)   : {round(tdee - 500)} kcal/day")
    print(f"  * Mild Loss   (-250 kcal)   : {round(tdee - 250)} kcal/day")
    print(f"  * Maintenance (0 kcal)      : {round(tdee)} kcal/day")
    print(f"  * Muscle Gain (+300 kcal)   : {round(tdee + 300)} kcal/day")
    print("=" * 45)
    pause()


# ------------------------------------------------------------
# TARGET HEART RATE ZONES (Karvonen / Max HR formula)
# ------------------------------------------------------------

def calculate_heart_rate_zones():
    if len(profile) == 0:
        print("\nPlease create your profile first.")
        pause()
        return

    age = profile["Age"]
    max_hr = 220 - age

    print("\n" + "=" * 45)
    print("         TARGET HEART RATE ZONES")
    print("=" * 45)
    print(f"Estimated Max Heart Rate : {max_hr} BPM (Beats/Min)")
    print("-" * 45)
    print(f"1. Warm Up (50% - 60%)      : {round(max_hr * 0.50)} - {round(max_hr * 0.60)} BPM")
    print(f"2. Fat Burn (60% - 70%)     : {round(max_hr * 0.60)} - {round(max_hr * 0.70)} BPM")
    print(f"3. Aerobic / Cardio (70-85%): {round(max_hr * 0.70)} - {round(max_hr * 0.85)} BPM")
    print(f"4. Peak / Anaerobic (85-100%): {round(max_hr * 0.85)} - {max_hr} BPM")
    print("-" * 45)
    pause()


# ------------------------------------------------------------
# IDEAL BODY WEIGHT & GOAL PROJECTION
# ------------------------------------------------------------

def ideal_weight_and_goals():
    if len(profile) == 0:
        print("\nPlease create your profile first.")
        pause()
        return

    height_cm = profile["Height"]
    weight_kg = profile["Weight"]
    gender = profile.get("Gender", "Male")

    # Height in inches
    height_inches = height_cm / 2.54
    inches_over_5ft = max(0, height_inches - 60)

    # Devine Formula
    if gender.lower() == "female":
        ibw = 45.5 + (2.3 * inches_over_5ft)
    else:
        ibw = 50.0 + (2.3 * inches_over_5ft)

    diff = round(weight_kg - ibw, 1)

    print("\n" + "=" * 45)
    print("       IDEAL WEIGHT & PROJECTIONS")
    print("=" * 45)
    print(f"Current Weight : {weight_kg} kg")
    print(f"Ideal Weight   : {round(ibw, 1)} kg (Devine Formula)")

    if abs(diff) < 2:
        print("Status         : You are right at your ideal weight!")
    elif diff > 0:
        weeks = round(diff / 0.5, 1)
        print(f"Status         : +{diff} kg from ideal weight.")
        print(f"Target Timeline: ~{weeks} weeks at a healthy 0.5 kg/week rate.")
    else:
        weeks = round(abs(diff) / 0.3, 1)
        print(f"Status         : {diff} kg below ideal weight.")
        print(f"Target Timeline: ~{weeks} weeks at a healthy 0.3 kg/week rate.")

    print("-" * 45)
    pause()


# ------------------------------------------------------------
# 2. DAILY GOALS MANAGEMENT SUBMENU
# ------------------------------------------------------------

def goals_menu():
    while True:
        print("\n" + "-" * 35)
        print("    Daily Goals Management")
        print("-" * 35)
        print("1. Set / Update Daily Goals")
        print("2. View Current Daily Goals")
        print("3. Reset Goals to Recommendations")
        print("4. Back to Main Menu")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            set_goals()
        elif choice == "2":
            view_goals()
        elif choice == "3":
            reset_recommended_goals()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice.")
            pause()


# ------------------------------------------------------------
# SET / UPDATE DAILY GOALS
# ------------------------------------------------------------

def set_goals():
    print("\nSet Daily Goals")
    print("-" * 35)
    print("Press Enter to keep existing value (if any).")

    # STEPS
    curr_steps = goals.get("Steps", 10000)
    while True:
        val = input(f"Daily Step Goal [{curr_steps}] : ").strip()
        if val == "":
            goals["Steps"] = curr_steps
            break
        try:
            steps = int(val)
            if steps > 0:
                goals["Steps"] = steps
                break
            else:
                print("Steps must be greater than 0.")
        except ValueError:
            print("Enter a valid number.")

    # WATER
    curr_water = goals.get("Water", 3.0)
    while True:
        val = input(f"Daily Water Goal (Litres) [{curr_water} L] : ").strip()
        if val == "":
            goals["Water"] = curr_water
            break
        try:
            water = float(val)
            if water > 0:
                goals["Water"] = water
                break
            else:
                print("Water goal must be greater than 0.")
        except ValueError:
            print("Enter a valid number.")

    # WORKOUT
    curr_workout = goals.get("Workout", 45)
    while True:
        val = input(f"Daily Workout Goal (Minutes) [{curr_workout} min] : ").strip()
        if val == "":
            goals["Workout"] = curr_workout
            break
        try:
            workout = int(val)
            if workout > 0:
                goals["Workout"] = workout
                break
            else:
                print("Workout goal must be greater than 0.")
        except ValueError:
            print("Enter a valid number.")

    # CALORIE BURN GOAL
    curr_burn = goals.get("CaloriesBurn", 400)
    while True:
        val = input(f"Daily Calorie Burn Goal (kcal) [{curr_burn} kcal] : ").strip()
        if val == "":
            goals["CaloriesBurn"] = curr_burn
            break
        try:
            burn = int(val)
            if burn > 0:
                goals["CaloriesBurn"] = burn
                break
            else:
                print("Calorie burn goal must be greater than 0.")
        except ValueError:
            print("Enter a valid number.")

    # CALORIE INTAKE TARGET
    curr_intake = goals.get("CaloriesIntake", 2000)
    while True:
        val = input(f"Daily Calorie Intake Target (kcal) [{curr_intake} kcal] : ").strip()
        if val == "":
            goals["CaloriesIntake"] = curr_intake
            break
        try:
            intake = int(val)
            if intake > 0:
                goals["CaloriesIntake"] = intake
                break
            else:
                print("Calorie intake target must be greater than 0.")
        except ValueError:
            print("Enter a valid number.")

    save_data()
    print("\nGoals Saved Successfully & Persisted.")
    pause()


# ------------------------------------------------------------
# VIEW DAILY GOALS
# ------------------------------------------------------------

def view_goals():
    if len(goals) == 0:
        print("\nNo goals set yet. Please set your daily goals first.")
        pause()
        return

    print("\nDaily Goals")
    print("-" * 35)
    print(f"Step Goal             : {goals.get('Steps', 10000)} steps")
    print(f"Water Goal            : {goals.get('Water', 3.0)} Litres")
    print(f"Workout Goal          : {goals.get('Workout', 45)} Minutes")
    print(f"Calorie Burn Goal     : {goals.get('CaloriesBurn', 400)} kcal")
    print(f"Calorie Intake Target : {goals.get('CaloriesIntake', 2000)} kcal")
    pause()


# ------------------------------------------------------------
# RESET TO RECOMMENDED GOALS
# ------------------------------------------------------------

def reset_recommended_goals():
    goals["Steps"] = 10000
    goals["Water"] = 3.0
    goals["Workout"] = 45
    goals["CaloriesBurn"] = 450
    goals["CaloriesIntake"] = 2200
    save_data()
    print("\nGoals have been set to standard healthy recommendations:")
    print("  * Steps: 10,000 steps")
    print("  * Water: 3.0 Litres")
    print("  * Workout: 45 Minutes")
    print("  * Calorie Burn: 450 kcal")
    print("  * Calorie Intake: 2,200 kcal")
    pause()


# ------------------------------------------------------------
# 3. LOG ACTIVITY & NUTRITION SUBMENU
# ------------------------------------------------------------

def log_activity_menu():
    if len(goals) == 0:
        print("\nPlease set your daily goals first.")
        pause()
        return

    while True:
        print("\n" + "-" * 35)
        print("    Log Activity & Nutrition")
        print("-" * 35)
        print("1. Log Steps Walked")
        print("2. Log Water Intake (Quick-Add / Custom)")
        print("3. Log Workout & Calculate Calories Burned")
        print("4. Log Meal / Calorie Intake")
        print("5. Quick Update All Progress")
        print("6. Back to Main Menu")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            log_steps()
        elif choice == "2":
            log_water()
        elif choice == "3":
            log_workout()
        elif choice == "4":
            log_calories_consumed()
        elif choice == "5":
            quick_update_all()
        elif choice == "6":
            break
        else:
            print("\nInvalid choice.")
            pause()


# ------------------------------------------------------------
# LOG STEPS
# ------------------------------------------------------------

def log_steps():
    progress = get_today_progress()
    print("\nLog Steps Walked")
    print("-" * 30)
    print(f"Current Today's Steps: {progress.get('Steps', 0)}")
    print("1. Add more steps to today's count")
    print("2. Set total steps for today")

    opt = input("Choose option (1/2): ").strip()

    while True:
        try:
            steps_input = int(input("Enter Steps : "))
            if steps_input >= 0:
                if opt == "1":
                    progress["Steps"] = progress.get("Steps", 0) + steps_input
                else:
                    progress["Steps"] = steps_input
                break
            else:
                print("Steps cannot be negative.")
        except ValueError:
            print("Enter a valid integer.")

    save_data()
    check_and_unlock_badges()
    print(f"\nSteps updated! Today's Total: {progress['Steps']} steps.")
    pause()


# ------------------------------------------------------------
# LOG WATER INTAKE
# ------------------------------------------------------------

def log_water():
    progress = get_today_progress()
    curr_water = progress.get("Water", 0.0)
    print("\nLog Water Intake")
    print("-" * 30)
    print(f"Current Hydration: {round(curr_water, 2)} L / {goals.get('Water', 3.0)} L")
    print("1. Add 1 Glass (250 ml / 0.25 L)")
    print("2. Add 1 Bottle (500 ml / 0.50 L)")
    print("3. Add 1 Large Bottle (1000 ml / 1.0 L)")
    print("4. Add Custom Litres")
    print("5. Set Exact Today's Total")

    opt = input("Choose option (1-5): ").strip()
    if opt == "1":
        progress["Water"] = round(curr_water + 0.25, 2)
    elif opt == "2":
        progress["Water"] = round(curr_water + 0.50, 2)
    elif opt == "3":
        progress["Water"] = round(curr_water + 1.00, 2)
    elif opt == "4":
        while True:
            try:
                amt = float(input("Enter Litres to add : "))
                if amt >= 0:
                    progress["Water"] = round(curr_water + amt, 2)
                    break
                else:
                    print("Amount cannot be negative.")
            except ValueError:
                print("Enter a valid number.")
    elif opt == "5":
        while True:
            try:
                amt = float(input("Enter Total Litres for today : "))
                if amt >= 0:
                    progress["Water"] = round(amt, 2)
                    break
                else:
                    print("Amount cannot be negative.")
            except ValueError:
                print("Enter a valid number.")
    else:
        print("Invalid option.")
        pause()
        return

    save_data()
    check_and_unlock_badges()
    print(f"\nWater updated! Today's Total: {progress['Water']} Litres.")
    pause()


# ------------------------------------------------------------
# LOG WORKOUT & ESTIMATE CALORIES BURNED
# ------------------------------------------------------------

def log_workout():
    progress = get_today_progress()
    user_weight = profile.get("Weight", 70.0)

    print("\nLog Workout Session")
    print("-" * 35)
    print("Select Activity Type:")
    for k, (name, met) in ACTIVITY_MET.items():
        print(f" {k}. {name}")

    act_key = input("\nEnter Activity (1-8) [Default 4]: ").strip()
    if act_key not in ACTIVITY_MET:
        act_key = "4"

    act_name, met_value = ACTIVITY_MET[act_key]

    while True:
        try:
            duration = int(input("Enter Duration in Minutes : "))
            if duration > 0:
                break
            else:
                print("Duration must be greater than 0.")
        except ValueError:
            print("Enter a valid integer.")

    duration_hours = duration / 60.0
    calc_calories = round(met_value * user_weight * duration_hours)

    print(f"\nCalculated Calories Burned: ~{calc_calories} kcal (MET: {met_value}, Weight: {user_weight}kg)")
    override = input("Press Enter to accept or enter custom calories burned: ").strip()
    if override != "":
        try:
            burned = int(override)
            if burned >= 0:
                calc_calories = burned
        except ValueError:
            pass

    progress["Workout"] = progress.get("Workout", 0) + duration
    progress["CaloriesBurned"] = progress.get("CaloriesBurned", 0) + calc_calories
    if "Workouts" not in progress:
        progress["Workouts"] = []

    workout_entry = {
        "Activity": act_name,
        "Duration": duration,
        "Calories": calc_calories,
        "Time": datetime.now().strftime("%H:%M")
    }
    progress["Workouts"].append(workout_entry)

    save_data()
    check_and_unlock_badges()
    print(f"\nWorkout logged successfully!")
    print(f"Today's Active Workout Total: {progress['Workout']} mins | {progress['CaloriesBurned']} kcal burned.")
    pause()


# ------------------------------------------------------------
# LOG CALORIE INTAKE (MEALS)
# ------------------------------------------------------------

def log_calories_consumed():
    progress = get_today_progress()
    curr_consumed = progress.get("CaloriesConsumed", 0)
    print("\nLog Food & Calorie Intake")
    print("-" * 35)
    print(f"Current Calories Consumed Today: {curr_consumed} kcal / Target: {goals.get('CaloriesIntake', 2000)} kcal")
    print("1. Add calories from a meal / snack")
    print("2. Set total calories consumed today")

    opt = input("Choose option (1/2): ").strip()
    while True:
        try:
            val = int(input("Enter Calories (kcal): "))
            if val >= 0:
                if opt == "1":
                    progress["CaloriesConsumed"] = curr_consumed + val
                else:
                    progress["CaloriesConsumed"] = val
                break
            else:
                print("Calories cannot be negative.")
        except ValueError:
            print("Enter a valid integer.")

    save_data()
    print(f"\nNutrition updated! Today's Total Consumed: {progress['CaloriesConsumed']} kcal.")
    pause()


# ------------------------------------------------------------
# QUICK UPDATE ALL PROGRESS (Steps, Water, Workout, Calories)
# ------------------------------------------------------------

def quick_update_all():
    progress = get_today_progress()
    print("\nQuick Update Today's Progress")
    print("-" * 35)

    # STEPS
    while True:
        try:
            val = input(f"Total Steps Today [{progress.get('Steps', 0)}] : ").strip()
            if val == "":
                break
            steps = int(val)
            if steps >= 0:
                progress["Steps"] = steps
                break
            else:
                print("Steps cannot be negative.")
        except ValueError:
            print("Enter a valid number.")

    # WATER
    while True:
        try:
            val = input(f"Total Water in Litres [{progress.get('Water', 0.0)}] : ").strip()
            if val == "":
                break
            water = float(val)
            if water >= 0:
                progress["Water"] = round(water, 2)
                break
            else:
                print("Water cannot be negative.")
        except ValueError:
            print("Enter a valid number.")

    # WORKOUT
    while True:
        try:
            val = input(f"Total Workout in Minutes [{progress.get('Workout', 0)}] : ").strip()
            if val == "":
                break
            workout = int(val)
            if workout >= 0:
                progress["Workout"] = workout
                break
            else:
                print("Workout cannot be negative.")
        except ValueError:
            print("Enter a valid number.")

    # CALORIES BURNED
    while True:
        try:
            val = input(f"Total Active Calories Burned [{progress.get('CaloriesBurned', 0)}] : ").strip()
            if val == "":
                break
            burn = int(val)
            if burn >= 0:
                progress["CaloriesBurned"] = burn
                break
            else:
                print("Calories burned cannot be negative.")
        except ValueError:
            print("Enter a valid number.")

    # CALORIES CONSUMED
    while True:
        try:
            val = input(f"Total Calories Consumed [{progress.get('CaloriesConsumed', 0)}] : ").strip()
            if val == "":
                break
            consumed = int(val)
            if consumed >= 0:
                progress["CaloriesConsumed"] = consumed
                break
            else:
                print("Calories consumed cannot be negative.")
        except ValueError:
            print("Enter a valid number.")

    save_data()
    check_and_unlock_badges()
    print("\nAll metrics updated successfully & saved!")
    pause()


# ------------------------------------------------------------
# PROGRESS BAR GENERATOR
# ------------------------------------------------------------

def progress_bar(percent, width=22):
    bounded = max(0, min(percent, 100))
    filled_blocks = int((bounded / 100) * width)
    empty_blocks = width - filled_blocks
    bar = "[" + "#" * filled_blocks + "-" * empty_blocks + "]"
    return bar


# ------------------------------------------------------------
# 4. VIEW TODAY'S PROGRESS DASHBOARD
# ------------------------------------------------------------

def view_progress():
    if len(goals) == 0:
        print("\nPlease set your daily goals first.")
        pause()
        return

    progress = get_today_progress()
    today_str = get_today_str()

    step_goal = goals.get("Steps", 10000)
    water_goal = goals.get("Water", 3.0)
    workout_goal = goals.get("Workout", 45)
    burn_goal = goals.get("CaloriesBurn", 400)
    intake_goal = goals.get("CaloriesIntake", 2000)

    steps = progress.get("Steps", 0)
    water = progress.get("Water", 0.0)
    workout = progress.get("Workout", 0)
    burned = progress.get("CaloriesBurned", 0)
    consumed = progress.get("CaloriesConsumed", 0)

    step_pct = (steps / step_goal * 100) if step_goal > 0 else 0
    water_pct = (water / water_goal * 100) if water_goal > 0 else 0
    workout_pct = (workout / workout_goal * 100) if workout_goal > 0 else 0
    burn_pct = (burned / burn_goal * 100) if burn_goal > 0 else 0

    capped_step = min(step_pct, 100)
    capped_water = min(water_pct, 100)
    capped_workout = min(workout_pct, 100)
    capped_burn = min(burn_pct, 100)
    overall = (capped_step + capped_water + capped_workout + capped_burn) / 4

    print("\n" + "=" * 55)
    print(f"        TODAY'S FITNESS DASHBOARD ({today_str})")
    print("=" * 55)

    # STEPS
    print(f"Steps           : {steps:>6} / {step_goal} steps")
    print(f"   {progress_bar(step_pct)} {step_pct:>6.1f}%")

    # WATER
    print(f"\nWater Intake    : {water:>6.2f} / {water_goal:.2f} Litres")
    print(f"   {progress_bar(water_pct)} {water_pct:>6.1f}%")

    # WORKOUT
    print(f"\nWorkout Time    : {workout:>6} / {workout_goal} Minutes")
    print(f"   {progress_bar(workout_pct)} {workout_pct:>6.1f}%")

    # CALORIES BURNED
    print(f"\nCalories Burned : {burned:>6} / {burn_goal} kcal")
    print(f"   {progress_bar(burn_pct)} {burn_pct:>6.1f}%")

    # CALORIE INTAKE & NET BALANCE
    net_cals = consumed - burned
    print(f"\nCalorie Intake  : {consumed} kcal (Target: {intake_goal} kcal)")
    print(f"Net Calorie Bal : {net_cals:+d} kcal (Consumed - Active Burn)")

    # WORKOUT LOGS
    workouts_list = progress.get("Workouts", [])
    if len(workouts_list) > 0:
        print("\nToday's Workout Sessions:")
        for idx, w in enumerate(workouts_list, 1):
            print(f"   {idx}. [{w.get('Time', '--:--')}] {w.get('Activity')} - {w.get('Duration')} mins (~{w.get('Calories')} kcal)")

    print("\n" + "-" * 55)
    print(f"OVERALL DAILY SCORE : {round(overall, 1)}% {progress_bar(overall)}")
    print("-" * 55)

    if overall >= 100:
        print("PERFECTION! All daily fitness goals achieved!")
    elif overall >= 80:
        print("EXCELLENT! You are close to completing all goals today.")
    elif overall >= 50:
        print("GOOD PROGRESS! Keep going, you are more than halfway there!")
    else:
        print("KEEP MOVING! Every step and workout counts.")

    check_and_unlock_badges()
    print("=" * 55)
    pause()


# ------------------------------------------------------------
# 5. HISTORY & WEEKLY ANALYTICS SUBMENU
# ------------------------------------------------------------

def history_menu():
    while True:
        print("\n" + "-" * 35)
        print("   History & Weekly Analytics")
        print("-" * 35)
        print("1. View Past 7 Days Summary")
        print("2. Browse Specific Date Log")
        print("3. View All-Time Statistics")
        print("4. Back to Main Menu")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            view_weekly_summary()
        elif choice == "2":
            browse_date_log()
        elif choice == "3":
            view_all_time_stats()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice.")
            pause()


# ------------------------------------------------------------
# VIEW PAST 7 DAYS SUMMARY
# ------------------------------------------------------------

def view_weekly_summary():
    if len(daily_logs) == 0:
        print("\nNo historical logs found yet.")
        pause()
        return

    print("\n" + "=" * 65)
    print("                PAST 7 DAYS ACTIVITY SUMMARY")
    print("=" * 65)
    print(f"{'Date':<12} | {'Steps':<8} | {'Water(L)':<8} | {'Workout':<9} | {'Burned':<8} | {'Score'}")
    print("-" * 65)

    today = date.today()
    total_steps = 0
    total_water = 0.0
    total_workout = 0
    total_burned = 0
    logged_days = 0

    step_goal = goals.get("Steps", 10000)
    water_goal = goals.get("Water", 3.0)
    workout_goal = goals.get("Workout", 45)

    for i in range(6, -1, -1):
        day_date = today - timedelta(days=i)
        day_str = str(day_date)
        log = daily_logs.get(day_str, None)

        if log:
            st = log.get("Steps", 0)
            wa = log.get("Water", 0.0)
            wo = log.get("Workout", 0)
            bu = log.get("CaloriesBurned", 0)

            s_pct = min(100, (st / step_goal * 100) if step_goal > 0 else 0)
            w_pct = min(100, (wa / water_goal * 100) if water_goal > 0 else 0)
            wo_pct = min(100, (wo / workout_goal * 100) if workout_goal > 0 else 0)
            score = round((s_pct + w_pct + wo_pct) / 3, 1)

            total_steps += st
            total_water += wa
            total_workout += wo
            total_burned += bu
            logged_days += 1

            print(f"{day_str:<12} | {st:<8} | {wa:<8.2f} | {wo:<6} min | {bu:<5} kcal | {score:>5.1f}%")
        else:
            print(f"{day_str:<12} | {'--':<8} | {'--':<8} | {'--':<9} | {'--':<8} | {'--'}")

    print("-" * 65)
    if logged_days > 0:
        avg_steps = round(total_steps / logged_days)
        avg_water = round(total_water / logged_days, 2)
        avg_workout = round(total_workout / logged_days, 1)
        avg_burned = round(total_burned / logged_days)
        print(f"WEEKLY AVERAGES ({logged_days} active days):")
        print(f" * Avg Steps/Day   : {avg_steps} steps")
        print(f" * Avg Water/Day   : {avg_water} Litres")
        print(f" * Avg Workout/Day : {avg_workout} Minutes")
        print(f" * Avg Burned/Day  : {avg_burned} kcal")
    print("=" * 65)
    pause()


# ------------------------------------------------------------
# BROWSE SPECIFIC DATE LOG
# ------------------------------------------------------------

def browse_date_log():
    if len(daily_logs) == 0:
        print("\nNo historical logs found.")
        pause()
        return

    print("\nAvailable Log Dates:")
    dates_list = sorted(daily_logs.keys(), reverse=True)
    for d in dates_list[:10]:
        print(" -", d)

    date_input = input("\nEnter Date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_input == "":
        date_input = get_today_str()

    if date_input not in daily_logs:
        print(f"\nNo log found for date: {date_input}")
        pause()
        return

    log = daily_logs[date_input]
    print(f"\nLog for {date_input}")
    print("-" * 35)
    print(f"Steps Walked      : {log.get('Steps', 0)}")
    print(f"Water Intake      : {log.get('Water', 0.0)} L")
    print(f"Workout Duration  : {log.get('Workout', 0)} mins")
    print(f"Calories Burned   : {log.get('CaloriesBurned', 0)} kcal")
    print(f"Calories Consumed : {log.get('CaloriesConsumed', 0)} kcal")

    workouts = log.get("Workouts", [])
    if len(workouts) > 0:
        print("\nWorkout Sessions:")
        for idx, w in enumerate(workouts, 1):
            print(f"  {idx}. [{w.get('Time', '--:--')}] {w.get('Activity')} - {w.get('Duration')} mins (~{w.get('Calories')} kcal)")
    pause()


# ------------------------------------------------------------
# VIEW ALL-TIME FITNESS STATISTICS
# ------------------------------------------------------------

def view_all_time_stats():
    if len(daily_logs) == 0:
        print("\nNo logged history yet.")
        pause()
        return

    total_days = len(daily_logs)
    total_steps = sum(v.get("Steps", 0) for v in daily_logs.values())
    total_water = sum(v.get("Water", 0.0) for v in daily_logs.values())
    total_workout = sum(v.get("Workout", 0) for v in daily_logs.values())
    total_burned = sum(v.get("CaloriesBurned", 0) for v in daily_logs.values())

    max_steps_day = max(daily_logs.items(), key=lambda x: x[1].get("Steps", 0), default=("N/A", {}))
    max_workout_day = max(daily_logs.items(), key=lambda x: x[1].get("Workout", 0), default=("N/A", {}))

    print("\n" + "=" * 45)
    print("          ALL-TIME FITNESS STATS")
    print("=" * 45)
    print(f"Total Days Logged     : {total_days} days")
    print(f"Total Steps Walked    : {total_steps:,} steps")
    print(f"Total Water Drank     : {round(total_water, 1)} Litres")
    print(f"Total Active Workout  : {total_workout} Minutes ({round(total_workout/60, 1)} hours)")
    print(f"Total Calories Burned : {total_burned:,} kcal")
    print("-" * 45)
    print(f"Personal Best (Steps) : {max_steps_day[1].get('Steps', 0)} steps on {max_steps_day[0]}")
    print(f"Personal Best (Workout): {max_workout_day[1].get('Workout', 0)} mins on {max_workout_day[0]}")
    print("=" * 45)
    pause()


# ------------------------------------------------------------
# 6. STREAKS & ACHIEVEMENT BADGES
# ------------------------------------------------------------

def calculate_streak():
    if len(daily_logs) == 0:
        return 0

    today = date.today()
    streak = 0

    check_date = today
    if str(check_date) not in daily_logs or (daily_logs[str(check_date)].get("Steps", 0) == 0 and daily_logs[str(check_date)].get("Workout", 0) == 0):
        check_date = today - timedelta(days=1)

    while True:
        day_str = str(check_date)
        if day_str in daily_logs:
            log = daily_logs[day_str]
            if log.get("Steps", 0) > 0 or log.get("Workout", 0) > 0 or log.get("Water", 0) > 0:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        else:
            break

    return streak


def check_and_unlock_badges():
    global achievements
    unlocked_now = []

    total_steps = sum(v.get("Steps", 0) for v in daily_logs.values())
    total_workout = sum(v.get("Workout", 0) for v in daily_logs.values())
    streak = calculate_streak()

    all_badges = [
        ("First Step", "Logged your first fitness activity.", len(daily_logs) >= 1),
        ("Hydration Hero", "Achieved your daily water goal.", any(v.get("Water", 0) >= goals.get("Water", 3.0) for v in daily_logs.values()) if len(goals) > 0 else False),
        ("10K Walker Club", "Walked over 10,000 steps in a single day.", any(v.get("Steps", 0) >= 10000 for v in daily_logs.values())),
        ("Calorie Crusher", "Burned 500+ active calories in one day.", any(v.get("CaloriesBurned", 0) >= 500 for v in daily_logs.values())),
        ("Consistency Master", "Maintained a 3-day active fitness streak.", streak >= 3),
        ("7-Day Warrior", "Maintained a 7-day active fitness streak.", streak >= 7),
        ("Century Performer", "Accumulated over 100,000 all-time steps.", total_steps >= 100000),
        ("Fitness Enthusiast", "Completed 300+ total workout minutes.", total_workout >= 300)
    ]

    for title, desc, condition in all_badges:
        if condition and title not in [a["title"] for a in achievements]:
            new_badge = {
                "title": title,
                "desc": desc,
                "date": get_today_str()
            }
            achievements.append(new_badge)
            unlocked_now.append(new_badge)

    if len(unlocked_now) > 0:
        save_data()
        for b in unlocked_now:
            print("\n" + "*" * 45)
            print(f" [NEW BADGE UNLOCKED] {b['title']}!")
            print(f"   {b['desc']}")
            print("*" * 45)


def streaks_and_badges_menu():
    streak = calculate_streak()
    check_and_unlock_badges()

    print("\n" + "=" * 50)
    print("         STREAKS & ACHIEVEMENT BADGES")
    print("=" * 50)
    print(f"Current Fitness Streak: {streak} Day{'s' if streak != 1 else ''} in a row!")
    if streak >= 7:
        print("   Incredible consistency! You are on fire!")
    elif streak >= 3:
        print("   Solid streak! Keep building the habit!")
    else:
        print("   Log your activity daily to build your streak.")

    print("\nUnlocked Badges:")
    print("-" * 50)
    if len(achievements) == 0:
        print("No badges unlocked yet. Start logging workouts and steps to earn awards!")
    else:
        for a in achievements:
            print(f" [*] {a['title']} (Earned: {a.get('date', 'N/A')})")
            print(f"     {a['desc']}")

    print("\nAvailable Milestones:")
    print("-" * 50)
    badge_titles = [a["title"] for a in achievements]
    available = [
        ("First Step", "Log any activity for 1 day"),
        ("Hydration Hero", f"Hit your water goal ({goals.get('Water', 3.0)} L)"),
        ("10K Walker Club", "Walk 10,000+ steps in a single day"),
        ("Calorie Crusher", "Burn 500+ kcal in a single day"),
        ("Consistency Master", "Maintain a 3-day active streak"),
        ("7-Day Warrior", "Maintain a 7-day active streak"),
        ("Century Performer", "Accumulate 100,000 all-time steps"),
        ("Fitness Enthusiast", "Log 300+ total workout minutes")
    ]
    for name, criteria in available:
        status = "[UNLOCKED]" if name in badge_titles else "[LOCKED]"
        print(f" - {name:<20} : {criteria} {status}")

    print("=" * 50)
    pause()


# ------------------------------------------------------------
# 7. EXPORT FITNESS SUMMARY REPORT (TXT FILE)
# ------------------------------------------------------------

def export_report():
    if len(profile) == 0 and len(daily_logs) == 0:
        print("\nNo profile or log data to export.")
        pause()
        return

    today_str = get_today_str()
    streak = calculate_streak()

    lines = []
    lines.append("=" * 60)
    lines.append("               FITNESS GOAL TRACKER - SUMMARY REPORT")
    lines.append(f"               Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)
    lines.append("\n[1] USER PROFILE")
    lines.append("-" * 35)
    lines.append(f"Name           : {profile.get('Name', 'N/A')}")
    lines.append(f"Age            : {profile.get('Age', 'N/A')}")
    lines.append(f"Gender         : {profile.get('Gender', 'N/A')}")
    lines.append(f"Height         : {profile.get('Height', 'N/A')} cm")
    lines.append(f"Weight         : {profile.get('Weight', 'N/A')} kg")
    lines.append(f"Activity Level : {profile.get('ActivityLevel', 'N/A')}")

    if "Height" in profile and "Weight" in profile:
        h_m = profile["Height"] / 100
        bmi = profile["Weight"] / (h_m * h_m)
        lines.append(f"BMI Score      : {round(bmi, 2)}")

    lines.append("\n[2] DAILY TARGET GOALS")
    lines.append("-" * 35)
    lines.append(f"Daily Steps Goal      : {goals.get('Steps', 'Not Set')} steps")
    lines.append(f"Daily Water Goal      : {goals.get('Water', 'Not Set')} Litres")
    lines.append(f"Daily Workout Goal    : {goals.get('Workout', 'Not Set')} Minutes")
    lines.append(f"Daily Calorie Burn    : {goals.get('CaloriesBurn', 'Not Set')} kcal")
    lines.append(f"Daily Calorie Intake  : {goals.get('CaloriesIntake', 'Not Set')} kcal")

    lines.append("\n[3] STREAK & ACHIEVEMENTS")
    lines.append("-" * 35)
    lines.append(f"Current Active Streak : {streak} Days")
    lines.append(f"Total Badges Unlocked : {len(achievements)}")
    for a in achievements:
        lines.append(f" * {a['title']} - {a['desc']} ({a.get('date', 'N/A')})")

    lines.append("\n[4] RECENT DAILY LOGS")
    lines.append("-" * 60)
    lines.append(f"{'Date':<12} | {'Steps':<8} | {'Water(L)':<8} | {'Workout':<9} | {'Burned'}")
    lines.append("-" * 60)

    for d, log in sorted(daily_logs.items(), reverse=True):
        st = log.get("Steps", 0)
        wa = log.get("Water", 0.0)
        wo = log.get("Workout", 0)
        bu = log.get("CaloriesBurned", 0)
        lines.append(f"{d:<12} | {st:<8} | {wa:<8.2f} | {wo:<6} min | {bu} kcal")

    lines.append("\n" + "=" * 60)
    lines.append("              END OF FITNESS REPORT")
    lines.append("=" * 60 + "\n")

    report_content = "\n".join(lines)

    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report_content)
        print("\n" + "=" * 50)
        print(f" Fitness report successfully exported to:")
        print(f" >> {os.path.abspath(REPORT_FILE)}")
        print("=" * 50)
    except Exception as e:
        print(f"\nError exporting report: {e}")

    pause()


# ------------------------------------------------------------
# 8. DATA & STORAGE SETTINGS SUBMENU
# ------------------------------------------------------------

def data_settings_menu():
    while True:
        print("\n" + "-" * 35)
        print("    Data & Storage Settings")
        print("-" * 35)
        print(f"Data File: {os.path.abspath(DATA_FILE)}")
        print("1. Save Data Now")
        print("2. Reload Data from File")
        print("3. Reset / Clear All Data")
        print("4. Back to Main Menu")

        choice = input("\nEnter Choice : ").strip()

        if choice == "1":
            save_data(silent=False)
            pause()
        elif choice == "2":
            load_data()
            print("\nData reloaded successfully.")
            pause()
        elif choice == "3":
            confirm = input("\nAre you SURE you want to delete all profile & log data? (yes/no): ").strip().lower()
            if confirm == "yes":
                global profile, goals, daily_logs, achievements
                profile = {}
                goals = {}
                daily_logs = {}
                achievements = []
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                print("\nAll data has been reset successfully.")
            else:
                print("\nReset canceled.")
            pause()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice.")
            pause()


# ------------------------------------------------------------
# MAIN PROGRAM FUNCTION
# ------------------------------------------------------------

def main():
    load_data()
    welcome()

    while True:
        menu()
        choice = input("\nEnter Your Choice (1-9) : ").strip()

        # 1. PROFILE & HEALTH METRICS
        if choice == "1":
            profile_menu()

        # 2. DAILY GOALS MANAGEMENT
        elif choice == "2":
            goals_menu()

        # 3. LOG ACTIVITY & NUTRITION
        elif choice == "3":
            log_activity_menu()

        # 4. VIEW TODAY'S PROGRESS DASHBOARD
        elif choice == "4":
            view_progress()

        # 5. HISTORY & WEEKLY ANALYTICS
        elif choice == "5":
            history_menu()

        # 6. STREAKS & ACHIEVEMENT BADGES
        elif choice == "6":
            streaks_and_badges_menu()

        # 7. EXPORT FITNESS SUMMARY REPORT
        elif choice == "7":
            export_report()

        # 8. DATA & STORAGE SETTINGS
        elif choice == "8":
            data_settings_menu()

        # 9. EXIT
        elif choice == "9":
            save_data()
            print("\n" + "=" * 50)
            print(" Thank you for using Fitness Goal Tracker!")
            print(" Your progress has been automatically saved.")
            print(" Stay healthy, keep moving, and see you next time!")
            print("=" * 50 + "\n")
            break

        # INVALID OPTION
        else:
            print("\nInvalid Choice. Please select an option between 1 and 9.")
            pause()


if __name__ == "__main__":
    main()
