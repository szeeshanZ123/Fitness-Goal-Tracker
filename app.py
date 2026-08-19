# ============================================================
# FITNESS GOAL TRACKER
# PHASE 2 - 50% COMPLETE
# ============================================================

# ------------------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------------------

profile = {}
goals = {}
progress = {}


# ------------------------------------------------------------
# PAUSE FUNCTION
# ------------------------------------------------------------

def pause():
    input("\nPress Enter to continue...")


# ------------------------------------------------------------
# WELCOME SCREEN
# ------------------------------------------------------------

def welcome():

    print("=" * 50)
    print("             FITNESS GOAL TRACKER")
    print("              PHASE 2 - 50%")
    print("=" * 50)


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

def menu():

    print("\nMain Menu")
    print("-" * 30)

    print("1. Create User Profile")
    print("2. View Profile")
    print("3. Edit Profile")
    print("4. Calculate BMI")
    print("5. Set Daily Goals")
    print("6. Edit Daily Goals")
    print("7. Update Today's Progress")
    print("8. View Today's Progress")
    print("9. Exit")


# ------------------------------------------------------------
# CREATE USER PROFILE
# ------------------------------------------------------------

def create_profile():

    print("\nCreate User Profile")
    print("-" * 30)

    profile["Name"] = input("Enter Name : ")

    # AGE
    while True:

        try:

            age = int(input("Enter Age : "))

            if age > 0:

                profile["Age"] = age
                break

            else:

                print("Age must be greater than 0.")

        except ValueError:

            print("Enter a valid age.")

    # GENDER
    profile["Gender"] = input("Enter Gender : ")

    # HEIGHT
    while True:

        try:

            height = float(
                input("Enter Height (cm) : ")
            )

            if height > 0:

                profile["Height"] = height
                break

            else:

                print("Invalid height.")

        except ValueError:

            print("Enter a valid height.")

    # WEIGHT
    while True:

        try:

            weight = float(
                input("Enter Weight (kg) : ")
            )

            if weight > 0:

                profile["Weight"] = weight
                break

            else:

                print("Invalid weight.")

        except ValueError:

            print("Enter a valid weight.")

    print("\nProfile Created Successfully.")

    pause()


# ------------------------------------------------------------
# VIEW PROFILE
# ------------------------------------------------------------

def view_profile():

    if len(profile) == 0:

        print("\nNo profile found.")

        pause()

        return

    print("\nUser Profile")
    print("-" * 30)

    print("Name    :", profile["Name"])
    print("Age     :", profile["Age"])
    print("Gender  :", profile["Gender"])
    print("Height  :", profile["Height"], "cm")
    print("Weight  :", profile["Weight"], "kg")

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
    print("-" * 30)

    print("Press Enter to keep the existing value.")

    # NAME
    name = input(
        "Name [" + profile["Name"] + "] : "
    )

    if name != "":

        profile["Name"] = name

    # AGE
    while True:

        age_input = input(
            "Age [" + str(profile["Age"]) + "] : "
        )

        if age_input == "":

            break

        try:

            age = int(age_input)

            if age > 0:

                profile["Age"] = age

                break

            else:

                print("Age must be greater than 0.")

        except ValueError:

            print("Enter a valid age.")

    # GENDER
    gender = input(
        "Gender [" + profile["Gender"] + "] : "
    )

    if gender != "":

        profile["Gender"] = gender

    # HEIGHT
    while True:

        height_input = input(
            "Height [" +
            str(profile["Height"]) +
            " cm] : "
        )

        if height_input == "":

            break

        try:

            height = float(height_input)

            if height > 0:

                profile["Height"] = height

                break

            else:

                print("Invalid height.")

        except ValueError:

            print("Enter a valid height.")

    # WEIGHT
    while True:

        weight_input = input(
            "Weight [" +
            str(profile["Weight"]) +
            " kg] : "
        )

        if weight_input == "":

            break

        try:

            weight = float(weight_input)

            if weight > 0:

                profile["Weight"] = weight

                break

            else:

                print("Invalid weight.")

        except ValueError:

            print("Enter a valid weight.")

    print("\nProfile Updated Successfully.")

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

    print("\nBMI CALCULATOR")
    print("-" * 30)

    print("Name   :", profile["Name"])
    print("Height :", profile["Height"], "cm")
    print("Weight :", profile["Weight"], "kg")

    print("\nBMI :", round(bmi, 2))

    # BMI CATEGORY
    if bmi < 18.5:

        category = "Underweight"

    elif bmi < 25:

        category = "Normal Weight"

    elif bmi < 30:

        category = "Overweight"

    else:

        category = "Obese"

    print("Category :", category)

    pause()


