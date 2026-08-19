# 🏋️ Fitness Goal Tracker

A simple **Python-based console application** designed to help users create a fitness profile, calculate BMI, set daily fitness goals, track daily progress, and monitor goal completion.

> **Current Status:** Phase 2 — 50% Complete

---

## 📌 Overview

The **Fitness Goal Tracker** is a beginner-friendly fitness management application developed using Python.

The application allows users to:

* Create and manage a personal fitness profile
* Calculate Body Mass Index (BMI)
* Set daily fitness goals
* Edit existing goals
* Record daily fitness progress
* View goal completion percentages
* Display visual progress bars
* Calculate overall daily progress
* Unlock achievement messages based on performance

The current version is built as a **menu-driven console application**.

---

## ✨ Features

### 👤 User Profile

Users can create a profile containing:

* Name
* Age
* Gender
* Height
* Weight

Users can also view and edit their existing profile.

---

### ⚖️ BMI Calculator

The application calculates BMI using the user's height and weight.

**Formula:**

```text
BMI = Weight (kg) / Height² (m)
```

The application categorizes BMI into:

* Underweight
* Normal Weight
* Overweight
* Obese

---

### 🎯 Daily Goals

Users can define three daily fitness targets:

* 👣 Daily Steps
* 💧 Daily Water Intake
* 🏋️ Workout Duration

Existing goals can also be edited.

---

### 📊 Daily Progress Tracking

Users can enter their progress for:

* Steps completed
* Water consumed
* Workout minutes completed

The application compares the progress against the user's daily goals.

---

### 📈 Progress Bars

The application displays text-based progress bars to make goal completion easier to understand.

Example:

```text
[##############------]

Completion : 70.0%
```

---

### 🏆 Achievement System

The application provides motivational messages based on overall progress.

| Progress  | Achievement             |
| --------- | ----------------------- |
| 100%      | 🏆 Achievement Unlocked |
| 70%+      | ⭐ Great Job             |
| 40%+      | 👍 Good Progress        |
| Below 40% | 💪 Keep Going           |

---

## 🛠️ Technologies Used

* **Python**
* Dictionaries
* Functions
* Conditional Statements
* Loops
* Exception Handling
* User Input Validation
* Basic Mathematical Calculations
* Console-Based UI

---

## 📂 Project Structure

```text
Fitness-Goal-Tracker/
│
├── fitness_goal_tracker.py
│
└── README.md
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fitness-goal-tracker.git
```

### 2. Open the project

```bash
cd fitness-goal-tracker
```

### 3. Run the Python file

```bash
python fitness_goal_tracker.py
```

---

## 🖥️ Application Menu

```text
Main Menu
------------------------------

1. Create User Profile
2. View Profile
3. Edit Profile
4. Calculate BMI
5. Set Daily Goals
6. Edit Daily Goals
7. Update Today's Progress
8. View Today's Progress
9. Exit
```

---

## 🔄 Application Workflow

```text
Start
  │
  ▼
Create User Profile
  │
  ▼
Calculate BMI
  │
  ▼
Set Daily Goals
  │
  ▼
Update Daily Progress
  │
  ▼
Calculate Completion %
  │
  ▼
View Progress Bars
  │
  ▼
Achievement Message
  │
  ▼
Exit
```

---

## 🔐 Input Validation

The application includes basic validation to prevent invalid input.

Examples include:

* Age must be greater than zero
* Height must be greater than zero
* Weight must be greater than zero
* Daily steps must be a positive number
* Water goal must be greater than zero
* Workout goal must be greater than zero
* Daily progress values cannot be negative
* Invalid numerical inputs are handled using exception handling

---

## 📊 Progress Calculation

Individual goal completion is calculated using:

```text
Progress % = (Actual Progress / Daily Goal) × 100
```

The completion percentage is limited to a maximum of **100%**.

Overall progress is calculated using the average of:

```text
Steps Progress
+
Water Progress
+
Workout Progress
-------------------------
3
```

---

## 🏆 Current Development Status

### Phase 1

* [x] Basic Python structure
* [x] Functions
* [x] Menu-driven program
* [x] User input
* [x] Dictionaries
* [x] Basic validation

### Phase 2 — 50% Complete

* [x] User profile management
* [x] BMI calculator
* [x] Daily goals
* [x] Goal editing
* [x] Daily progress tracking
* [x] Progress percentage
* [x] Progress bars
* [x] Achievement system

### Future Improvements

* [ ] Store data permanently using files
* [ ] Add date-wise progress history
* [ ] Add weekly and monthly reports
* [ ] Add calorie tracking
* [ ] Add sleep tracking
* [ ] Add multiple user accounts
* [ ] Add graphical dashboard
* [ ] Add database integration
* [ ] Convert into a web application
* [ ] Add data visualization

---

## 🎯 Project Objective

The main objective of this project is to practice Python programming concepts by developing a practical fitness tracking application.

The project demonstrates how basic programming concepts such as **functions, dictionaries, loops, conditional statements, validation, and calculations** can be combined to create a functional application.

---

## 📚 Learning Outcomes

Through this project, the following concepts are practiced:

* Python fundamentals
* Function-based programming
* Data storage using dictionaries
* Input validation
* Exception handling
* Mathematical calculations
* Menu-driven application development
* Basic progress analysis
* User-friendly console interaction

---

## 🔮 Future Vision

The long-term goal is to transform this console-based application into a more advanced **Fitness Management System** with persistent storage, analytics, visual dashboards, and personalized fitness insights.

---

## 👨‍💻 Author

**Zeeshan Shaikh**

Student | Python Learner | Data Analytics & Data Science Enthusiast

---

## ⭐ Project Status

**Version:** 2.0
**Completion:** 50%
**Type:** Python Console Application
**Status:** 🚧 In Development

---

⭐ If you find this project useful, consider giving the repository a star!
