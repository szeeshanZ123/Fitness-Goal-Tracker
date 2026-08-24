# 🏋️ Fitness Goal Tracker

A complete, feature-rich, command-line fitness tracking and health analytics application written in Python. Track your daily steps, hydration, workouts, calories burned, meals, and body metrics with persistent data storage and gamified achievements.

![Version](https://img.shields.io/badge/version-1.0.0--100%25%20Complete-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Scientific & Health Formulas Used](#-scientific--health-formulas-used)
- [Project Structure](#-project-structure)
- [Installation & Getting Started](#-installation--getting-started)
- [Usage Guide](#-usage-guide)
- [Data Storage & Reports](#-data-storage--reports)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Fitness Goal Tracker** is designed for individuals who want a clean, fast, and distraction-free CLI tool to monitor their daily health habits. Unlike cloud-locked apps, this tool keeps all your personal health data safely on your machine in human-readable JSON and text reports.

---

## ✨ Key Features

### 👤 1. User Profile & Advanced Health Metrics
- **Profile Management:** Store Name, Age, Gender, Height, Weight, and Activity Level.
- **BMI (Body Mass Index):** Automatic calculation with health categories and personalized advice.
- **BMR (Basal Metabolic Rate):** Mifflin-St Jeor equation to estimate base metabolic rate.
- **TDEE (Total Daily Energy Expenditure):** Calorie maintenance estimate based on activity multiplier.
- **Target Heart Rate Zones:** Computes Warm-up (50-60%), Fat Burn (60-70%), Cardio (70-85%), and Peak (85-100%) zones.
- **Ideal Body Weight:** Uses the Devine Formula to calculate healthy target weights and realistic timelines.

### 🎯 2. Daily Goals Management
- Set and adjust daily targets for:
  - **Steps** (e.g., 10,000 steps)
  - **Water Intake** (e.g., 3.0 Litres)
  - **Active Workout Time** (e.g., 45 Minutes)
  - **Calorie Burn Target** (e.g., 450 kcal)
  - **Calorie Intake Target** (e.g., 2,200 kcal)
- One-click reset to standard healthy recommendations.

### 🏃 3. Activity & Nutrition Logging
- **Steps Tracking:** Quick-add steps or update total daily count.
- **Water Hydration Logger:** One-click presets (+250ml glass, +500ml bottle, +1.0L bottle) or custom amount.
- **Workout Sessions & MET Calorie Estimator:** Select activity types (Walking, Running, Cycling, Strength/Gym, HIIT, Yoga, Swimming, etc.) with automatic calorie burn calculation based on MET values, duration, and body weight.
- **Meal & Calorie Intake:** Track daily calories consumed and calculate **Net Calorie Balance** (`Consumed - Burned`).
- **Quick Update All:** Rapid single-screen update for all metrics.

### 📊 4. Live Progress Dashboard
- Clean ASCII progress bars for each individual fitness goal.
- Overall daily completion percentage score with motivational achievement feedback.

### 📈 5. Multi-Day History & Weekly Analytics
- Date-stamped logs (`YYYY-MM-DD`).
- **Past 7 Days Summary Table:** Formatted table showing daily steps, water, workouts, calories burned, and completion score.
- **Weekly Averages:** Automatic calculation of daily averages across active days.
- **Date Browser & All-Time Stats:** Look up past logs or view personal records (e.g., best step day, longest workout).

### 🏆 6. Streaks & Gamification Badge System
- **Streak Tracker:** Tracks consecutive active days.
- **Milestone Achievement Badges:**
  - `First Step` — Logged first fitness activity.
  - `Hydration Hero` — Hit daily water goal.
  - `10K Walker Club` — Walked 10,000+ steps in a single day.
  - `Calorie Crusher` — Burned 500+ active calories in one day.
  - `Consistency Master` — Maintained a 3-day active streak.
  - `7-Day Warrior` — Maintained a 7-day active streak.
  - `Century Performer` — Accumulated 100,000+ all-time steps.
  - `Fitness Enthusiast` — Completed 300+ total workout minutes.

### 💾 7. Persistence & Summary Report Export
- **Auto-Save & Load:** JSON file storage (`fitness_data.json`) automatically saves changes and loads upon startup.
- **Export Summary Report:** Generates a formatted text summary report (`fitness_report.txt`) for easy sharing or archiving.

---

## 🧮 Scientific & Health Formulas Used

| Metric | Formula / Algorithm |
| :--- | :--- |
| **BMI** | BMI = Weight(kg) / (Height(m))^2 |
| **BMR (Male)** | BMR = 10 x weight(kg) + 6.25 x height(cm) - 5 x age + 5 |
| **BMR (Female)** | BMR = 10 x weight(kg) + 6.25 x height(cm) - 5 x age - 161 |
| **TDEE** | TDEE = BMR x Activity Multiplier (1.2 to 1.9) |
| **Calorie Burn** | Calories = MET x Weight (kg) x Duration (hours) |
| **Max Heart Rate** | Max HR = 220 - Age |
| **Ideal Body Weight** | Devine Formula: Men = 50.0 + 2.3 x (inches - 60), Women = 45.5 + 2.3 x (inches - 60) |

---

## 📁 Project Structure

```
Fitness-Goal-Tracker/
│
├── app.py                # Main application code (100% complete)
├── fitness_data.json     # Persistent data storage (Auto-generated)
├── fitness_report.txt    # Exported fitness summary report (Auto-generated)
└── README.md             # Project documentation
```

---

## 🚀 Installation & Getting Started

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the Application

1. Clone or download the repository:
   ```bash
   git clone https://github.com/szeeshanZ123/Fitness-Goal-Tracker.git
   cd Fitness-Goal-Tracker
   ```

2. Run the application:
   ```bash
   python app.py
   ```

---

## 📖 Usage Guide

When you start the application, you will be greeted by the Main Menu:

```
===================================
             MAIN MENU
===================================
 1. User Profile & Health Metrics
 2. Daily Goals Management
 3. Log Activity & Nutrition
 4. View Today's Progress Dashboard
 5. History & Weekly Analytics
 6. Streaks & Achievement Badges
 7. Export Fitness Summary Report
 8. Data & Storage Settings
 9. Exit
-----------------------------------
```

### Quick Workflow:
1. **Option 1:** Create your User Profile (Name, Age, Height, Weight, Activity Level).
2. **Option 2:** Set your target daily goals (Steps, Water, Workout, Calories).
3. **Option 3:** Log your activities throughout the day (Steps, Water, Workouts, Meals).
4. **Option 4:** View your live ASCII progress dashboard and overall daily score.
5. **Option 5 & 6:** Track weekly trends, check your active streaks, and unlock badges.
6. **Option 7:** Export your complete fitness history report to `fitness_report.txt`.

---

## 💾 Data Storage & Reports

- **`fitness_data.json`**: Automatically saved in the application directory on every update. Contains profile settings, goals, multi-day logs, streaks, and unlocked badges.
- **`fitness_report.txt`**: A clean, printable text report summarizing your stats, targets, badges, and recent logs.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check out the issues page or fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
