import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def step_counter_gui(parent=None):
    """Create and manage the Step Counter Log window."""
    window = tk.Toplevel(parent) if parent else tk.Tk()
    window.title("Step Counter Log")
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
            window.lift()           # Bring window back to front
            window.focus_force()    # Force focus on window

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
    tk.Label(
        window,
        text="Step Counter Log",
        font=("Times New Roman", 48, "bold"),
        bg=BG_COLOR,
        fg=BTN_COLOR
    ).pack(pady=40)

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

    # Save daily step goal and walked steps
    def save_steps():
        """Validate and save step data to steps.txt."""
        goal_str = goal_entry.get().strip()
        steps_str = steps_entry.get().strip()

        if goal_str in ("", "e.g. 10000"):
            messagebox.showerror("Error", "Please enter your daily step goal")
            return
        if steps_str in ("", "e.g. 7500"):
            messagebox.showerror("Error", "Please enter steps walked today")
            return

        if not goal_str.isdigit() or not steps_str.isdigit():
            messagebox.showerror("Error", "Please enter numbers only!")
            return

        goal = int(goal_str)
        steps = int(steps_str)

        today = datetime.now().strftime("%Y-%m-%d")

        # Append to file
        with open("steps.txt", "a") as file:
            file.write(f"{today},{goal},{steps}\n")

        remaining = max(goal - steps, 0)

        messagebox.showinfo(
            "Progress Saved",
            f"Date: {today}\n"
            f"Goal: {goal} steps\n"
            f"Steps Taken: {steps}\n"
            f"Remaining: {remaining} steps"
        )

        # Clear inputs and restore placeholders
        goal_entry.delete(0, tk.END)
        steps_entry.delete(0, tk.END)
        insert_placeholders()

        window.lift()
        window.focus_force()

    def insert_placeholders():
        """Apply placeholders to input fields."""
        set_placeholder(goal_entry, "e.g. 10000")
        set_placeholder(steps_entry, "e.g. 7500")

    # View all step log entries
    def view_history():
        """Display history of step logs."""
        try:
            with open("steps.txt", "r") as file:
                lines = file.readlines()
            if not lines:
                messagebox.showinfo("History", "No step logs yet.")
                return

            history = "\n".join(
                f"{i+1}. {line.strip().replace(',', ' | ')} steps" for i, line in enumerate(lines)
            )
        except FileNotFoundError:
            history = "No step logs found."

        hist_win = tk.Toplevel(window)
        hist_win.title("Step History")
        hist_win.configure(bg=BG_COLOR)
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w // 2) - (250)
        y = (screen_h // 2) - (250)
        hist_win.geometry(f"500x400+{x}+{y}")

        tk.Label(hist_win, text="Step Log History", font=("Times New Roman", 28, "bold"),
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
        tk.Label(hist_win, text=history, font=("Times New Roman", 18), justify="left",
                 bg=BG_COLOR, fg=TEXT_COLOR).pack(padx=40, pady=10)
        tk.Button(hist_win, text="Close", font=("Times New Roman", 18),
                  command=hist_win.destroy, width=17, bg=BTN_COLOR,
                  activebackground=BTN_HOVER, relief="flat").pack(pady=20)

    # Delete selected step log entries
    def delete_selected():
        """Allow user to delete one or more step log entries."""
        try:
            with open("steps.txt", "r") as file:
                lines = file.readlines()

            if not lines:
                messagebox.showinfo("Info", "No entries to delete.")
                return

            # Sort by date (newest first)
            lines.sort(key=lambda x: datetime.strptime(x.split(",")[0], "%Y-%m-%d"), reverse=True)

            del_win = tk.Toplevel(window)
            del_win.title("Delete Step Entries")
            del_win.configure(bg=BG_COLOR)
            screen_w = window.winfo_screenwidth()
            screen_h = window.winfo_screenheight()
            x = (screen_w // 2) - (250)
            y = (screen_h // 2) - (250)
            del_win.geometry(f"600x600+{x}+{y}")

            tk.Label(
                del_win,
                text="Select entries to delete:",
                font=("Times New Roman", 24),
                bg=BG_COLOR,
                fg=TEXT_COLOR
            ).pack(pady=20)

            listbox = tk.Listbox(
                del_win,
                font=("Times New Roman", 18),
                width=50,
                height=12,
                selectmode=tk.MULTIPLE
            )
            for i, line in enumerate(lines):
                date, goal, steps = line.strip().split(",")
                listbox.insert(tk.END, f"{i+1}. {date} | Goal: {goal} | Steps: {steps}")
            listbox.pack(padx=20, pady=10)

            def confirm_delete():
                """Delete selected entries from file."""
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("Warning", "No entries selected.")
                    return

                if messagebox.askyesno("Confirm Delete", f"Delete {len(selection)} selected entrie(s)?"):
                    new_lines = [lines[i] for i in range(len(lines)) if i not in selection]
                    with open("steps.txt", "w") as file:
                        file.writelines(new_lines)
                    messagebox.showinfo("Success", "Selected entries deleted successfully.")
                    del_win.destroy()

            tk.Button(del_win, text="Delete Selected", font=("Times New Roman", 20),
                      bg="red", width=20, activebackground="#C21807",
                      command=confirm_delete).pack(pady=20)

            tk.Button(del_win, text="Cancel", font=("Times New Roman", 18),
                      command=del_win.destroy, width=23, bg=BTN_COLOR,
                      activebackground=BTN_HOVER, relief="flat").pack(pady=10)

        except FileNotFoundError:
            messagebox.showinfo("Info", "No step log file found.")

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
    form_frame.pack(pady=40)

    tk.Label(form_frame, text="Daily Step Goal:", font=("Times New Roman", 24),
             bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=20, pady=15, sticky="w")
    goal_entry = tk.Entry(form_frame, font=("Times New Roman", 24), width=20,
                          relief="solid", bd=1)
    goal_entry.grid(row=0, column=1, padx=20, pady=15)

    tk.Label(form_frame, text="Steps Walked Today:", font=("Times New Roman", 24),
             bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=20, pady=15, sticky="w")
    steps_entry = tk.Entry(form_frame, font=("Times New Roman", 24), width=20,
                           relief="solid", bd=1)
    steps_entry.grid(row=1, column=1, padx=20, pady=15)

    insert_placeholders()

    tk.Button(form_frame, text="Save Today's Steps", font=("Times New Roman", 20),
              bg="aquamarine", activebackground="turquoise", command=save_steps)\
        .grid(row=2, column=0, columnspan=2, pady=10)

    # Main action buttons
    button_frame = tk.Frame(window, bg=BG_COLOR)
    button_frame.pack(pady=30)

    buttons = [
        ("View Step History", view_history),
        ("Delete Selected Entries", delete_selected),
        ("Close", close)
    ]

    for text, cmd in buttons:
        btn = tk.Button(
            button_frame,
            text=text,
            font=("Times New Roman", 24),
            command=cmd,
            width=30,
            bg=BTN_COLOR,
            fg="white",
            activebackground=BTN_HOVER,
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        )
        btn.pack(pady=12, ipadx=20, ipady=15)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # Footer
    tk.Label(
        window,
        text="© 2025 Health & Wellness Assistant",
        font=("Times New Roman", 14),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(side="bottom", pady=25)