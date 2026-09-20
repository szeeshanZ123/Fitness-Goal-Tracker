# ============================================================
# FITNESS GOAL TRACKER
# Version 2.0 - Personal Fitness Management System
# A Comprehensive Python Terminal Application for Fitness Tracking
# ============================================================

import csv
import json
import os
import shutil
import sys
from datetime import datetime, date, timedelta

# Ensure UTF-8 output if supported on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ============================================================
# CONSTANTS & CONFIGURATION
# ============================================================

APP_NAME = "FITNESS GOAL TRACKER"
APP_VERSION = "2.0"
APP_SUBTITLE = "Personal Fitness Management System"

DATA_FILE = "fitness_data.json"
BACKUP_FILE = "fitness_backup.json"
REPORT_FILE = "fitness_report.txt"
CSV_FILE = "fitness_history.csv"

# MET (Metabolic Equivalent of Task) values for workout calculation
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

# Standard Primary Fitness Goals
FITNESS_GOAL_TYPES = {
    "1": "Weight Loss",
    "2": "Weight Gain",
    "3": "Muscle Building",
    "4": "General Fitness",
    "5": "Maintain Weight"
}


# ============================================================
# GLOBAL DATA STRUCTURES
# ============================================================

profile = {}
goals = {}
daily_logs = {}
weight_history = {}
achievements = []


# ============================================================
# INPUT VALIDATION & HELPER FUNCTIONS
# ============================================================

def pause():
    """Prompt user to press Enter to continue."""
    input("\nPress Enter to continue...")


def get_today_str():
    """Return today's date formatted as YYYY-MM-DD."""
    return str(date.today())


def get_valid_string(prompt, allow_empty=False, default=None):
    """Safely prompt for a non-empty string with optional default."""
    while True:
        prompt_str = f"{prompt} [{default}]: " if default is not None else f"{prompt}: "
        user_input = input(prompt_str).strip()
        if user_input == "" and default is not None:
            return default
        if user_input == "" and not allow_empty:
            print(">> Input cannot be empty. Please try again.")
            continue
        return user_input


def get_valid_int(prompt, min_val=None, max_val=None, default=None):
    """Safely prompt and validate an integer input with bounds and optional default."""
    while True:
        prompt_str = f"{prompt} [{default}]: " if default is not None else f"{prompt}: "
        user_input = input(prompt_str).strip()
        if user_input == "" and default is not None:
            return default
        try:
            val = int(user_input)
            if min_val is not None and val < min_val:
                print(f">> Value must be at least {min_val}. Please try again.")
                continue
            if max_val is not None and val > max_val:
                print(f">> Value must be at most {max_val}. Please try again.")
                continue
            return val
        except ValueError:
            print(">> Invalid input. Please enter a valid whole number.")


def get_valid_float(prompt, min_val=None, max_val=None, default=None):
    """Safely prompt and validate a float input with bounds and optional default."""
    while True:
        prompt_str = f"{prompt} [{default}]: " if default is not None else f"{prompt}: "
        user_input = input(prompt_str).strip()
        if user_input == "" and default is not None:
            return default
        try:
            val = float(user_input)
            if min_val is not None and val < min_val:
                print(f">> Value must be at least {min_val}. Please try again.")
                continue
            if max_val is not None and val > max_val:
                print(f">> Value must be at most {max_val}. Please try again.")
                continue
            return val
        except ValueError:
            print(">> Invalid input. Please enter a valid numeric value.")


def get_valid_choice(prompt, choices, default=None):
    """Safely prompt for a choice from a list or set of allowed strings."""
    valid_choices = [str(c) for c in choices]
    while True:
        prompt_str = f"{prompt} [{default}]: " if default is not None else f"{prompt}: "
        user_input = input(prompt_str).strip()
        if user_input == "" and default is not None:
            return str(default)
        if user_input in valid_choices:
            return user_input
        print(f">> Invalid selection. Allowed options: {', '.join(valid_choices)}")


