---

# 🩺 Health & Wellness Assistant

A Python-based desktop application built using **Tkinter**, designed to help users manage their daily health activities in one place.
The system integrates multiple wellness features including BMI calculation, medication reminders, daily wellness logging, and step tracking.

---

## 📂 Project Structure

```
health-wellness-assistant/
│
├── Source Code/
│   ├── main.py
│   ├── bmiCalorie.py
│   ├── dailyWellnessLog.py
│   ├── medicationReminder.py
│   └── stepCounter.py
├── .gitignore
└── README.md
```

---

## 🧠 Features Overview

### 1️⃣ Main Menu (`main.py`)

* Acts as the **central launcher** of the application
* Provides navigation buttons to access all modules:

  * Daily Wellness Log
  * BMI & Calorie Calculator
  * Medication Reminder
  * Step Counter Log
* Ensures a consistent and user-friendly interface

---

### 2️⃣ BMI & Calorie Calculator (`bmiCalorie.py`)

* Calculates **Body Mass Index (BMI)** based on:

  * Height
  * Weight
* Displays BMI category (Underweight, Normal, Overweight, Obese)
* Estimates daily calorie needs
* Provides instant health feedback

---

### 3️⃣ Daily Wellness Log (`dailyWellnessLog.py`)

* Allows users to record daily wellness data:

  * Sleep hours
  * Water intake
  * Mood selection
  * Meals consumed
  * Personal reflections
* Features include:

  * Input validation
  * Placeholder guidance
  * View past records
  * Delete selected log entries
* Data stored in `wellness.txt`

---

### 4️⃣ Medication Reminder (`medicationReminder.py`)

* Enables users to:

  * Add medication schedules (name, time, dosage)
  * Check reminders based on current time
  * View medication history
  * Delete selected medication records
* Includes UI enhancements such as:

  * Hover effects
  * Fade-in animation
* Data stored in `medication.txt`

---

### 5️⃣ Step Counter Log (`stepCounter.py`)

* Allows users to:

  * Set daily step goals
  * Manually log daily steps
  * Track progress toward goals
  * View step history
* Encourages healthy daily movement
* Data stored in `steps.txt`

---

## 💻 System Requirements

* Python **3.9 or later**
* A Python installation with **Tkinter/Tcl/Tk** available
* Windows is the intended desktop platform; the code uses maximized-window behavior such as `state("zoomed")`
* No external libraries required (uses built-in modules only)

---

## ▶️ How to Run the Program

From the repository root, open PowerShell and run:

```powershell
cd "Source Code"
python main.py
```

Keep the five Python modules together. Start the program from `Source Code` because its data paths are relative to the current working directory.

---

## 🗃 Data Storage

The application uses **text files** for simple data persistence:

| File Name        | Purpose              |
| ---------------- | -------------------- |
| `wellness.txt`   | Daily wellness logs  |
| `medication.txt` | Medication schedules |
| `steps.txt`      | Step counter records |

Existing health records are deliberately not uploaded. The application creates local data files when records are saved; the files are ignored by Git. Never commit personal wellness or medication information. There is no cloud service or database setup required.

---

## 🎨 User Interface Highlights

* Fullscreen layout for better accessibility
* Consistent color theme
* Hover effects on buttons
* Fade-in transitions for improved user experience
* Input validation with clear error messages

---

## 📌 Notes

* This project is designed for **educational purposes**
* Data is stored locally and not encrypted
* Manual input is required (no device syncing)
* Medication reminders are checked through the application interface, not a background notification service
* Calculations and reminders are educational features, not a medical device or medical advice

## Coding Contributions

| Contributor | Module | Contribution |
| --- | --- | --- |
| [Lam Yi Hen](https://github.com/lamyihen77-beep) | `Source Code/bmiCalorie.py` | BMI and calorie estimates, input validation, and calculator interface |
| [Lim Jun Yi](https://github.com/ljunyi0212) | `Source Code/dailyWellnessLog.py` | Daily wellness logging, record storage, history, and deletion |
| [Cheah Yong Shun](https://github.com/ys012007) | `Source Code/medicationReminder.py` | Medication schedules, reminder checks, taken-status tracking, and history management |
| [Tan Yi Heng](https://github.com/tan0480) | `Source Code/stepCounter.py`, `Source Code/main.py` | Manual step logging, goal progress, history management, main menu, and module integration |

This mapping reflects the team contributions confirmed for this assignment. The repository imports existing work; the import dates are not its original development dates. Tan Yi Heng performs the commits and push, while each feature commit credits its module's author.

## Import Verification

The five original Python modules passed syntax compilation with Python 3.14, and the four functions imported by `main.py` were checked against their module definitions. Tkinter was available in that environment. These are static checks, not a completed GUI or end-to-end test; no existing health records were used or modified.

The independent `test.py` dropdown demonstration, Python caches, assignment PDFs, assessment spreadsheet, and local health records are excluded from this repository.
