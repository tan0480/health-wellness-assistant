import tkinter as tk
from tkinter import messagebox

# Color constants used across the BMI & Calorie Calculator window
BTN_COLOR = "#4A90E2"          # Default button background
BTN_HOVER = "#357ABD"          # Button hover background
TEXT_COLOR = "#333333"         # General text color
BACKGROUND = "#DBE9FF"         # Window background

def bmi_calorie_calculator_gui():
    """Create and manage the BMI & Calorie Calculator window."""
    bmi_window = tk.Toplevel()
    bmi_window.title("BMI & Calorie Calculator")
    bmi_window.state("zoomed")              # Open in maximized/full-screen mode
    bmi_window.configure(bg=BACKGROUND)

    # Confirm exit when user clicks the window's close button (X)
    def confirm_exit():
        """Ask for confirmation before closing the window."""
        if messagebox.askyesno("Exit", "Are you sure you want to close this window?"):
            bmi_window.destroy()
        else:
            bmi_window.lift()           # Bring window back to front
            bmi_window.focus_force()    # Force focus on window

    bmi_window.protocol("WM_DELETE_WINDOW", confirm_exit)

    # Hover effect for buttons
    def on_enter(e):
        """Change button background color on mouse hover."""
        e.widget.config(bg=BTN_HOVER)

    def on_leave(e):
        """Restore original button background color when mouse leaves."""
        e.widget.config(bg=BTN_COLOR)

    # Calculate BMI, BMR, and daily calorie needs based on user input
    def calculate_bmi_calories():
        """Perform BMI, BMR, and calorie calculations and display results."""
        weight_str = weight_entry.get().strip()
        height_str = height_entry.get().strip()
        age_str = age_entry.get().strip()

        # Basic input validation
        if not weight_str:
            messagebox.showerror("Input Error", "Weight cannot be empty")
            weight_entry.focus_set()
            return

        if not height_str:
            messagebox.showerror("Input Error", "Height cannot be empty")
            height_entry.focus_set()
            return

        if not age_str:
            messagebox.showerror("Input Error", "Age cannot be empty")
            age_entry.focus_set()
            return

        # Check for valid number formats
        if not weight_str.replace(".", "", 1).isdigit():
            messagebox.showerror("Input Error", "Weight must be a number (e.g., 70 or 70.5)")
            weight_entry.focus_set()
            return

        if not height_str.replace(".", "", 1).isdigit():
            messagebox.showerror("Input Error", "Height must be a number (e.g., 1.75)")
            height_entry.focus_set()
            return

        if not age_str.isdigit():
            messagebox.showerror("Input Error", "Age must be a whole number")
            age_entry.focus_set()
            return

        try:
            weight = float(weight_str)
            height = float(height_str)
            age = int(age_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid number format.")
            return

        # Reasonable input range checks
        if weight > 1000:
            messagebox.showerror("Input Error", "Weight cannot exceed 1000 kg")
            weight_entry.focus_set()
            return

        if height > 3.0:
            messagebox.showerror("Input Error", "Height must be in meters (e.g., 1.75)")
            height_entry.focus_set()
            return

        if age > 200:
            messagebox.showerror("Input Error", "Age must be less than 200")
            age_entry.focus_set()
            return

        gender = gender_var.get()
        activity_level = activity_level_var.get()

        # Calculate BMI
        bmi = weight / (height ** 2)
        bmi_result.config(text=f"BMI: {bmi:.2f}")

        # Display BMI category with color coding
        if bmi < 18.5:
            bmi_category.config(text="Category: Underweight", fg="red")
        elif bmi < 25:
            bmi_category.config(text="Category: Normal", fg="green")
        elif bmi < 30:
            bmi_category.config(text="Category: Overweight", fg="orange")
        else:
            bmi_category.config(text="Category: Obese", fg="red")

        # Calculate BMR using Harris-Benedict equation
        height_cm = height * 100
        if gender == "M":
            bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161

        bmr_result.config(text=f"BMR: {int(bmr)} kcal/day")

        # Apply activity multiplier to get daily calorie needs
        multipliers = {"1": 1.2, "2": 1.55, "3": 1.8}
        multiplier = multipliers.get(activity_level, 1.2)
        calories = bmr * multiplier

        calories_result.config(text=f"Estimated Daily Calories: {int(calories)} kcal")

        # Clear input fields after calculation
        weight_entry.delete(0, tk.END)
        height_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)

    # Title label
    tk.Label(
        bmi_window,
        text="BMI & Calorie Calculator",
        font=("Times New Roman", 40, "bold"),
        bg=BACKGROUND,
        fg=BTN_COLOR
    ).pack(pady=20)

    # Form frame for inputs
    form = tk.Frame(bmi_window, bg=BACKGROUND)
    form.pack(pady=10)

    # Helper function to create labeled input rows
    def add_row(text, row):
        """Create a label and entry field in the form."""
        tk.Label(
            form, text=text,
            font=("Times New Roman", 20),
            bg=BACKGROUND, fg=TEXT_COLOR
        ).grid(row=row, column=0, sticky="e", padx=15, pady=12)

        entry = tk.Entry(form, font=("Times New Roman", 20), width=15)
        entry.grid(row=row, column=1, pady=12)
        return entry

    # Input fields
    weight_entry = add_row("Weight (kg):", 0)
    height_entry = add_row("Height (m):", 1)
    age_entry = add_row("Age:", 2)

    # Gender selection
    tk.Label(form, text="Gender:", font=("Times New Roman", 20),
             bg=BACKGROUND, fg=TEXT_COLOR).grid(row=3, column=0, sticky="e", padx=20, pady=15)

    gender_var = tk.StringVar(value="M")
    gender_frame = tk.Frame(form, bg=BACKGROUND)
    gender_frame.grid(row=3, column=1, pady=15)

    tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="M",
                   font=("Times New Roman", 18), bg=BACKGROUND, selectcolor=BACKGROUND,
                   activebackground=BACKGROUND).pack(side="left", padx=10)
    tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="F",
                   font=("Times New Roman", 18), bg=BACKGROUND, selectcolor=BACKGROUND,
                   activebackground=BACKGROUND).pack(side="left", padx=10)

    # Activity level selection
    activity_level_var = tk.StringVar(value="1")
    tk.Label(form, text="Activity Level:", font=("Times New Roman", 20),
             bg=BACKGROUND, fg=TEXT_COLOR).grid(row=5, column=0, sticky="e", padx=20, pady=15)

    tk.Radiobutton(form, text="Low", font=("Times New Roman", 18), variable=activity_level_var,
                   value="1", bg=BACKGROUND, activebackground=BACKGROUND).grid(row=5, column=1, sticky="w")
    tk.Radiobutton(form, text="Moderate", font=("Times New Roman", 18), variable=activity_level_var,
                   value="2", bg=BACKGROUND, activebackground=BACKGROUND).grid(row=6, column=1, sticky="w")
    tk.Radiobutton(form, text="High", font=("Times New Roman", 18), variable=activity_level_var,
                   value="3", bg=BACKGROUND, activebackground=BACKGROUND).grid(row=7, column=1, sticky="w")

    # Calculate button
    calc_btn = tk.Button(
        bmi_window,
        text="Calculate",
        font=("Times New Roman", 22),
        bg=BTN_COLOR,
        fg="white",
        width=18,
        command=calculate_bmi_calories,
        activebackground=BTN_HOVER,
        activeforeground="white",
        relief="flat"
    )
    calc_btn.pack(pady=5)
    calc_btn.bind("<Enter>", on_enter)
    calc_btn.bind("<Leave>", on_leave)

    # Result labels
    bmi_result = tk.Label(bmi_window, font=("Times New Roman", 20), bg=BACKGROUND)
    bmi_result.pack()

    bmi_category = tk.Label(bmi_window, font=("Times New Roman", 20), bg=BACKGROUND)
    bmi_category.pack()

    bmr_result = tk.Label(bmi_window, font=("Times New Roman", 20), bg=BACKGROUND)
    bmr_result.pack()

    calories_result = tk.Label(bmi_window, font=("Times New Roman", 20), bg=BACKGROUND)
    calories_result.pack(pady=10)

    # Close button
    exit_btn = tk.Button(
        bmi_window,
        text="Close",
        font=("Times New Roman", 20),
        bg=BTN_COLOR,
        fg="white",
        width=15,
        activebackground=BTN_HOVER,
        activeforeground="white",
        command=confirm_exit,
        relief="flat"
    )
    exit_btn.pack(pady=10)

    # Footer
    tk.Label(bmi_window, text="© 2025 Health & Wellness Assistant",
             font=("Times New Roman", 14), bg=BACKGROUND, fg=TEXT_COLOR)\
        .pack(side="bottom", pady=10)