def get_valid_date(prompt, default=None):
    """Safely prompt for a date string in YYYY-MM-DD format."""
    while True:
        prompt_str = f"{prompt} [{default}]: " if default is not None else f"{prompt}: "
        user_input = input(prompt_str).strip()
        if user_input == "" and default is not None:
            return default
        try:
            dt = datetime.strptime(user_input, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            print(">> Invalid date format. Please use YYYY-MM-DD (e.g. 2026-09-20).")


# ============================================================
# DATA ACCESS & INITIALIZATION
# ============================================================

def get_day_progress(date_str):
    """Get or initialize daily log for a given date with backward-compatible structure."""
    if date_str not in daily_logs:
        daily_logs[date_str] = {
            "Steps": 0,
            "Water": 0.0,
            "Workout": 0,
            "CaloriesBurned": 0,
            "CaloriesConsumed": 0,
            "Workouts": [],
            "Meals": {
                "Breakfast": [],
                "Lunch": [],
                "Dinner": [],
                "Snack": []
            }
        }
    else:
        # Backward compatibility checks for existing logs
        if "Workouts" not in daily_logs[date_str]:
            daily_logs[date_str]["Workouts"] = []
        if "Meals" not in daily_logs[date_str]:
            daily_logs[date_str]["Meals"] = {
                "Breakfast": [],
                "Lunch": [],
                "Dinner": [],
                "Snack": []
            }
        for meal_type in ["Breakfast", "Lunch", "Dinner", "Snack"]:
            if meal_type not in daily_logs[date_str]["Meals"]:
                daily_logs[date_str]["Meals"][meal_type] = []
    return daily_logs[date_str]


def get_today_progress():
    """Get or initialize today's daily log."""
    return get_day_progress(get_today_str())


# ============================================================
# FILE STORAGE & BACKUP MANAGEMENT
# ============================================================

def save_data(silent=True):
    """Persist current application state safely to JSON file."""
    data = {
        "profile": profile,
        "goals": goals,
        "daily_logs": daily_logs,
        "weight_history": weight_history,
        "achievements": achievements
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        if not silent:
            print(f"\n>> Data saved successfully to '{DATA_FILE}'")
    except Exception as e:
        if not silent:
            print(f"\n>> Error saving data: {e}")


def load_data():
    """Load and migrate existing JSON data safely."""
    global profile, goals, daily_logs, weight_history, achievements
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                profile = data.get("profile", {})
                goals = data.get("goals", {})
                daily_logs = data.get("daily_logs", {})
                weight_history = data.get("weight_history", {})
                achievements = data.get("achievements", [])

                # Backward compatibility: populate weight_history from profile if missing
                if not weight_history and "Weight" in profile:
                    weight_history[get_today_str()] = float(profile["Weight"])

                # Backward compatibility: ensure profile has defaults
                if "StartingWeight" not in profile and "Weight" in profile:
                    profile["StartingWeight"] = profile["Weight"]
                if "TargetWeight" not in profile and "Weight" in profile:
                    profile["TargetWeight"] = profile["Weight"]
                if "FitnessGoal" not in profile:
                    profile["FitnessGoal"] = "General Fitness"

        except Exception as e:
            print(f"\n>> Warning: Could not read '{DATA_FILE}' properly ({e}). Starting with default state.")
            profile = {}
            goals = {}
            daily_logs = {}
            weight_history = {}
            achievements = []


def create_backup():
    """Create a backup copy of the primary data file."""
    if not os.path.exists(DATA_FILE):
        print("\n>> No data file found to backup. Please save your data first.")
        return False
    try:
        shutil.copyfile(DATA_FILE, BACKUP_FILE)
        print(f"\n>> Backup successfully created: '{BACKUP_FILE}'")
        return True
    except Exception as e:
        print(f"\n>> Error creating backup: {e}")
        return False


def restore_backup():
    """Restore the application data from backup file."""
    if not os.path.exists(BACKUP_FILE):
        print(f"\n>> Backup file '{BACKUP_FILE}' not found.")
        return False
    try:
        shutil.copyfile(BACKUP_FILE, DATA_FILE)
        load_data()
        print(f"\n>> Backup restored successfully from '{BACKUP_FILE}'!")
        return True
    except Exception as e:
        print(f"\n>> Error restoring backup: {e}")
        return False


# ============================================================
# CALCULATIONS & CORE FORMULAS
# ============================================================

def calculate_bmi_value(height_cm, weight_kg):
    """Calculate BMI and return tuple (bmi_score, category, advice)."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "N/A", "Invalid height or weight."
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)

    if bmi < 18.5:
        category = "Underweight (< 18.5)"
        advice = "Consider a nutrient-dense diet to reach a healthy weight."
    elif bmi < 25.0:
        category = "Normal Weight (18.5 - 24.9)"
        advice = "Great job! Keep maintaining your balanced diet and workout routine."
    elif bmi < 30.0:
        category = "Overweight (25.0 - 29.9)"
        advice = "Incorporate regular cardio & a moderate calorie deficit to improve health."
    else:
        category = "Obese (>= 30.0)"
        advice = "Focus on structured exercise, hydration, and a sustainable nutrition plan."

    return round(bmi, 2), category, advice


def calculate_bmr_tdee_values(height_cm, weight_kg, age, gender="Male", activity="Moderately Active"):
    """Calculate BMR using Mifflin-St Jeor equation and TDEE based on activity level."""
    if gender.lower() == "female":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    multiplier = activity_multipliers.get(activity, 1.55)
    tdee = bmr * multiplier
    return round(bmr, 1), round(tdee, 1), multiplier


def calculate_ideal_weight_value(height_cm, gender="Male"):
    """Calculate Ideal Body Weight (IBW) in kg using the Devine Formula."""
    height_inches = height_cm / 2.54
    inches_over_5ft = max(0.0, height_inches - 60.0)
    if gender.lower() == "female":
        ibw = 45.5 + (2.3 * inches_over_5ft)
    else:
        ibw = 50.0 + (2.3 * inches_over_5ft)
    return round(ibw, 1)


def calculate_daily_score_for_log(log):
    """
    Calculate daily fitness score (0 - 100%) based on weighted metrics:
    - Steps: 25%
    - Water: 20%
    - Workout: 25%
    - Calorie Burn: 20%
    - Nutrition Logged: 10% (awarded if meal or calorie intake is logged)
    """
    if not log:
        return 0.0, "Getting Started"

    step_goal = goals.get("Steps", 10000)
    water_goal = goals.get("Water", 3.0)
    workout_goal = goals.get("Workout", 45)
    burn_goal = goals.get("CaloriesBurn", 400)

    steps = log.get("Steps", 0)
    water = log.get("Water", 0.0)
    workout = log.get("Workout", 0)
    burned = log.get("CaloriesBurned", 0)
    consumed = log.get("CaloriesConsumed", 0)
    meals = log.get("Meals", {})
    meal_count = sum(len(items) for items in meals.values()) if isinstance(meals, dict) else 0

    s_ratio = min(1.0, (steps / step_goal)) if step_goal > 0 else 0.0
    w_ratio = min(1.0, (water / water_goal)) if water_goal > 0 else 0.0
    wo_ratio = min(1.0, (workout / workout_goal)) if workout_goal > 0 else 0.0
    b_ratio = min(1.0, (burned / burn_goal)) if burn_goal > 0 else 0.0
    n_ratio = 1.0 if (consumed > 0 or meal_count > 0) else 0.0

    score = (s_ratio * 25.0) + (w_ratio * 20.0) + (wo_ratio * 25.0) + (b_ratio * 20.0) + (n_ratio * 10.0)
    score = min(100.0, max(0.0, score))

    if score >= 90.0:
        classification = "Excellent"
    elif score >= 75.0:
        classification = "Very Good"
    elif score >= 60.0:
        classification = "Good"
    elif score >= 40.0:
        classification = "Needs Improvement"
    else:
        classification = "Getting Started"

    return round(score, 1), classification


def progress_bar(percent, width=20):
    """Generate visual ASCII progress bar."""
    bounded = max(0.0, min(percent, 100.0))
    filled_blocks = int((bounded / 100.0) * width)
    empty_blocks = width - filled_blocks
    return "[" + "#" * filled_blocks + "-" * empty_blocks + "]"


def calculate_streak():
    """Calculate current consecutive active days streak."""
    if len(daily_logs) == 0:
        return 0

    today = date.today()
    streak = 0
    check_date = today

    today_str = str(check_date)
    if today_str not in daily_logs or (
        daily_logs[today_str].get("Steps", 0) == 0
        and daily_logs[today_str].get("Workout", 0) == 0
        and daily_logs[today_str].get("Water", 0.0) == 0.0
    ):
        check_date = today - timedelta(days=1)

    while True:
        day_str = str(check_date)
        if day_str in daily_logs:
            log = daily_logs[day_str]
            if log.get("Steps", 0) > 0 or log.get("Workout", 0) > 0 or log.get("Water", 0.0) > 0:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        else:
            break

    return streak


# ============================================================
# MOTIVATIONAL MESSAGES
# ============================================================

def get_motivational_message(score, streak, active_today=True):
    """Return a contextual, non-repetitive motivational message based on performance."""
    if streak >= 7:
        return "Incredible discipline! Your 7+ day streak is building a life-changing fitness habit."
    if score >= 90:
        return "Outstanding! You crushed virtually all of your fitness targets today."
    if score >= 75:
        return "Great progress! A small final push will help you hit 100% completion."
    if score >= 50:
        return "Good momentum! Stay consistent, drink your water, and keep moving."
    if not active_today:
        return "Don't worry about yesterday. Today is a fresh opportunity to move and hydrate!"
    return "Every single step and workout counts. Keep taking action toward your goals!"


# ============================================================
# ACHIEVEMENTS & BADGES
# ============================================================

ALL_BADGES_DEFINITIONS = [
    ("First Step", "Logged your first fitness activity.", "activity_count", 1),
    ("Early Starter", "Logged fitness activities on 3 distinct days.", "activity_count", 3),
    ("Month Champion", "Maintained active logs for 20 total days.", "activity_count", 20),
    ("Hydration Hero", "Achieved your daily water goal.", "water_goal_hit", 1),
    ("Hydration Master", "Hit your daily water goal on 7 different days.", "water_goal_hit", 7),
    ("10K Walker Club", "Walked over 10,000 steps in a single day.", "single_day_steps", 10000),
    ("Marathon Mindset", "Accumulated 50,000 total steps across all logs.", "total_steps", 50000),
    ("Century Performer", "Accumulated 100,000 all-time steps.", "total_steps", 100000),
    ("Calorie Crusher", "Burned 500+ active calories in a single day.", "single_day_burn", 500),
    ("Workout Pro", "Completed 10 total workout sessions.", "workout_count", 10),
    ("Fitness Enthusiast", "Logged 300+ total workout minutes.", "total_workout_mins", 300),
    ("Consistency Master", "Maintained a 3-day active fitness streak.", "streak", 3),
    ("7-Day Warrior", "Maintained a 7-day active fitness streak.", "streak", 7),
    ("Goal Crusher", "Scored 100% on your daily fitness score in a day.", "perfect_score", 1)
]


def check_and_unlock_badges():
    """Evaluate badge conditions and unlock new achievements."""
    global achievements
    unlocked_now = []
    unlocked_titles = [a.get("title") for a in achievements]

    total_steps = sum(v.get("Steps", 0) for v in daily_logs.values())
    total_workout_mins = sum(v.get("Workout", 0) for v in daily_logs.values())
    total_workouts_count = sum(len(v.get("Workouts", [])) for v in daily_logs.values())
    streak = calculate_streak()
    water_target = goals.get("Water", 3.0)

    water_goals_hit = sum(1 for v in daily_logs.values() if v.get("Water", 0.0) >= water_target)
    perfect_score_days = sum(1 for v in daily_logs.values() if calculate_daily_score_for_log(v)[0] >= 99.9)

    for title, desc, rule_type, threshold in ALL_BADGES_DEFINITIONS:
        if title in unlocked_titles:
            continue

        unlocked = False
        if rule_type == "activity_count" and len(daily_logs) >= threshold:
            unlocked = True
        elif rule_type == "water_goal_hit" and water_goals_hit >= threshold:
            unlocked = True
        elif rule_type == "single_day_steps" and any(v.get("Steps", 0) >= threshold for v in daily_logs.values()):
            unlocked = True
        elif rule_type == "total_steps" and total_steps >= threshold:
            unlocked = True
        elif rule_type == "single_day_burn" and any(v.get("CaloriesBurned", 0) >= threshold for v in daily_logs.values()):
            unlocked = True
        elif rule_type == "workout_count" and total_workouts_count >= threshold:
            unlocked = True
        elif rule_type == "total_workout_mins" and total_workout_mins >= threshold:
            unlocked = True
        elif rule_type == "streak" and streak >= threshold:
            unlocked = True
        elif rule_type == "perfect_score" and perfect_score_days >= threshold:
            unlocked = True

        if unlocked:
            badge_entry = {
                "title": title,
                "desc": desc,
                "date": get_today_str()
            }
            achievements.append(badge_entry)
            unlocked_now.append(badge_entry)

    if unlocked_now:
        save_data()
        for b in unlocked_now:
            print("\n" + "*" * 50)
            print(f" [NEW BADGE UNLOCKED] {b['title']}!")
            print(f"   {b['desc']}")
            print("*" * 50)


# ============================================================
# 1. USER PROFILE & HEALTH METRICS
# ============================================================

def profile_menu():
    """Submenu for user profile, health metrics, and weight tracking."""
    while True:
        print("\n" + "=" * 45)
        print("     USER PROFILE & HEALTH METRICS")
        print("=" * 45)
        print(" 1. Create / Setup Profile")
        print(" 2. View Complete Profile")
        print(" 3. Edit Profile")
        print(" 4. Calculate BMI (Body Mass Index)")
        print(" 5. Calculate BMR & TDEE (Calorie Needs)")
        print(" 6. Target Heart Rate Zones")
        print(" 7. Ideal Body Weight & Goal Projection")
        print(" 8. Weight Tracking & History")
        print(" 9. Back to Main Menu")
        print("-" * 45)

        choice = get_valid_choice("Enter Choice (1-9)", ["1", "2", "3", "4", "5", "6", "7", "8", "9"])

        if choice == "1":
            create_profile()
        elif choice == "2":
            view_profile()
        elif choice == "3":
            edit_profile()
        elif choice == "4":
            show_bmi_screen()
        elif choice == "5":
            show_bmr_tdee_screen()
        elif choice == "6":
            show_heart_rate_screen()
        elif choice == "7":
            show_ideal_weight_screen()
        elif choice == "8":
            weight_tracking_menu()
        elif choice == "9":
            break


def create_profile():
    """Setup new user profile with data validation."""
    print("\n" + "-" * 35)
    print("      Create User Profile")
    print("-" * 35)

    name = get_valid_string("Enter Name")
    age = get_valid_int("Enter Age", min_val=1, max_val=120)
    gender_choice = get_valid_choice("Enter Gender (1. Male / 2. Female / 3. Other)", ["1", "2", "3", "Male", "Female", "Other"], default="1")
    gender_map = {"1": "Male", "2": "Female", "3": "Other", "Male": "Male", "Female": "Female", "Other": "Other"}
    gender = gender_map[gender_choice]

    height = get_valid_float("Enter Height in cm", min_val=50.0, max_val=260.0)
    weight = get_valid_float("Enter Current Weight in kg", min_val=20.0, max_val=350.0)
    target_weight = get_valid_float("Enter Target Weight in kg", min_val=20.0, max_val=350.0, default=weight)

    print("\nSelect Activity Level:")
    print(" 1. Sedentary (little to no exercise)")
    print(" 2. Lightly Active (light exercise 1-3 days/week)")
    print(" 3. Moderately Active (moderate exercise 3-5 days/week)")
    print(" 4. Very Active (hard exercise 6-7 days/week)")
    print(" 5. Extra Active (very hard exercise & physical job)")
    act_choice = get_valid_choice("Choose Activity Level (1-5)", ["1", "2", "3", "4", "5"], default="3")
    act_map = {
        "1": "Sedentary",
        "2": "Lightly Active",
        "3": "Moderately Active",
        "4": "Very Active",
        "5": "Extra Active"
    }
    activity_level = act_map[act_choice]

    print("\nSelect Primary Fitness Goal:")
    for k, v in FITNESS_GOAL_TYPES.items():
        print(f" {k}. {v}")
    goal_choice = get_valid_choice("Choose Primary Goal (1-5)", ["1", "2", "3", "4", "5"], default="4")
    fitness_goal = FITNESS_GOAL_TYPES[goal_choice]

    profile["Name"] = name
    profile["Age"] = age
    profile["Gender"] = gender
    profile["Height"] = height
    profile["Weight"] = weight
    profile["StartingWeight"] = weight
    profile["TargetWeight"] = target_weight
    profile["ActivityLevel"] = activity_level
    profile["FitnessGoal"] = fitness_goal

    # Record starting weight in history
    weight_history[get_today_str()] = weight

    # Set default recommendations based on goal
    apply_fitness_goal_recommendations(fitness_goal, silent=True)

    save_data()
    check_and_unlock_badges()
    print("\n>> Profile created successfully and initial goals configured!")
    pause()


def view_profile():
    """Display user profile and key health stats."""
    if not profile:
        print("\n>> No profile found. Please create your profile first.")
        pause()
        return

    print("\n" + "=" * 45)
    print("            USER PROFILE")
    print("=" * 45)
    print(f"Name           : {profile.get('Name', 'N/A')}")
    print(f"Age            : {profile.get('Age', 'N/A')} years")
    print(f"Gender         : {profile.get('Gender', 'N/A')}")
    print(f"Height         : {profile.get('Height', 'N/A')} cm")
    print(f"Current Weight : {profile.get('Weight', 'N/A')} kg")
    print(f"Starting Weight: {profile.get('StartingWeight', profile.get('Weight', 'N/A'))} kg")
    print(f"Target Weight  : {profile.get('TargetWeight', 'N/A')} kg")
    print(f"Activity Level : {profile.get('ActivityLevel', 'N/A')}")
    print(f"Primary Goal   : {profile.get('FitnessGoal', 'General Fitness')}")

    if "Height" in profile and "Weight" in profile:
        bmi, cat, _ = calculate_bmi_value(profile["Height"], profile["Weight"])
        print(f"Current BMI    : {bmi} ({cat})")

    print("=" * 45)
    pause()


def edit_profile():
    """Edit existing profile fields while allowing user to keep existing values."""
    if not profile:
        print("\n>> Please create your profile first.")
        pause()
        return

    print("\n" + "-" * 35)
    print("        Edit Profile")
    print("-" * 35)
    print("(Press Enter on any field to keep existing value)")

    profile["Name"] = get_valid_string("Name", allow_empty=True, default=profile.get("Name", ""))
    profile["Age"] = get_valid_int("Age", min_val=1, max_val=120, default=profile.get("Age", 20))

    curr_gender = profile.get("Gender", "Male")
    gender_input = input(f"Gender (Male/Female/Other) [{curr_gender}]: ").strip().capitalize()
    if gender_input in ["Male", "Female", "Other"]:
        profile["Gender"] = gender_input

    profile["Height"] = get_valid_float("Height (cm)", min_val=50.0, max_val=260.0, default=profile.get("Height", 170.0))
    curr_weight = profile.get("Weight", 70.0)
    new_weight = get_valid_float("Weight (kg)", min_val=20.0, max_val=350.0, default=curr_weight)
    profile["Weight"] = new_weight
    weight_history[get_today_str()] = new_weight

    profile["TargetWeight"] = get_valid_float("Target Weight (kg)", min_val=20.0, max_val=350.0, default=profile.get("TargetWeight", curr_weight))

    print(f"\nCurrent Activity: {profile.get('ActivityLevel', 'Moderately Active')}")
    print("1. Sedentary | 2. Lightly Active | 3. Moderately Active | 4. Very Active | 5. Extra Active")
    act_choice = input("Change Activity Level (1-5 or press Enter to keep): ").strip()
    act_map = {
        "1": "Sedentary",
        "2": "Lightly Active",
        "3": "Moderately Active",
        "4": "Very Active",
        "5": "Extra Active"
    }
    if act_choice in act_map:
        profile["ActivityLevel"] = act_map[act_choice]

    save_data()
    print("\n>> Profile updated successfully!")
    pause()


def show_bmi_screen():
    """Display BMI calculation, classification, and health advice."""
    if not profile:
        print("\n>> Please create your profile first.")
        pause()
        return

    bmi, category, advice = calculate_bmi_value(profile.get("Height", 170.0), profile.get("Weight", 70.0))
    print("\n" + "=" * 45)
    print("          BMI (BODY MASS INDEX)")
    print("=" * 45)
    print(f"Height   : {profile.get('Height')} cm")
    print(f"Weight   : {profile.get('Weight')} kg")
    print(f"\nBMI      : {bmi}")
    print(f"Category : {category}")
    print(f"Advice   : {advice}")
    print("=" * 45)
    pause()


def show_bmr_tdee_screen():
    """Display BMR and TDEE calculation with calorie guidance."""
    if not profile:
        print("\n>> Please create your profile first.")
        pause()
        return

    bmr, tdee, multiplier = calculate_bmr_tdee_values(
        profile.get("Height", 170.0),
        profile.get("Weight", 70.0),
        profile.get("Age", 25),
        profile.get("Gender", "Male"),
        profile.get("ActivityLevel", "Moderately Active")
    )

    print("\n" + "=" * 50)
    print("       METABOLIC RATE & DAILY ENERGY NEEDS")
    print("=" * 50)
    print(f"Basal Metabolic Rate (BMR) : {bmr} kcal/day")
    print("  (Estimated calories burned by your body at rest)")
    print(f"Activity Level Multiplier  : {profile.get('ActivityLevel')} (x{multiplier})")
    print(f"Total Daily Energy (TDEE)  : {tdee} kcal/day")
    print("  (Estimated calories required to maintain current weight)")
    print("-" * 50)
    print("Recommended Calorie Targets:")
    print(f"  * Weight Loss (-400 kcal)   : {round(max(1200, tdee - 400))} kcal/day")
    print(f"  * Mild Loss   (-200 kcal)   : {round(tdee - 200)} kcal/day")
    print(f"  * Maintenance (0 kcal)      : {round(tdee)} kcal/day")
    print(f"  * Muscle Gain (+250 kcal)   : {round(tdee + 250)} kcal/day")
    print(f"  * Weight Gain (+400 kcal)   : {round(tdee + 400)} kcal/day")
    print("=" * 50)
    pause()


def show_heart_rate_screen():
    """Display target training heart rate zones."""
    if not profile:
        print("\n>> Please create your profile first.")
        pause()
        return

    age = profile.get("Age", 20)
    max_hr = 220 - age

    print("\n" + "=" * 45)
    print("         TARGET HEART RATE ZONES")
    print("=" * 45)
    print(f"Estimated Max Heart Rate : {max_hr} BPM (Beats/Min)")
    print("-" * 45)
    print(f" 1. Warm-Up  (50% - 60%) : {round(max_hr * 0.50)} - {round(max_hr * 0.60)} BPM")
    print(f" 2. Fat Burn (60% - 70%) : {round(max_hr * 0.60)} - {round(max_hr * 0.70)} BPM")
    print(f" 3. Aerobic  (70% - 85%) : {round(max_hr * 0.70)} - {round(max_hr * 0.85)} BPM")
    print(f" 4. Peak     (85%-100%)  : {round(max_hr * 0.85)} - {max_hr} BPM")
    print("=" * 45)
    pause()


def show_ideal_weight_screen():
    """Display ideal body weight and estimated timeline to reach it."""
    if not profile:
        print("\n>> Please create your profile first.")
        pause()
        return

    curr_weight = profile.get("Weight", 70.0)
    ibw = calculate_ideal_weight_value(profile.get("Height", 170.0), profile.get("Gender", "Male"))
    diff = round(curr_weight - ibw, 1)

    print("\n" + "=" * 45)
    print("       IDEAL WEIGHT & TIMELINE")
    print("=" * 45)
    print(f"Current Weight : {curr_weight} kg")
    print(f"Ideal Weight   : {ibw} kg (Devine Formula)")
    print(f"Target Weight  : {profile.get('TargetWeight', curr_weight)} kg")

    if abs(diff) <= 1.5:
        print("Status         : You are currently right around your ideal weight!")
    elif diff > 0:
        weeks = round(diff / 0.5, 1)
        print(f"Status         : +{diff} kg above ideal weight.")
        print(f"Estimated Time : ~{weeks} weeks at a safe pace of 0.5 kg/week.")
    else:
        weeks = round(abs(diff) / 0.3, 1)
        print(f"Status         : {abs(diff)} kg below ideal weight.")
        print(f"Estimated Time : ~{weeks} weeks at a safe pace of 0.3 kg/week.")

    print("=" * 45)
    pause()


# ============================================================
# WEIGHT TRACKING & HISTORY
# ============================================================

def weight_tracking_menu():
    """Weight tracking submenu."""
    while True:
        print("\n" + "-" * 35)
        print("     Weight Tracking & History")
        print("-" * 35)
        print("1. Log Today's Weight")
        print("2. Log Weight for a Specific Date")
        print("3. View Weight History & Change Summary")
        print("4. Update Target Weight")
        print("5. Back to Profile Menu")

        choice = get_valid_choice("Enter Choice (1-5)", ["1", "2", "3", "4", "5"])

        if choice == "1":
            log_weight_entry(get_today_str())
        elif choice == "2":
            target_date = get_valid_date("Enter Date (YYYY-MM-DD)", default=get_today_str())
            log_weight_entry(target_date)
        elif choice == "3":
            view_weight_history()
        elif choice == "4":
            curr_target = profile.get("TargetWeight", profile.get("Weight", 70.0))
            new_target = get_valid_float("Enter New Target Weight (kg)", min_val=20.0, max_val=350.0, default=curr_target)
            profile["TargetWeight"] = new_target
            save_data()
            print(f"\n>> Target weight updated to {new_target} kg.")
            pause()
        elif choice == "5":
            break


def log_weight_entry(date_str):
    """Log or update weight for a given date."""
    curr_weight = profile.get("Weight", 70.0)
    existing_entry = weight_history.get(date_str, curr_weight)
    weight = get_valid_float(f"Enter Weight for {date_str} (kg)", min_val=20.0, max_val=350.0, default=existing_entry)

    weight_history[date_str] = weight
    if date_str == get_today_str() or not profile.get("Weight"):
        profile["Weight"] = weight

    if "StartingWeight" not in profile:
        profile["StartingWeight"] = weight

    save_data()
    print(f"\n>> Weight logged for {date_str}: {weight} kg")
    pause()


def view_weight_history():
    """Display formatted table of weight entries and overall progress."""
    if not weight_history:
        print("\n>> No weight logs recorded yet.")
        pause()
        return

    sorted_dates = sorted(weight_history.keys())
    starting_weight = profile.get("StartingWeight", weight_history[sorted_dates[0]])
    current_weight = weight_history[sorted_dates[-1]]
    target_weight = profile.get("TargetWeight", starting_weight)
    total_change = round(current_weight - starting_weight, 2)
    to_target = round(current_weight - target_weight, 2)

    print("\n" + "=" * 50)
    print("              WEIGHT PROGRESS SUMMARY")
    print("=" * 50)
    print(f"Starting Weight : {starting_weight} kg")
    print(f"Current Weight  : {current_weight} kg")
    print(f"Target Weight   : {target_weight} kg")
    print(f"Net Change      : {'+' if total_change > 0 else ''}{total_change} kg")
    print(f"Remaining Goal  : {'+' if to_target > 0 else ''}{to_target} kg to reach target")
    print("-" * 50)
    print(f"{'Date':<14} | {'Weight (kg)':<12} | {'Change From Start'}")
    print("-" * 50)

    for d in sorted_dates:
        w = weight_history[d]
        diff_start = round(w - starting_weight, 2)
        diff_str = f"{'+' if diff_start > 0 else ''}{diff_start} kg"
        print(f"{d:<14} | {w:<12.1f} | {diff_str}")

    print("=" * 50)
    pause()


# ============================================================
# 2. FITNESS GOALS & RECOMMENDATIONS
# ============================================================

def goals_menu():
    """Submenu for setting, viewing, and configuring fitness goals."""
    while True:
        print("\n" + "=" * 45)
        print("        DAILY FITNESS GOALS")
        print("=" * 45)
        print(" 1. Select Primary Fitness Goal (Auto-Tune)")
        print(" 2. Set / Customize Daily Goals Manually")
        print(" 3. View Current Goals")
        print(" 4. Reset to Standard Healthy Goals")
        print(" 5. Back to Main Menu")
        print("-" * 45)

        choice = get_valid_choice("Enter Choice (1-5)", ["1", "2", "3", "4", "5"])

        if choice == "1":
            select_fitness_goal_type()
        elif choice == "2":
            set_goals_manually()
        elif choice == "3":
            view_goals()
        elif choice == "4":
            reset_recommended_goals()
        elif choice == "5":
            break


def apply_fitness_goal_recommendations(goal_name, silent=False):
    """Set goal parameters based on goal type and user profile."""
    height = profile.get("Height", 170.0)
    weight = profile.get("Weight", 70.0)
    age = profile.get("Age", 25)
    gender = profile.get("Gender", "Male")
    activity = profile.get("ActivityLevel", "Moderately Active")

    _, tdee, _ = calculate_bmr_tdee_values(height, weight, age, gender, activity)

    if goal_name == "Weight Loss":
        goals["Steps"] = 10000
        goals["Water"] = 3.5
        goals["Workout"] = 45
        goals["CaloriesBurn"] = 500
        goals["CaloriesIntake"] = max(1200, round(tdee - 400))
    elif goal_name == "Weight Gain":
        goals["Steps"] = 6000
        goals["Water"] = 3.0
        goals["Workout"] = 45
        goals["CaloriesBurn"] = 300
        goals["CaloriesIntake"] = round(tdee + 400)
    elif goal_name == "Muscle Building":
        goals["Steps"] = 8000
        goals["Water"] = 3.5
        goals["Workout"] = 60
        goals["CaloriesBurn"] = 450
        goals["CaloriesIntake"] = round(tdee + 250)
    elif goal_name == "Maintain Weight":
        goals["Steps"] = 8000
        goals["Water"] = 3.0
        goals["Workout"] = 30
        goals["CaloriesBurn"] = 350
        goals["CaloriesIntake"] = round(tdee)
    else:  # General Fitness
        goals["Steps"] = 8000
        goals["Water"] = 2.8
        goals["Workout"] = 30
        goals["CaloriesBurn"] = 350
        goals["CaloriesIntake"] = round(tdee)

    save_data()
    if not silent:
        print(f"\n>> Targets automatically adjusted for '{goal_name}':")
        print(f"   * Steps           : {goals['Steps']} steps/day")
        print(f"   * Water           : {goals['Water']} L/day")
        print(f"   * Workout Time    : {goals['Workout']} min/day")
        print(f"   * Calorie Burn    : {goals['CaloriesBurn']} kcal/day")
        print(f"   * Calorie Intake  : {goals['CaloriesIntake']} kcal/day")
        pause()


def select_fitness_goal_type():
    """Allow user to pick a primary fitness goal and configure targets."""
    print("\nSelect Primary Fitness Goal:")
    for k, v in FITNESS_GOAL_TYPES.items():
        print(f" {k}. {v}")

    choice = get_valid_choice("Choose Goal (1-5)", ["1", "2", "3", "4", "5"], default="4")
    goal_name = FITNESS_GOAL_TYPES[choice]
    profile["FitnessGoal"] = goal_name
    apply_fitness_goal_recommendations(goal_name, silent=False)


def set_goals_manually():
    """Prompt user to set or customize specific daily targets."""
    print("\n" + "-" * 35)
    print("   Customize Daily Targets")
    print("-" * 35)

    goals["Steps"] = get_valid_int("Daily Step Goal", min_val=500, max_val=100000, default=goals.get("Steps", 10000))
    goals["Water"] = get_valid_float("Daily Water Goal (Litres)", min_val=0.5, max_val=15.0, default=goals.get("Water", 3.0))
    goals["Workout"] = get_valid_int("Daily Workout Goal (Minutes)", min_val=5, max_val=360, default=goals.get("Workout", 45))
    goals["CaloriesBurn"] = get_valid_int("Daily Active Calorie Burn (kcal)", min_val=50, max_val=5000, default=goals.get("CaloriesBurn", 400))
    goals["CaloriesIntake"] = get_valid_int("Daily Calorie Intake Target (kcal)", min_val=800, max_val=10000, default=goals.get("CaloriesIntake", 2000))

    save_data()
    print("\n>> Goals updated and saved successfully!")
    pause()


def view_goals():
    """Display current target goals."""
    if not goals:
        print("\n>> No daily goals configured yet. Please set your goals.")
        pause()
        return

    print("\n" + "=" * 45)
    print("          CURRENT DAILY GOALS")
    print("=" * 45)
    print(f"Primary Fitness Goal   : {profile.get('FitnessGoal', 'General Fitness')}")
    print(f"Daily Step Goal        : {goals.get('Steps', 10000):,} steps")
    print(f"Daily Water Goal       : {goals.get('Water', 3.0):.2f} Litres (~{round(goals.get('Water', 3.0)/0.25)} glasses)")
    print(f"Daily Workout Goal     : {goals.get('Workout', 45)} Minutes")
    print(f"Daily Calorie Burn     : {goals.get('CaloriesBurn', 400)} kcal")
    print(f"Daily Calorie Intake   : {goals.get('CaloriesIntake', 2000)} kcal")
    print("=" * 45)
    pause()


def reset_recommended_goals():
    """Reset daily goals to standard healthy defaults."""
    goals["Steps"] = 10000
    goals["Water"] = 3.0
    goals["Workout"] = 45
    goals["CaloriesBurn"] = 450
    goals["CaloriesIntake"] = 2200
    save_data()
    print("\n>> Goals reset to standard healthy baseline (10k Steps, 3.0L Water, 45m Workout).")
    pause()


# ============================================================
# 3. ACTIVITY & NUTRITION LOGGING
# ============================================================

def log_activity_menu():
    """Submenu for logging steps, water, workouts, and meals."""
    while True:
        print("\n" + "=" * 45)
        print("    ACTIVITY & NUTRITION LOGGING")
        print("=" * 45)
        print(" 1. Log Steps Walked")
        print(" 2. Log Water Intake (Quick-Add / Glasses)")
        print(" 3. Log Workout Session (MET Calculation)")
        print(" 4. Log Food & Meals (Breakfast/Lunch/Dinner/Snack)")
        print(" 5. Quick Update All Daily Metrics")
        print(" 6. Back to Main Menu")
        print("-" * 45)

        choice = get_valid_choice("Enter Choice (1-6)", ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            log_steps()
        elif choice == "2":
            log_water()
        elif choice == "3":
            log_workout()
        elif choice == "4":
            log_meals_menu()
        elif choice == "5":
            quick_update_all()
        elif choice == "6":
            break


def log_steps():
    """Log steps walked today."""
    progress = get_today_progress()
    curr_steps = progress.get("Steps", 0)

    print("\n" + "-" * 35)
    print("         Log Steps Walked")
    print("-" * 35)
    print(f"Current Steps Today : {curr_steps:,} / {goals.get('Steps', 10000):,} steps")
    print("1. Add more steps to today's count")
    print("2. Set total steps for today")
    opt = get_valid_choice("Choose option (1/2)", ["1", "2"], default="1")

    if opt == "1":
        steps_to_add = get_valid_int("Enter Steps to Add", min_val=0, max_val=100000)
        progress["Steps"] = curr_steps + steps_to_add
    else:
        new_total = get_valid_int("Enter Total Steps Today", min_val=0, max_val=100000)
        progress["Steps"] = new_total

    save_data()
    check_and_unlock_badges()
    print(f"\n>> Steps updated! Today's Total: {progress['Steps']:,} steps.")
    pause()


def log_water():
    """Log water intake with quick-add presets, glasses counter, and goal progress."""
    progress = get_today_progress()
    curr_water = progress.get("Water", 0.0)
    target_water = goals.get("Water", 3.0)

    print("\n" + "-" * 40)
    print("          Log Water Intake")
    print("-" * 40)
    glasses = round(curr_water / 0.25, 1)
    target_glasses = round(target_water / 0.25, 1)
    print(f"Current Hydration : {curr_water:.2f} L / {target_water:.2f} L ({glasses} / {target_glasses} glasses)")
    pct = (curr_water / target_water * 100) if target_water > 0 else 0
    print(f"Progress          : {progress_bar(pct)} {pct:.1f}%")

    rem = max(0.0, target_water - curr_water)
    if rem > 0:
        print(f"Remaining Target  : {rem:.2f} Litres")
    else:
        print("Status            : Hydration Goal Completed! Excellent work!")

    print("\nQuick Options:")
    print(" 1. Add 1 Glass (250 ml / 0.25 L)")
    print(" 2. Add 1 Bottle (500 ml / 0.50 L)")
    print(" 3. Add 1 Large Bottle (1000 ml / 1.00 L)")
    print(" 4. Add Custom Litres")
    print(" 5. Set Exact Today's Total")

    opt = get_valid_choice("Choose option (1-5)", ["1", "2", "3", "4", "5"], default="1")

    if opt == "1":
        progress["Water"] = round(curr_water + 0.25, 2)
    elif opt == "2":
        progress["Water"] = round(curr_water + 0.50, 2)
    elif opt == "3":
        progress["Water"] = round(curr_water + 1.00, 2)
    elif opt == "4":
        add_l = get_valid_float("Enter Litres to add", min_val=0.0, max_val=10.0)
        progress["Water"] = round(curr_water + add_l, 2)
    elif opt == "5":
        tot_l = get_valid_float("Enter Exact Total Litres today", min_val=0.0, max_val=20.0)
        progress["Water"] = round(tot_l, 2)

    save_data()
    check_and_unlock_badges()
    print(f"\n>> Water logged! Today's Total: {progress['Water']:.2f} Litres.")
    if progress["Water"] >= target_water:
        print(">> Hydration Goal Completed for today! Stay refreshed!")
    pause()


def log_workout():
    """Log workout session with MET calculation, category, time, and notes."""
    progress = get_today_progress()
    user_weight = profile.get("Weight", 70.0)

    print("\n" + "=" * 45)
    print("        LOG WORKOUT SESSION")
    print("=" * 45)
    print("Select Activity Category:")
    for k, (name, met) in ACTIVITY_MET.items():
        print(f" {k}. {name:<32} (MET: {met})")

    act_key = get_valid_choice("Choose Activity (1-8)", list(ACTIVITY_MET.keys()), default="4")
    act_name, met_value = ACTIVITY_MET[act_key]

    duration = get_valid_int("Enter Duration in Minutes", min_val=1, max_val=360)
    duration_hours = duration / 60.0
    calc_calories = round(met_value * user_weight * duration_hours)

    print(f"\nEstimated Calories Burned: ~{calc_calories} kcal (MET: {met_value}, Weight: {user_weight} kg)")
    custom_cals = input(f"Press Enter to accept ~{calc_calories} kcal or enter custom calories burned: ").strip()
    if custom_cals != "":
        try:
            val = int(custom_cals)
            if val >= 0:
                calc_calories = val
        except ValueError:
            pass

    workout_time = input(f"Enter Time of Workout (HH:MM) [{datetime.now().strftime('%H:%M')}]: ").strip()
    if not workout_time:
        workout_time = datetime.now().strftime("%H:%M")

    note = input("Enter Short Note / Description (Optional, e.g. 'Morning run in the park'): ").strip()

    progress["Workout"] = progress.get("Workout", 0) + duration
    progress["CaloriesBurned"] = progress.get("CaloriesBurned", 0) + calc_calories

    workout_entry = {
        "Activity": act_name,
        "Duration": duration,
        "Calories": calc_calories,
        "Time": workout_time,
        "Note": note
    }
    progress["Workouts"].append(workout_entry)

    save_data()
    check_and_unlock_badges()
    print("\n>> Workout logged successfully!")
    print(f"   Today's Workout Time : {progress['Workout']} min")
    print(f"   Active Burn Today    : {progress['CaloriesBurned']} kcal")
    pause()


def log_meals_menu():
    """Food and meal logging submenu."""
    progress = get_today_progress()
    while True:
        meals = progress["Meals"]
        total_cals = progress.get("CaloriesConsumed", 0)
        target_cals = goals.get("CaloriesIntake", 2000)
        remaining_cals = target_cals - total_cals

        print("\n" + "=" * 45)
        print("       FOOD & NUTRITION LOGGING")
        print("=" * 45)
        print(f"Total Consumed Today : {total_cals} kcal / Target: {target_cals} kcal")
        print(f"Remaining Budget     : {remaining_cals} kcal ({'On Target' if remaining_cals >= 0 else 'Over Budget'})")
        print("-" * 45)
        print("1. Log Breakfast")
        print("2. Log Lunch")
        print("3. Log Dinner")
        print("4. Log Snack")
        print("5. View Today's Meal Breakdown")
        print("6. Quick Add Calorie Amount")
        print("7. Back to Logging Menu")

        choice = get_valid_choice("Enter Choice (1-7)", ["1", "2", "3", "4", "5", "6", "7"])

        meal_types = {"1": "Breakfast", "2": "Lunch", "3": "Dinner", "4": "Snack"}
        if choice in meal_types:
            meal_name = meal_types[choice]
            food_desc = get_valid_string(f"Enter Food Description for {meal_name} (e.g. Oatmeal & Banana)")
            food_cals = get_valid_int("Enter Calories (kcal)", min_val=0, max_val=5000)

            item = {
                "Description": food_desc,
                "Calories": food_cals,
                "Time": datetime.now().strftime("%H:%M")
            }
            meals[meal_name].append(item)
            progress["CaloriesConsumed"] = sum(
                sum(i.get("Calories", 0) for i in items)
                for items in meals.values()
            )
            save_data()
            print(f"\n>> {meal_name} logged ({food_desc} - {food_cals} kcal).")
            pause()

        elif choice == "5":
            view_today_meals()
        elif choice == "6":
            curr_c = progress.get("CaloriesConsumed", 0)
            add_c = get_valid_int("Enter Additional Calories (kcal)", min_val=0, max_val=5000)
            progress["CaloriesConsumed"] = curr_c + add_c
            save_data()
            print(f"\n>> Calories updated! Total Consumed: {progress['CaloriesConsumed']} kcal.")
            pause()
        elif choice == "7":
            break


def view_today_meals():
    """Display breakdown of logged meals for today."""
    progress = get_today_progress()
    meals = progress.get("Meals", {})

    print("\n" + "=" * 50)
    print("           TODAY'S MEAL BREAKDOWN")
    print("=" * 50)
    has_meals = False
    for meal_type in ["Breakfast", "Lunch", "Dinner", "Snack"]:
        items = meals.get(meal_type, [])
        print(f"\n[{meal_type.upper()}]")
        if not items:
            print("  (No items logged)")
        else:
            has_meals = True
            for idx, item in enumerate(items, 1):
                t = item.get("Time", "--:--")
                d = item.get("Description", "Food Item")
                c = item.get("Calories", 0)
                print(f"  {idx}. [{t}] {d} - {c} kcal")

    tot = progress.get("CaloriesConsumed", 0)
    target = goals.get("CaloriesIntake", 2000)
    print("\n" + "-" * 50)
    print(f"Total Consumed : {tot} kcal")
    print(f"Daily Target   : {target} kcal")
    print(f"Remaining      : {target - tot} kcal")
    print("=" * 50)
    pause()


def quick_update_all():
    """Update all core daily metrics in a single quick form."""
    progress = get_today_progress()
    print("\n" + "=" * 45)
    print("    QUICK UPDATE ALL DAILY METRICS")
    print("=" * 45)

    progress["Steps"] = get_valid_int("Total Steps Today", min_val=0, max_val=100000, default=progress.get("Steps", 0))
    progress["Water"] = get_valid_float("Total Water Today (Litres)", min_val=0.0, max_val=20.0, default=progress.get("Water", 0.0))
    progress["Workout"] = get_valid_int("Total Workout Today (Minutes)", min_val=0, max_val=360, default=progress.get("Workout", 0))
    progress["CaloriesBurned"] = get_valid_int("Total Active Calorie Burn (kcal)", min_val=0, max_val=5000, default=progress.get("CaloriesBurned", 0))
    progress["CaloriesConsumed"] = get_valid_int("Total Calories Consumed (kcal)", min_val=0, max_val=10000, default=progress.get("CaloriesConsumed", 0))

    save_data()
    check_and_unlock_badges()
    print("\n>> All today's fitness metrics successfully updated & saved!")
    pause()


# ============================================================
# 4. TODAY'S PROGRESS DASHBOARD
# ============================================================

def view_progress():
    """Display comprehensive dashboard for today's fitness progress."""
    if not goals:
        print("\n>> Please configure your daily goals first.")
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

    score, classification = calculate_daily_score_for_log(progress)
    streak = calculate_streak()

    print("\n" + "=" * 60)
    print(f"        TODAY'S FITNESS DASHBOARD ({today_str})")
    print(f"        Welcome back, {profile.get('Name', 'Athlete')}!")
    print("=" * 60)

    # STEPS
    rem_steps = max(0, step_goal - steps)
    print(f"Steps Walked    : {steps:>6,} / {step_goal:,} steps")
    print(f"  {progress_bar(step_pct)} {step_pct:>5.1f}% (Remaining: {rem_steps:,})")

    # WATER
    rem_water = max(0.0, water_goal - water)
    glasses = round(water / 0.25, 1)
    print(f"\nWater Intake    : {water:>6.2f} / {water_goal:.2f} Litres ({glasses} glasses)")
    print(f"  {progress_bar(water_pct)} {water_pct:>5.1f}% (Remaining: {rem_water:.2f} L)")

    # WORKOUT
    rem_workout = max(0, workout_goal - workout)
    print(f"\nWorkout Time    : {workout:>6} / {workout_goal} Minutes")
    print(f"  {progress_bar(workout_pct)} {workout_pct:>5.1f}% (Remaining: {rem_workout} min)")

    # CALORIE BURN
    rem_burn = max(0, burn_goal - burned)
    print(f"\nCalories Burned : {burned:>6} / {burn_goal} kcal")
    print(f"  {progress_bar(burn_pct)} {burn_pct:>5.1f}% (Remaining: {rem_burn} kcal)")

    # CALORIE INTAKE & NET BALANCE
    net_cals = consumed - burned
    rem_intake = intake_goal - consumed
    print(f"\nNutrition / Food: {consumed} kcal consumed (Target: {intake_goal} kcal | Budget left: {rem_intake} kcal)")
    print(f"Net Calorie Bal : {'+' if net_cals > 0 else ''}{net_cals} kcal (Intake - Active Burn)")

    # WORKOUT SESSIONS
    workouts_list = progress.get("Workouts", [])
    if workouts_list:
        print("\nToday's Workout Sessions:")
        for idx, w in enumerate(workouts_list, 1):
            note_str = f" | Note: {w['Note']}" if w.get("Note") else ""
            print(f"  * [{w.get('Time', '--:--')}] {w.get('Activity')} ({w.get('Duration')} min, ~{w.get('Calories')} kcal){note_str}")

    # SCORE & STREAK SUMMARY
    print("\n" + "-" * 60)
    print(f"DAILY FITNESS SCORE : {score}% [{classification}]")
    print(f"CURRENT STREAK      : {streak} Day{'s' if streak != 1 else ''} | Badges Unlocked: {len(achievements)}")
    print("-" * 60)
    print(f"Status Motivation  : \"{get_motivational_message(score, streak)}\"")
    print("=" * 60)

    check_and_unlock_badges()
    pause()


# ============================================================
# 5. HISTORY & ANALYTICS
# ============================================================

def history_menu():
    """Submenu for browsing past logs, weekly analytics, and all-time statistics."""
    while True:
        print("\n" + "=" * 45)
        print("        HISTORY & ANALYTICS")
        print("=" * 45)
        print(" 1. View Today's Detailed Log")
        print(" 2. View Yesterday's Log")
        print(" 3. View Past 7 Days Summary Table")
        print(" 4. Weekly Performance Analysis & Insights")
        print(" 5. Search Specific Date Log (YYYY-MM-DD)")
        print(" 6. View All History Table")
        print(" 7. View All-Time Fitness Records & Stats")
        print(" 8. Back to Main Menu")
        print("-" * 45)

        choice = get_valid_choice("Enter Choice (1-8)", ["1", "2", "3", "4", "5", "6", "7", "8"])

        if choice == "1":
            display_single_date_log(get_today_str())
        elif choice == "2":
            yesterday_str = str(date.today() - timedelta(days=1))
            display_single_date_log(yesterday_str)
        elif choice == "3":
            view_weekly_summary_table()
        elif choice == "4":
            view_weekly_performance_analysis()
        elif choice == "5":
            target_date = get_valid_date("Enter Date to Search (YYYY-MM-DD)", default=get_today_str())
            display_single_date_log(target_date)
        elif choice == "6":
            view_all_history_table()
        elif choice == "7":
            view_all_time_stats()
        elif choice == "8":
            break


def display_single_date_log(date_str):
    """Display full details for a specified date log."""
    if date_str not in daily_logs:
        print(f"\n>> No fitness log recorded for date: {date_str}")
        pause()
        return

    log = daily_logs[date_str]
    score, classification = calculate_daily_score_for_log(log)

    print("\n" + "=" * 50)
    print(f"          FITNESS LOG: {date_str}")
    print("=" * 50)
    print(f"Steps Walked      : {log.get('Steps', 0):,} steps")
    print(f"Water Intake      : {log.get('Water', 0.0):.2f} Litres")
    print(f"Workout Duration  : {log.get('Workout', 0)} Minutes")
    print(f"Calories Burned   : {log.get('CaloriesBurned', 0)} kcal")
    print(f"Calories Consumed : {log.get('CaloriesConsumed', 0)} kcal")
    print(f"Daily Score       : {score}% ({classification})")

    # Weight on that day if recorded
    if date_str in weight_history:
        print(f"Recorded Weight   : {weight_history[date_str]} kg")

    workouts = log.get("Workouts", [])
    if workouts:
        print("\nWorkout Sessions:")
        for idx, w in enumerate(workouts, 1):
            note = f" - {w['Note']}" if w.get("Note") else ""
            print(f"  {idx}. [{w.get('Time', '--:--')}] {w.get('Activity')} ({w.get('Duration')} min, ~{w.get('Calories')} kcal){note}")

    meals = log.get("Meals", {})
    has_meals = any(len(items) > 0 for items in meals.values()) if isinstance(meals, dict) else False
    if has_meals:
        print("\nMeals Logged:")
        for m_type in ["Breakfast", "Lunch", "Dinner", "Snack"]:
            for item in meals.get(m_type, []):
                print(f"  * [{m_type}] {item.get('Description')} ({item.get('Calories')} kcal)")

    print("=" * 50)
    pause()


def view_weekly_summary_table():
    """Display table of the past 7 days activity."""
    if not daily_logs:
        print("\n>> No historical logs recorded yet.")
        pause()
        return

    print("\n" + "=" * 72)
    print("                    PAST 7 DAYS ACTIVITY SUMMARY")
    print("=" * 72)
    print(f"{'Date':<12} | {'Steps':<8} | {'Water(L)':<8} | {'Workout':<8} | {'Burned':<7} | {'Score'}")
    print("-" * 72)

    today = date.today()
    for i in range(6, -1, -1):
        d_str = str(today - timedelta(days=i))
        if d_str in daily_logs:
            log = daily_logs[d_str]
            st = log.get("Steps", 0)
            wa = log.get("Water", 0.0)
            wo = log.get("Workout", 0)
            bu = log.get("CaloriesBurned", 0)
            sc, _ = calculate_daily_score_for_log(log)
            print(f"{d_str:<12} | {st:<8,} | {wa:<8.2f} | {wo:<5} min | {bu:<4} kcal | {sc:>5.1f}%")
        else:
            print(f"{d_str:<12} | {'--':<8} | {'--':<8} | {'--':<8} | {'--':<7} | {'--'}")

    print("=" * 72)
    pause()


def view_weekly_performance_analysis():
    """Perform in-depth 7-day analytics, best days calculation, and recommendations."""
    today = date.today()
    past_7_dates = [str(today - timedelta(days=i)) for i in range(7)]

    active_logs = []
    for d in past_7_dates:
        if d in daily_logs:
            active_logs.append((d, daily_logs[d]))

    print("\n" + "=" * 55)
    print("             WEEKLY PERFORMANCE ANALYSIS")
    print("=" * 55)

    if not active_logs:
        print("No active logs recorded in the past 7 days.")
        print("Start logging your daily metrics to see weekly analytics!")
        print("=" * 55)
        pause()
        return

    active_days_count = len(active_logs)
    total_steps = sum(log.get("Steps", 0) for _, log in active_logs)
    total_water = sum(log.get("Water", 0.0) for _, log in active_logs)
    total_workout = sum(log.get("Workout", 0) for _, log in active_logs)
    total_burned = sum(log.get("CaloriesBurned", 0) for _, log in active_logs)
    total_consumed = sum(log.get("CaloriesConsumed", 0) for _, log in active_logs)

    scores = [calculate_daily_score_for_log(log)[0] for _, log in active_logs]
    avg_score = round(sum(scores) / len(scores), 1)

    avg_steps = round(total_steps / active_days_count)
    avg_water = round(total_water / active_days_count, 2)
    avg_workout = round(total_workout / active_days_count, 1)
    avg_burned = round(total_burned / active_days_count)
    avg_consumed = round(total_consumed / active_days_count)

    best_step_entry = max(active_logs, key=lambda x: x[1].get("Steps", 0))
    best_workout_entry = max(active_logs, key=lambda x: x[1].get("Workout", 0))
    best_overall_entry = max(active_logs, key=lambda x: calculate_daily_score_for_log(x[1])[0])

    step_day_name = datetime.strptime(best_step_entry[0], "%Y-%m-%d").strftime("%A")
    workout_day_name = datetime.strptime(best_workout_entry[0], "%Y-%m-%d").strftime("%A")
    overall_day_name = datetime.strptime(best_overall_entry[0], "%Y-%m-%d").strftime("%A")

    print(f"Active Days          : {active_days_count} / 7 days")
    print(f"Average Steps        : {avg_steps:,} steps/day")
    print(f"Average Water        : {avg_water} Litres/day")
    print(f"Average Workout Time : {avg_workout} Minutes/day")
    print(f"Average Calories Burn: {avg_burned} kcal/day")
    print(f"Average Intake       : {avg_consumed} kcal/day")
    print("-" * 55)
    print(f"Best Step Day        : {step_day_name} ({best_step_entry[1].get('Steps', 0):,} steps)")
    print(f"Best Workout Day     : {workout_day_name} ({best_workout_entry[1].get('Workout', 0)} min)")
    print(f"Best Overall Day     : {overall_day_name} (Score: {calculate_daily_score_for_log(best_overall_entry[1])[0]}%)")
    print(f"Weekly Fitness Score : {avg_score}%")
    print("-" * 55)

    # Rule-based simple recommendations
    print("Recommendation:")
    water_target = goals.get("Water", 3.0)
    step_target = goals.get("Steps", 10000)
    if avg_water < water_target * 0.8:
        print("  * Your hydration is slightly below target. Try keeping a water bottle nearby.")
    elif avg_steps < step_target * 0.8:
        print("  * Step count is lower than your target. Add a 15-minute brisk walk after meals.")
    elif active_days_count >= 5:
        print("  * Outstanding consistency this week! Maintain your momentum and sleep well.")
    else:
        print("  * Focus on building regularity by logging at least 5 active days next week.")

    print("=" * 55)
    pause()


def view_all_history_table():
    """Display complete chronological table of all stored logs."""
    if not daily_logs:
        print("\n>> No historical logs recorded yet.")
        pause()
        return

    print("\n" + "=" * 80)
    print("                         COMPLETE LOG HISTORY")
    print("=" * 80)
    print(f"{'Date':<12} | {'Steps':<8} | {'Water(L)':<8} | {'Workout':<9} | {'Burned':<7} | {'Intake':<7} | {'Score'}")
    print("-" * 80)

    for d in sorted(daily_logs.keys(), reverse=True):
        log = daily_logs[d]
        st = log.get("Steps", 0)
        wa = log.get("Water", 0.0)
        wo = log.get("Workout", 0)
        bu = log.get("CaloriesBurned", 0)
        co = log.get("CaloriesConsumed", 0)
        sc, _ = calculate_daily_score_for_log(log)
        print(f"{d:<12} | {st:<8,} | {wa:<8.2f} | {wo:<6} min | {bu:<4} kcal | {co:<4} kcal | {sc:>5.1f}%")

    print("=" * 80)
    pause()


def view_all_time_stats():
    """Display all-time accumulated statistics and personal bests."""
    if not daily_logs:
        print("\n>> No logged history available yet.")
        pause()
        return

    total_days = len(daily_logs)
    total_steps = sum(v.get("Steps", 0) for v in daily_logs.values())
    total_water = sum(v.get("Water", 0.0) for v in daily_logs.values())
    total_workout = sum(v.get("Workout", 0) for v in daily_logs.values())
    total_burned = sum(v.get("CaloriesBurned", 0) for v in daily_logs.values())
    total_consumed = sum(v.get("CaloriesConsumed", 0) for v in daily_logs.values())

    print("\n" + "=" * 50)
    print("            ALL-TIME FITNESS STATISTICS")
    print("=" * 50)
    print(f"Total Logged Days     : {total_days} days")
    print(f"Total Steps Walked    : {total_steps:,} steps")
    print(f"Total Water Intake    : {round(total_water, 2)} Litres")
    print(f"Total Workout Time    : {total_workout:,} Minutes ({round(total_workout/60, 1)} hours)")
    print(f"Total Calories Burned : {total_burned:,} kcal")
    print(f"Total Calories Intake : {total_consumed:,} kcal")
    print("=" * 50)
    pause()


# ============================================================
# 6. FITNESS INSIGHTS
# ============================================================

def view_fitness_insights():
    """Generate dynamic automated observations from stored historical data."""
    print("\n" + "=" * 55)
    print("                FITNESS INSIGHTS")
    print("=" * 55)

    if not daily_logs:
        print(">> Not enough data yet to generate insights.")
        print("   Log your daily workouts, steps, and water to see smart insights!")
        print("=" * 55)
        pause()
        return

    today = date.today()
    past_7_dates = [str(today - timedelta(days=i)) for i in range(7)]
    past_7_logs = [daily_logs[d] for d in past_7_dates if d in daily_logs]

    insights = []

    # Streak observation
    streak = calculate_streak()
    if streak >= 3:
        insights.append(f"Your current streak is {streak} consecutive days of fitness activity.")
    elif streak == 1:
        insights.append("You have started a 1-day active streak. Keep the momentum going tomorrow!")
    else:
        insights.append("No active streak currently. Log an activity today to start a new streak!")

    # Weekly steps observation
    if past_7_logs:
        avg_steps = round(sum(l.get("Steps", 0) for l in past_7_logs) / len(past_7_logs))
        insights.append(f"You averaged {avg_steps:,} steps per day over the past week.")

        # Water consistency
        water_target = goals.get("Water", 3.0)
        water_hit_days = sum(1 for l in past_7_logs if l.get("Water", 0.0) >= water_target)
        insights.append(f"You achieved your water goal on {water_hit_days} of the last {len(past_7_logs)} active days.")

        # Best day of the week
        best_day_tuple = max(
            ((d, l.get("Steps", 0)) for d, l in daily_logs.items()),
            key=lambda x: x[1],
            default=("N/A", 0)
        )
        if best_day_tuple[0] != "N/A":
            day_name = datetime.strptime(best_day_tuple[0], "%Y-%m-%d").strftime("%A")
            insights.append(f"Your highest recorded activity day was {day_name} with {best_day_tuple[1]:,} steps.")

    # Weight trend observation
    if len(weight_history) >= 2:
        sorted_weights = [weight_history[d] for d in sorted(weight_history.keys())]
        w_diff = round(sorted_weights[-1] - sorted_weights[0], 2)
        if w_diff < 0:
            insights.append(f"You have reduced {abs(w_diff)} kg since your first recorded weight entry.")
        elif w_diff > 0:
            insights.append(f"You have gained {w_diff} kg since your first recorded weight entry.")
        else:
            insights.append("Your weight has remained stable across your recorded logs.")

    # Badges observation
    insights.append(f"You have unlocked {len(achievements)} of {len(ALL_BADGES_DEFINITIONS)} available achievement badges.")

    for idx, ins in enumerate(insights, 1):
        print(f" {idx}. {ins}")

    print("=" * 55)
    pause()


# ============================================================
# 7. STREAKS & ACHIEVEMENTS
# ============================================================

def streaks_and_badges_menu():
    """Display current streak, unlocked badges, and available milestones."""
    streak = calculate_streak()
    check_and_unlock_badges()

    print("\n" + "=" * 55)
    print("         STREAKS & ACHIEVEMENT BADGES")
    print("=" * 55)
    print(f"Current Fitness Streak : {streak} Day{'s' if streak != 1 else ''} in a row!")
    if streak >= 7:
        print("  Status: Incredible consistency! You are building an elite habit!")
    elif streak >= 3:
        print("  Status: Solid streak! Keep moving every day!")
    else:
        print("  Status: Log steps, workouts, or water daily to build your streak.")

    print("\nUnlocked Badges:")
    print("-" * 55)
    if not achievements:
        print("  (No badges unlocked yet. Start logging workouts and steps to earn awards!)")
    else:
        for a in achievements:
            print(f"  [*] {a['title']} (Unlocked: {a.get('date', 'N/A')})")
            print(f"      {a['desc']}")

    print("\nAvailable Milestones:")
    print("-" * 55)
    unlocked_titles = [a["title"] for a in achievements]
    for title, desc, _, _ in ALL_BADGES_DEFINITIONS:
        status = "[UNLOCKED]" if title in unlocked_titles else "[LOCKED]"
        print(f"  - {title:<20} : {desc:<45} {status}")

    print("=" * 55)
    pause()


# ============================================================
# 8. PERSONAL BESTS & RECORDS
# ============================================================

def view_personal_bests():
    """Display user's all-time personal bests and records."""
    print("\n" + "=" * 55)
    print("              PERSONAL RECORDS & BESTS")
    print("=" * 55)

    if not daily_logs:
        print(">> No logged data found to compute personal bests.")
        print("=" * 55)
        pause()
        return

    max_steps_entry = max(daily_logs.items(), key=lambda x: x[1].get("Steps", 0), default=("N/A", {}))
    max_workout_entry = max(daily_logs.items(), key=lambda x: x[1].get("Workout", 0), default=("N/A", {}))
    max_burn_entry = max(daily_logs.items(), key=lambda x: x[1].get("CaloriesBurned", 0), default=("N/A", {}))
    max_water_entry = max(daily_logs.items(), key=lambda x: x[1].get("Water", 0.0), default=("N/A", {}))
    max_score_entry = max(daily_logs.items(), key=lambda x: calculate_daily_score_for_log(x[1])[0], default=("N/A", {}))

    streak = calculate_streak()

    print(f"Highest Steps in One Day : {max_steps_entry[1].get('Steps', 0):,} steps (on {max_steps_entry[0]})")
    print(f"Longest Workout Session  : {max_workout_entry[1].get('Workout', 0)} mins (on {max_workout_entry[0]})")
    print(f"Highest Calorie Burn     : {max_burn_entry[1].get('CaloriesBurned', 0)} kcal (on {max_burn_entry[0]})")
    print(f"Highest Water Intake     : {max_water_entry[1].get('Water', 0.0):.2f} Litres (on {max_water_entry[0]})")
    print(f"Highest Daily Score      : {calculate_daily_score_for_log(max_score_entry[1])[0]}% (on {max_score_entry[0]})")
    print(f"Current Active Streak    : {streak} days")
    print("=" * 55)
    pause()


# ============================================================
# 9. REPORTS & CSV EXPORT
# ============================================================

def reports_menu():
    """Submenu for generating text summary reports and CSV data export."""
    while True:
        print("\n" + "=" * 45)
        print("         REPORTS & EXPORT")
        print("=" * 45)
        print(" 1. Export Fitness Summary Report (TXT)")
        print(" 2. Export Activity History to CSV")
        print(" 3. View Report File Location")
        print(" 4. Back to Main Menu")
        print("-" * 45)

        choice = get_valid_choice("Enter Choice (1-4)", ["1", "2", "3", "4"])

        if choice == "1":
            export_txt_report()
        elif choice == "2":
            export_history_csv()
        elif choice == "3":
            print("\nExported Files Location:")
            print(f"  * TXT Report : {os.path.abspath(REPORT_FILE)}")
            print(f"  * CSV Export : {os.path.abspath(CSV_FILE)}")
            pause()
        elif choice == "4":
            break


def export_txt_report():
    """Export clean, comprehensive text report formatted for printing or submission."""
    if not profile and not daily_logs:
        print("\n>> No profile or log data to export.")
        pause()
        return

    today_str = get_today_str()
    streak = calculate_streak()

    lines = []
    lines.append("=" * 65)
    lines.append("           FITNESS GOAL TRACKER - SUMMARY REPORT")
    lines.append(f"           Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"           Version: {APP_VERSION}")
    lines.append("=" * 65)

    lines.append("\n[1] USER PROFILE & HEALTH METRICS")
    lines.append("-" * 40)
    lines.append(f"Name            : {profile.get('Name', 'N/A')}")
    lines.append(f"Age             : {profile.get('Age', 'N/A')} years")
    lines.append(f"Gender          : {profile.get('Gender', 'N/A')}")
    lines.append(f"Height          : {profile.get('Height', 'N/A')} cm")
    lines.append(f"Current Weight  : {profile.get('Weight', 'N/A')} kg")
    lines.append(f"Starting Weight : {profile.get('StartingWeight', profile.get('Weight', 'N/A'))} kg")
    lines.append(f"Target Weight   : {profile.get('TargetWeight', 'N/A')} kg")
    lines.append(f"Activity Level  : {profile.get('ActivityLevel', 'N/A')}")
    lines.append(f"Primary Goal    : {profile.get('FitnessGoal', 'General Fitness')}")

    if "Height" in profile and "Weight" in profile:
        bmi, cat, _ = calculate_bmi_value(profile["Height"], profile["Weight"])
        lines.append(f"BMI Score       : {bmi} ({cat})")

    lines.append("\n[2] DAILY TARGET GOALS")
    lines.append("-" * 40)
    lines.append(f"Daily Steps Goal       : {goals.get('Steps', 'Not Set')} steps")
    lines.append(f"Daily Water Goal       : {goals.get('Water', 'Not Set')} Litres")
    lines.append(f"Daily Workout Goal     : {goals.get('Workout', 'Not Set')} Minutes")
    lines.append(f"Daily Calorie Burn     : {goals.get('CaloriesBurn', 'Not Set')} kcal")
    lines.append(f"Daily Calorie Intake   : {goals.get('CaloriesIntake', 'Not Set')} kcal")

    lines.append("\n[3] STREAK & ACHIEVEMENTS")
    lines.append("-" * 40)
    lines.append(f"Current Active Streak  : {streak} Days")
    lines.append(f"Total Badges Unlocked  : {len(achievements)} / {len(ALL_BADGES_DEFINITIONS)}")
    for a in achievements:
        lines.append(f"  * {a['title']} - {a['desc']} ({a.get('date', 'N/A')})")

    lines.append("\n[4] RECENT DAILY ACTIVITY LOGS")
    lines.append("-" * 65)
    lines.append(f"{'Date':<12} | {'Steps':<8} | {'Water(L)':<8} | {'Workout':<8} | {'Burned':<7} | {'Score'}")
    lines.append("-" * 65)

    for d, log in sorted(daily_logs.items(), reverse=True):
        st = log.get("Steps", 0)
        wa = log.get("Water", 0.0)
        wo = log.get("Workout", 0)
        bu = log.get("CaloriesBurned", 0)
        sc, _ = calculate_daily_score_for_log(log)
        lines.append(f"{d:<12} | {st:<8,} | {wa:<8.2f} | {wo:<5} min | {bu:<4} kcal | {sc:>5.1f}%")

    lines.append("\n" + "=" * 65)
    lines.append("                  END OF FITNESS REPORT")
    lines.append("=" * 65 + "\n")

    report_content = "\n".join(lines)
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report_content)
        print("\n" + "=" * 55)
        print(" Fitness report successfully exported to:")
        print(f" >> {os.path.abspath(REPORT_FILE)}")
        print("=" * 55)
    except Exception as e:
        print(f"\n>> Error exporting report: {e}")

    pause()


def export_history_csv():
    """Export complete activity log history to a clean CSV file."""
    if not daily_logs:
        print("\n>> No activity logs to export to CSV.")
        pause()
        return

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Steps", "Water_L", "Workout_Min", "CaloriesBurned", "CaloriesConsumed", "DailyScore_Pct"])
            for d in sorted(daily_logs.keys()):
                log = daily_logs[d]
                sc, _ = calculate_daily_score_for_log(log)
                writer.writerow([
                    d,
                    log.get("Steps", 0),
                    log.get("Water", 0.0),
                    log.get("Workout", 0),
                    log.get("CaloriesBurned", 0),
                    log.get("CaloriesConsumed", 0),
                    sc
                ])

        print("\n" + "=" * 55)
        print(" Activity history exported successfully to CSV:")
        print(f" >> {os.path.abspath(CSV_FILE)}")
        print("=" * 55)
    except Exception as e:
        print(f"\n>> Error exporting to CSV: {e}")

    pause()


# ============================================================
# 10. DATA & BACKUP SETTINGS
# ============================================================

def data_settings_menu():
    """Submenu for manual save, reload, backup, restore, and reset."""
    while True:
        print("\n" + "=" * 45)
        print("      DATA & BACKUP SETTINGS")
        print("=" * 45)
        print(f"Primary Data File: {os.path.abspath(DATA_FILE)}")
        print(f"Backup Data File : {os.path.abspath(BACKUP_FILE)}")
        print("-" * 45)
        print(" 1. Save Data Now")
        print(" 2. Reload Data from File")
        print(" 3. Backup Data to Backup File")
        print(" 4. Restore Data from Backup File")
        print(" 5. Reset / Clear All Data")
        print(" 6. Back to Main Menu")
        print("-" * 45)

        choice = get_valid_choice("Enter Choice (1-6)", ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            save_data(silent=False)
            pause()
        elif choice == "2":
            load_data()
            print("\n>> Data reloaded successfully from storage.")
            pause()
        elif choice == "3":
            save_data(silent=True)
            create_backup()
            pause()
        elif choice == "4":
            confirm = input("\nAre you SURE you want to restore from backup? Current unsaved changes will be replaced. (yes/no): ").strip().lower()
            if confirm == "yes":
                restore_backup()
            else:
                print(">> Restore canceled.")
            pause()
        elif choice == "5":
            confirm = input("\nAre you SURE you want to delete all profile, goals, and activity data? (yes/no): ").strip().lower()
            if confirm == "yes":
                global profile, goals, daily_logs, weight_history, achievements
                profile = {}
                goals = {}
                daily_logs = {}
                weight_history = {}
                achievements = []
                if os.path.exists(DATA_FILE):
                    try:
                        os.remove(DATA_FILE)
                    except Exception:
                        pass
                print("\n>> All data has been successfully reset.")
            else:
                print(">> Reset canceled.")
            pause()
        elif choice == "6":
            break


# ============================================================
# 11. HELP & ABOUT
# ============================================================

def show_help_and_about():
    """Display project metadata, architecture summary, and user guide."""
    print("\n" + "=" * 60)
    print("                    HELP & ABOUT")
    print(f"       {APP_NAME} - Version {APP_VERSION}")
    print(f"         {APP_SUBTITLE}")
    print("=" * 60)
    print("Purpose:")
    print("  A complete terminal-based personal fitness management system")
    print("  designed to assist users in tracking workouts, steps, water,")
    print("  nutrition, weight history, and daily fitness performance.")
    print("\nKey Features:")
    print("  * Health Metrics: BMI, BMR/TDEE (Mifflin-St Jeor), Devine Ideal Weight,")
    print("    Target Heart Rate Zones, Weight History.")
    print("  * Fitness Goals: Weight Loss, Muscle Building, Weight Gain, etc.")
    print("  * Activity Logging: MET-based workout burn calculation, steps,")
    print("    quick-add water glasses, categorized meal logging.")
    print("  * Analytics: Past 7 days summaries, Weekly performance analysis,")
    print("    Personal records/bests, and Automated fitness insights.")
    print("  * Gamification: Daily Fitness Score (0-100%), streaks, and 14 badges.")
    print("  * Storage & Export: Safe JSON storage with automated backups,")
    print("    professional TXT summary reports, and CSV data exports.")
    print("\nTechnology Used:")
    print("  * Python 3 Standard Library (json, csv, datetime, os, shutil, sys)")
    print("  * Zero external heavy dependencies required.")
    print("=" * 60)
    pause()


# ============================================================
# MAIN DASHBOARD / SUMMARY
# ============================================================

def display_main_header_dashboard():
    """Display compact, informative dashboard summary on application menu start."""
    today_progress = get_today_progress()
    today_str = get_today_str()

    steps = today_progress.get("Steps", 0)
    step_goal = goals.get("Steps", 10000)

    water = today_progress.get("Water", 0.0)
    water_goal = goals.get("Water", 3.0)

    workout = today_progress.get("Workout", 0)
    workout_goal = goals.get("Workout", 45)

    burned = today_progress.get("CaloriesBurned", 0)
    burn_goal = goals.get("CaloriesBurn", 400)

    score, classification = calculate_daily_score_for_log(today_progress)
    streak = calculate_streak()
    user_name = profile.get("Name", "Athlete")

    print("\n" + "=" * 55)
    print(f"             {APP_NAME}")
    print(f"                   Version {APP_VERSION}")
    print("=" * 55)
    print(f"Welcome, {user_name} | {today_str}")
    print("-" * 55)
    print("Today's Summary:")
    print(f"  Steps         : {steps:,} / {step_goal:,}")
    print(f"  Water         : {water:.1f} / {water_goal:.1f} L")
    print(f"  Workout       : {workout} / {workout_goal} min")
    print(f"  Calories Burn : {burned} / {burn_goal} kcal")
    print(f"  Daily Score   : {score}% ({classification})")
    print(f"  Current Streak: {streak} Day{'s' if streak != 1 else ''} | Badges: {len(achievements)}")
    print(f"  Status        : \"{get_motivational_message(score, streak)}\"")
    print("=" * 55)


def display_main_menu():
    """Display the primary 12-item menu."""
    print(" 1. User Profile & Health Metrics")
    print(" 2. Fitness Goals & Recommendations")
    print(" 3. Activity & Nutrition Logging")
    print(" 4. Today's Progress Dashboard")
    print(" 5. History & Analytics")
    print(" 6. Fitness Insights")
    print(" 7. Streaks & Achievements")
    print(" 8. Personal Bests")
    print(" 9. Reports & Export (TXT / CSV)")
    print("10. Data & Backup Settings")
    print("11. Help & About")
    print("12. Exit")
    print("-" * 55)


# ============================================================
# MAIN PROGRAM LOOP
# ============================================================

def main():
    """Application entry point."""
    load_data()
    check_and_unlock_badges()

    while True:
        display_main_header_dashboard()
        display_main_menu()

        choice = get_valid_choice("Enter Choice (1-12)", [str(i) for i in range(1, 13)])

        # 1. USER PROFILE & HEALTH METRICS
        if choice == "1":
            profile_menu()

        # 2. FITNESS GOALS
        elif choice == "2":
            goals_menu()

        # 3. ACTIVITY & NUTRITION LOGGING
        elif choice == "3":
            log_activity_menu()

        # 4. TODAY'S DASHBOARD
        elif choice == "4":
            view_progress()

        # 5. HISTORY & ANALYTICS
        elif choice == "5":
            history_menu()

        # 6. FITNESS INSIGHTS
        elif choice == "6":
            view_fitness_insights()

        # 7. STREAKS & ACHIEVEMENTS
        elif choice == "7":
            streaks_and_badges_menu()

        # 8. PERSONAL BESTS
        elif choice == "8":
            view_personal_bests()

        # 9. REPORTS & EXPORT
        elif choice == "9":
            reports_menu()

        # 10. DATA & BACKUP SETTINGS
        elif choice == "10":
            data_settings_menu()

        # 11. HELP & ABOUT
        elif choice == "11":
            show_help_and_about()

        # 12. EXIT
        elif choice == "12":
            save_data(silent=True)
            print("\n" + "=" * 55)
            print(" Thank you for using Fitness Goal Tracker!")
            print(" Your data has been safely saved.")
            print(" Stay consistent, stay hydrated, and have a great day!")
            print("=" * 55 + "\n")
            break


if __name__ == "__main__":
    main()
