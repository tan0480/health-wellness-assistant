import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date

def medication_reminder_gui(parent=None):
    """Create and manage the Medication Reminder window."""
    window = tk.Toplevel(parent) if parent else tk.Tk()
    window.title("Medication Reminder")
    window.state('zoomed')
    window.configure(bg="#DBE9FF")

    # Color constants
    BTN_COLOR = "#4A90E2"       # Default button color
    BTN_HOVER = "#357ABD"       # Hover button color
    TEXT_COLOR = "#333333"      # General text color
    BG_COLOR = "#DBE9FF"        # Window background

    # Confirm exit when user clicks window close button (X)
    def confirm_exit():
        """Ask for confirmation before closing the window."""
        if messagebox.askyesno("Exit", "Are you sure you want to close this window?"):
            window.destroy()
        else:
            window.lift()
            window.focus_force()

    window.protocol("WM_DELETE_WINDOW", confirm_exit)

    # Fade-in animation for smooth appearance
    window.attributes("-alpha", 0.0)
    def fade_in(alpha=0.0):
        """Gradually increase window opacity."""
        if alpha < 1.0:
            alpha += 0.5
            window.attributes("-alpha", alpha)
            window.after(5, fade_in, alpha)
    fade_in()

    # Title label
    tk.Label(window, text="Medication Reminder", font=("Times New Roman", 48, "bold"),
             bg=BG_COLOR, fg=BTN_COLOR).pack(pady=40)

    # Hover effects for buttons
    def on_enter(e): e.widget.config(bg=BTN_HOVER)
    def on_leave(e): e.widget.config(bg=BTN_COLOR)

    # Placeholder support for entry fields
    def set_placeholder(entry, placeholder):
        """Set placeholder text and handle focus events."""
        entry.insert(0, placeholder)
        entry.config(fg="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get().strip() == "":
                entry.insert(0, placeholder)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # Add new medication to file
    def add_medication_gui():
        """Save new medication details to medication.txt."""
        name = name_entry.get().strip()
        time = time_entry.get().strip()
        dose = dose_entry.get().strip()

        # Input validation
        if not name or name == "e.g. Paracetamol":
            messagebox.showerror("Error", "Please enter medication name")
            window.lift()
            window.focus_force()
            return
        if not time or time == "HH:MM":
            messagebox.showerror("Error", "Please enter time")
            window.lift()
            window.focus_force()
            return
        if not dose or dose == "e.g. 1 Tablet":
            messagebox.showerror("Error", "Please enter dosage")
            window.lift()
            window.focus_force()
            return

        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Time must be in HH:MM (24-hour)")
            return

        # Save with empty taken_date
        with open("medication.txt", "a") as file:
            file.write(f"{name},{time},{dose},\n")

        messagebox.showinfo("Success", "Medication schedule saved!")
        name_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        dose_entry.delete(0, tk.END)
        insert_placeholders()

        window.lift()
        window.focus_force()

    def insert_placeholders():
        """Apply placeholders to input fields."""
        set_placeholder(name_entry, "e.g. Paracetamol")
        set_placeholder(time_entry, "HH:MM")
        set_placeholder(dose_entry, "e.g. 1 Tablet")

    # Check for due medications today
    def check_medication_gui():
        """Check and display reminders for medications due today."""
        today = date.today().isoformat()
        current_time = datetime.now()
        current_minutes = current_time.hour * 60 + current_time.minute
        reminders = []
        lines = []

        try:
            with open("medication.txt", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            messagebox.showinfo("No Schedule", "No medications found.")
            window.lift()
            window.focus_force()
            return

        updated_lines = []
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) < 4:
                parts.append("")
            name, time_str, dose, taken_date = parts[:4]

            try:
                t = datetime.strptime(time_str, "%H:%M")
                med_minutes = t.hour * 60 + t.minute

                if (taken_date != today or not taken_date) and med_minutes <= current_minutes:
                    reminders.append((name, time_str, dose, line.strip()))
            except ValueError:
                continue

            updated_lines.append(",".join(parts) + "\n")

        if reminders:
            msg = "Time to Take:\n\n" + "\n".join(
                f"• {name}  |  Dosage: {dose}  |  Time: {time}" for name, time, dose, _ in reminders
            )
            top = tk.Toplevel(window)
            top.title("Medication Reminder")
            top.configure(bg=BG_COLOR)
            screen_w = window.winfo_screenwidth()
            screen_h = window.winfo_screenheight()
            x = (screen_w // 2) - (250)
            y = (screen_h // 2) - (250)
            top.geometry(f"700x600+{x}+{y}")

            tk.Label(top, text="Time to Take Medication", font=("Times New Roman", 28, "bold"),
                     bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
            tk.Label(top, text=msg, font=("Times New Roman", 20), justify="left",
                     bg=BG_COLOR, fg=TEXT_COLOR).pack(padx=30, pady=10)

            def mark_all_taken():
                """Mark all due medications as taken today."""
                today = date.today().isoformat()
                new_lines = []
                for line in updated_lines:
                    parts = line.strip().split(",")
                    name, time_str, dose, _ = parts[:4]
                    if any(n == name and t == time_str for n, t, _, _ in reminders):
                        parts[3] = today
                    new_lines.append(",".join(parts) + "\n")

                with open("medication.txt", "w") as file:
                    file.writelines(new_lines)

                messagebox.showinfo("Success", "Marked as taken!")
                top.destroy()
                window.lift()
                window.focus_force()

            tk.Button(top, text="Mark All as Taken", font=("Times New Roman", 20),
                      bg="aquamarine", activebackground="turquoise", command=mark_all_taken).pack(pady=20)

            tk.Button(top, text="Close", font=("Times New Roman", 18),
                      command=top.destroy, width=17, bg=BTN_COLOR, activebackground=BTN_HOVER,
                      relief="flat").pack(pady=20)
        else:
            messagebox.showinfo("No Reminder", "No medication due right now.")

        window.lift()
        window.focus_force()

    # View all scheduled medications
    def view_history_gui():
        """Display list of all scheduled medications."""
        try:
            with open("medication.txt", "r") as file:
                lines = file.readlines()
            if not lines:
                messagebox.showinfo("History", "No medications scheduled.")
                return

            history = "\n".join(
                f"{i+1}. {line.strip().replace(',', ' | ')}" for i, line in enumerate(lines)
            )
        except FileNotFoundError:
            history = "No medications scheduled yet."

        hist_win = tk.Toplevel(window)
        hist_win.title("Medication Schedule")
        hist_win.configure(bg=BG_COLOR)
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w // 2) - (250)
        y = (screen_h // 2) - (250)
        hist_win.geometry(f"500x400+{x}+{y}")

        tk.Label(hist_win, text="Current Schedule", font=("Times New Roman", 24, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
        tk.Label(hist_win, text=history, font=("Times New Roman", 18), justify="left",
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(padx=30, pady=10)
        tk.Button(hist_win, text="Close", font=("Times New Roman", 18),
                  command=hist_win.destroy, width=20, bg=BTN_COLOR,
                  activebackground=BTN_HOVER, relief="flat").pack(pady=20)

        window.lift()
        window.focus_force()

    # View medications taken today
    def view_taken_today_gui():
        """Show medications marked as taken on current date."""
        today = date.today().isoformat()
        taken = []
        try:
            with open("medication.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) >= 4 and parts[3] == today:
                        taken.append(parts[0] + " | " + parts[1] + " | " + parts[2])
        except FileNotFoundError:
            pass

        taken_win = tk.Toplevel(window)
        taken_win.title("Taken Today")
        taken_win.configure(bg=BG_COLOR)
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w // 2) - (250)
        y = (screen_h // 2) - (250)
        taken_win.geometry(f"500x400+{x}+{y}")

        tk.Label(taken_win, text="Taken Today", font=("Times New Roman", 24, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
        tk.Label(taken_win, text="\n".join(taken) or "Nothing taken today.",
                 font=("Times New Roman", 18), bg=BG_COLOR, fg=TEXT_COLOR).pack(padx=30, pady=10)
        tk.Button(taken_win, text="Close", font=("Times New Roman", 18),
                  command=taken_win.destroy, width=20, bg=BTN_COLOR,
                  activebackground=BTN_HOVER, relief="flat").pack(pady=20)

        window.lift()
        window.focus_force()

    # Delete selected medications
    def delete_single_medication_gui():
        """Allow user to delete one or more medication entries."""
        try:
            with open("medication.txt", "r") as file:
                lines = file.readlines()
            if not lines:
                messagebox.showinfo("Info", "No medications to delete.")
                return

            lines.sort(key=lambda x: datetime.strptime(x.split(",")[1], "%H:%M"))

            del_win = tk.Toplevel(window)
            del_win.title("Delete Medication")
            del_win.configure(bg=BG_COLOR)
            screen_w = window.winfo_screenwidth()
            screen_h = window.winfo_screenheight()
            x = (screen_w // 2) - (250)
            y = (screen_h // 2) - (250)
            del_win.geometry(f"600x600+{x}+{y}")

            tk.Label(del_win, text="Select entries to delete:", font=("Times New Roman", 24),
                     bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

            listbox = tk.Listbox(del_win, font=("Times New Roman", 18), width=60,
                                 height=12, selectmode=tk.MULTIPLE)
            for i, line in enumerate(lines):
                name, time, dose, _ = line.strip().split(",", 3)
                listbox.insert(tk.END, f"{i+1}. {name} | {time} | {dose}")
            listbox.pack(padx=20, pady=10)

            def delete_selected():
                """Delete selected entries from file."""
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("Warning", "No entries selected.")
                    window.lift()
                    window.focus_force()
                    del_win.lift()
                    del_win.focus_force()
                    return
                if messagebox.askyesno("Confirm", f"Delete {len(selection)} entrie(s)?"):
                    new_lines = [lines[i] for i in range(len(lines)) if i not in selection]
                    with open("medication.txt", "w") as file:
                        file.writelines(new_lines)
                    messagebox.showinfo("Success", "Deleted successfully.")
                    del_win.destroy()
                    view_history_gui()
                else:
                    window.lift()
                    window.focus_force()
                    del_win.lift()
                    del_win.focus_force()

            tk.Button(del_win, text="Delete Selected", font=("Times New Roman", 20), width=20,
                      bg="red", activebackground="#C21807", command=delete_selected).pack(pady=10)
            tk.Button(del_win, text="Cancel", font=("Times New Roman", 18),
                      command=del_win.destroy, width=23, bg=BTN_COLOR,
                      activebackground=BTN_HOVER, relief="flat").pack(pady=10)

        except FileNotFoundError:
            messagebox.showerror("Error", "No schedule found.")
            window.lift()
            window.focus_force()

        window.lift()
        window.focus_force()

    # Close current window with confirmation
    def close():
        """Close window after confirmation."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            window.destroy()
        else:
            window.lift()
            window.focus_force()

    # Input form
    form_frame = tk.Frame(window, bg=BG_COLOR)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Medication Name:", font=("Times New Roman", 24),
             bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=15, pady=10, sticky="w")
    name_entry = tk.Entry(form_frame, font=("Times New Roman", 24), width=30, relief="solid", bd=1)
    name_entry.grid(row=0, column=1, padx=15, pady=10)

    tk.Label(form_frame, text="Time (HH:MM):", font=("Times New Roman", 24),
             bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=15, pady=10, sticky="w")
    time_entry = tk.Entry(form_frame, font=("Times New Roman", 24), width=30, relief="solid", bd=1)
    time_entry.grid(row=1, column=1, padx=15, pady=10)

    tk.Label(form_frame, text="Dosage:", font=("Times New Roman", 24),
             bg=BG_COLOR, fg=TEXT_COLOR).grid(row=2, column=0, padx=15, pady=10, sticky="w")
    dose_entry = tk.Entry(form_frame, font=("Times New Roman", 24), width=30, relief="solid", bd=1)
    dose_entry.grid(row=2, column=1, padx=15, pady=10)

    tk.Button(form_frame, text="Add Medication", font=("Times New Roman", 20),
              bg="aquamarine", activebackground="turquoise", command=add_medication_gui)\
        .grid(row=3, column=0, columnspan=2, pady=10)

    insert_placeholders()

    # Main action buttons
    button_frame = tk.Frame(window, bg=BG_COLOR)
    button_frame.pack()

    buttons = [
        ("Check Reminders Now", check_medication_gui),
        ("View Schedule", view_history_gui),
        ("View Medication Taken Today", view_taken_today_gui),
        ("Delete Medications", delete_single_medication_gui),
        ("Close", close)
    ]

    for text, cmd in buttons:
        btn = tk.Button(button_frame, text=text, font=("Times New Roman", 24),
                        command=cmd, width=30, bg=BTN_COLOR, fg="white",
                        activebackground=BTN_HOVER, activeforeground="white",
                        relief="flat", cursor="hand2")
        btn.pack(pady=5, ipadx=20, ipady=10)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Footer
    tk.Label(window, text="© 2025 Health & Wellness Assistant",
             font=("Times New Roman", 14), bg=BG_COLOR, fg=TEXT_COLOR)\
        .pack(side="bottom", pady=10)