# ------------------------------------------------------------
# SET DAILY GOALS
# ------------------------------------------------------------

def set_goals():

    print("\nSet Daily Goals")
    print("-" * 30)

    # STEP GOAL
    while True:

        try:

            steps = int(
                input("Daily Step Goal : ")
            )

            if steps > 0:

                goals["Steps"] = steps

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    # WATER GOAL
    while True:

        try:

            water = float(
                input(
                    "Daily Water Goal (Litres) : "
                )
            )

            if water > 0:

                goals["Water"] = water

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    # WORKOUT GOAL
    while True:

        try:

            workout = int(
                input(
                    "Daily Workout Goal (Minutes) : "
                )
            )

            if workout > 0:

                goals["Workout"] = workout

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    print("\nGoals Saved Successfully.")

    pause()


# ------------------------------------------------------------
# EDIT DAILY GOALS
# ------------------------------------------------------------

def edit_goals():

    if len(goals) == 0:

        print("\nPlease set your goals first.")

        pause()

        return

    print("\nEdit Daily Goals")
    print("-" * 30)

    print("Press Enter to keep the existing value.")

    # STEPS
    while True:

        steps_input = input(
            "Steps [" +
            str(goals["Steps"]) +
            "] : "
        )

        if steps_input == "":

            break

        try:

            steps = int(steps_input)

            if steps > 0:

                goals["Steps"] = steps

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    # WATER
    while True:

        water_input = input(
            "Water [" +
            str(goals["Water"]) +
            " L] : "
        )

        if water_input == "":

            break

        try:

            water = float(water_input)

            if water > 0:

                goals["Water"] = water

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    # WORKOUT
    while True:

        workout_input = input(
            "Workout [" +
            str(goals["Workout"]) +
            " min] : "
        )

        if workout_input == "":

            break

        try:

            workout = int(workout_input)

            if workout > 0:

                goals["Workout"] = workout

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    print("\nGoals Updated Successfully.")

    pause()


# ------------------------------------------------------------
# UPDATE TODAY'S PROGRESS
# ------------------------------------------------------------

def update_progress():

    if len(goals) == 0:

        print(
            "\nPlease set your daily goals first."
        )

        pause()

        return

    print("\nUpdate Today's Progress")
    print("-" * 30)

    # STEPS
    while True:

        try:

            steps = int(
                input("Today's Steps : ")
            )

            if steps >= 0:

                progress["Steps"] = steps

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    # WATER
    while True:

        try:

            water = float(
                input(
                    "Water Consumed (Litres) : "
                )
            )

            if water >= 0:

                progress["Water"] = water

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    # WORKOUT
    while True:

        try:

            workout = int(
                input(
                    "Workout Done (Minutes) : "
                )
            )

            if workout >= 0:

                progress["Workout"] = workout

                break

            else:

                print("Invalid value.")

        except ValueError:

            print("Enter a valid number.")

    print(
        "\nToday's Progress Updated Successfully."
    )

    pause()


# ------------------------------------------------------------
# PROGRESS BAR
# ------------------------------------------------------------

