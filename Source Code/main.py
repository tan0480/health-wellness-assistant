import tkinter as tk
from tkinter import messagebox

# Import feature modules
from dailyWellnessLog import daily_wellness_log_gui
from bmiCalorie import bmi_calorie_calculator_gui
from medicationReminder import medication_reminder_gui
from stepCounter import step_counter_gui


def exit_program_gui():
    """Handle program exit with confirmation dialog."""
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        window.destroy()
    else:
        window.lift()           # Bring window back to front
        window.focus_force()    # Force focus on window


def on_enter(event):
    """Change button background on hover (enter)."""
    event.widget.config(bg=BTN_HOVER)


def on_leave(event):
    """Restore button background when mouse leaves."""
    event.widget.config(bg=BTN_COLOR)


# Main application window
window = tk.Tk()
window.title("Health & Wellness Assistant")
window.state('zoomed')  # Full screen (maximized)

# Color constants
BTN_COLOR = "#4A90E2"       # Default button color
BTN_HOVER = "#357ABD"       # Hover button color
TEXT_COLOR = "#333333"      # General text color
background = "#DBE9FF"      # Window background color

# Confirm exit when user clicks window close button (X)
def confirm_exit():
    """Confirm exit when closing window via window manager."""
    if messagebox.askyesno("Exit", "Are you sure you want to close this window?"):
        window.destroy()
    else:
        window.lift()
        window.focus_force()

window.protocol("WM_DELETE_WINDOW", confirm_exit)

window.configure(bg=background)
window.attributes("-alpha", 0.0)  # Start invisible for fade-in effect

# Smooth fade-in animation
def fade_in(alpha=0.0):
    """Gradually increase window opacity for fade-in effect."""
    if alpha < 1.0:
        alpha += 0.5
        window.attributes("-alpha", alpha)
        window.after(5, fade_in, alpha)

# Main title label
heading = tk.Label(
    window,
    text="Health & Wellness Assistant",
    font=("Times New Roman", 48, "bold"),
    bg=background,
    fg=BTN_COLOR
)
heading.pack(pady=100)

# List of main menu options and their corresponding functions
button_info = [
    ("Daily Wellness Log", daily_wellness_log_gui),
    ("BMI & Calorie Calculator", bmi_calorie_calculator_gui),
    ("Medication Reminder", medication_reminder_gui),
    ("Step Counter Log", step_counter_gui),
    ("Exit", exit_program_gui)
]

# Create frame for buttons
button_frame = tk.Frame(window, bg=background)
button_frame.pack(pady=40)

# Create and style buttons
for text, cmd in button_info:
    btn = tk.Button(
        button_frame,
        text=text,
        font=("Times New Roman", 24),
        width=35,
        command=cmd,
        bg=BTN_COLOR,
        fg="white",
        activebackground=BTN_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2"
    )
    btn.pack(pady=0, ipadx=20, ipady=20)
    btn.bind("<Enter>", on_enter)    # Hover effect
    btn.bind("<Leave>", on_leave)    # Hover end effect

# Footer label
footer = tk.Label(
    window,
    text="© 2025 Health & Wellness Assistant",
    font=("Times New Roman", 14),
    bg=background,
    fg=TEXT_COLOR
)
footer.pack(side="bottom", pady=20)

# Start fade-in animation
fade_in()

# Run the application
window.mainloop()