def progress_bar(percent):

    total_blocks = 20

    filled_blocks = int(
        percent / 100 * total_blocks
    )

    empty_blocks = (
        total_blocks -
        filled_blocks
    )

    bar = (
        "[" +
        "#" * filled_blocks +
        "-" * empty_blocks +
        "]"
    )

    return bar


# ------------------------------------------------------------
# VIEW TODAY'S PROGRESS
# ------------------------------------------------------------

def view_progress():

    if len(goals) == 0:

        print(
            "\nPlease set your goals first."
        )

        pause()

        return

    if len(progress) == 0:

        print(
            "\nNo progress available."
        )

        pause()

        return

    # STEP PERCENTAGE
    step_percent = (
        progress["Steps"] /
        goals["Steps"]
    ) * 100

    # WATER PERCENTAGE
    water_percent = (
        progress["Water"] /
        goals["Water"]
    ) * 100

    # WORKOUT PERCENTAGE
    workout_percent = (
        progress["Workout"] /
        goals["Workout"]
    ) * 100

    # LIMIT TO 100%
    step_percent = min(
        step_percent,
        100
    )

    water_percent = min(
        water_percent,
        100
    )

    workout_percent = min(
        workout_percent,
        100
    )

    # OVERALL PROGRESS
    overall = (
        step_percent +
        water_percent +
        workout_percent
    ) / 3

    print("\nToday's Progress")
    print("-" * 45)

    # STEPS
    print("\nSteps")

    print(
        progress["Steps"],
        "/",
        goals["Steps"]
    )

    print(
        progress_bar(step_percent)
    )

    print(
        "Completion :",
        round(step_percent, 2),
        "%"
    )

    # WATER
    print("\nWater")

    print(
        progress["Water"],
        "/",
        goals["Water"],
        "L"
    )

    print(
        progress_bar(water_percent)
    )

    print(
        "Completion :",
        round(water_percent, 2),
        "%"
    )

    # WORKOUT
    print("\nWorkout")

    print(
        progress["Workout"],
        "/",
        goals["Workout"],
        "Minutes"
    )

    print(
        progress_bar(workout_percent)
    )

    print(
        "Completion :",
        round(workout_percent, 2),
        "%"
    )

    print("\n" + "-" * 45)

    print(
        "Overall Progress :",
        round(overall, 2),
        "%"
    )

    # --------------------------------------------------------
    # ACHIEVEMENT SYSTEM
    # --------------------------------------------------------

    if overall == 100:

        print(
            "\nAchievement Unlocked!"
        )

        print(
            "Excellent! All daily goals achieved."
        )

    elif overall >= 70:

        print(
            "\nGreat Job!"
        )

        print(
            "You are close to completing "
            "all your goals."
        )

    elif overall >= 40:

        print(
            "\nGood Progress!"
        )

        print(
            "Keep working towards your goals."
        )

    else:

        print(
            "\nKeep Going!"
        )

        print(
            "Every small step counts."
        )

    pause()


# ------------------------------------------------------------
# PROGRAM START
# ------------------------------------------------------------

welcome()


# ------------------------------------------------------------
# MAIN PROGRAM LOOP
# ------------------------------------------------------------

while True:

    menu()

    choice = input(
        "\nEnter Your Choice : "
    )

    # CREATE PROFILE
    if choice == "1":

        create_profile()

    # VIEW PROFILE
    elif choice == "2":

        view_profile()

    # EDIT PROFILE
    elif choice == "3":

        edit_profile()

    # BMI
    elif choice == "4":

        calculate_bmi()

    # SET GOALS
    elif choice == "5":

        set_goals()

    # EDIT GOALS
    elif choice == "6":

        edit_goals()

    # UPDATE PROGRESS
    elif choice == "7":

        update_progress()

    # VIEW PROGRESS
    elif choice == "8":

        view_progress()

    # EXIT
    elif choice == "9":

        print(
            "\nThank You For Using "
            "Fitness Goal Tracker."
        )

        print("Goodbye!")

        break

    # INVALID OPTION
    else:

        print(
            "\nInvalid Choice."
        )

        pause()
