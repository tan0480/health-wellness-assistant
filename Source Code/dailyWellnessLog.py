import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from datetime import datetime
import os

def daily_wellness_log_gui(parent=None):
    window = tk.Toplevel(parent) if parent else tk.Tk()
    window.title("Daily Wellness Log")
    window.state("zoomed")
    window.configure(bg="#DBE9FF")

    # Only grab focus if opened from parent window
    if parent:
        window.grab_set()
        window.focus_force()

    BTN_COLOR = "#4A90E2"
    BTN_HOVER = "#357ABD"
    TEXT_COLOR = "#333333"
    BG_COLOR = "#DBE9FF"

    # Fade In
    window.attributes("-alpha", 0.0)
    def fade_in(alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            window.attributes("-alpha", alpha)
            window.after(10, fade_in, alpha)
    fade_in()

    def on_enter_blue(e): e.widget.config(bg=BTN_HOVER)
    def on_leave_blue(e): e.widget.config(bg=BTN_COLOR)

    # Placeholder functions
    def set_entry_placeholder(entry, text):
        entry.insert(0, text)
        entry.config(fg="grey")
        def on_focus_in(e):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg="black")
        def on_focus_out(e):
            if entry.get().strip() == "":
                entry.insert(0, text)
                entry.config(fg="grey")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def set_text_placeholder(widget, text):
        widget.insert("1.0", text)
        widget.config(fg="grey")
        def on_focus_in(e):
            if widget.get("1.0", "end-1c").strip() == text.strip():
                widget.delete("1.0", tk.END)
                widget.config(fg="black")
        def on_focus_out(e):
            if widget.get("1.0", "end-1c").strip() == "":
                widget.insert("1.0", text)
                widget.config(fg="grey")
        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    # Title
    tk.Label(window, text="Daily Wellness Log", font=("Times New Roman", 48, "bold"),
             bg=BG_COLOR, fg=BTN_COLOR).pack(pady=40)

    container = tk.Frame(window, bg=BG_COLOR)
    container.pack(expand=True)
    form = tk.Frame(container, bg=BG_COLOR)
    form.pack()

    LABEL_FONT = ("Times New Roman", 22)
    ENTRY_FONT = ("Times New Roman", 22)

    # Sleep
    tk.Label(form, text="Sleep (hours):", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)\
        .grid(row=0, column=0, sticky="e", padx=15, pady=6)
    sleep_entry = tk.Entry(form, font=ENTRY_FONT, width=22)
    sleep_entry.grid(row=0, column=1, pady=6)
    set_entry_placeholder(sleep_entry, "e.g. 7.5")

    # Hydration
    tk.Label(form, text="Hydration (litres):", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)\
        .grid(row=1, column=0, sticky="e", padx=15, pady=6)
    water_entry = tk.Entry(form, font=ENTRY_FONT, width=22)
    water_entry.grid(row=1, column=1, pady=6)
    set_entry_placeholder(water_entry, "e.g. 8")

    # Mood - Dropdown (FIXED)
    tk.Label(form, text="Mood:", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)\
        .grid(row=2, column=0, sticky="e", padx=15, pady=6)

    mood_var = tk.StringVar()
    MOOD_VALUES = ["Happy", "Neutral", "Sad", "Stressed", "Energetic"]
    
    mood_combo = ttk.Combobox(form, textvariable=mood_var, values=MOOD_VALUES,
                              state="readonly", font=ENTRY_FONT, width=21)
    mood_combo.grid(row=2, column=1, pady=6, ipady=4)
    mood_combo.set("Select mood...")  # Set hint after creating combo

    # Meals
    MEALS_PLACEHOLDER = "e.g. Breakfast: oats, Lunch: rice & chicken"
    tk.Label(form, text="Meals:", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)\
        .grid(row=3, column=0, sticky="ne", padx=15, pady=6)
    meals_entry = tk.Text(form, font=ENTRY_FONT, width=28, height=2)
    meals_entry.grid(row=3, column=1, pady=6)
    set_text_placeholder(meals_entry, MEALS_PLACEHOLDER)

    # Reflection
    REFLECTION_PLACEHOLDER = "e.g. Felt slightly tired"
    tk.Label(form, text="Reflection:", font=LABEL_FONT, bg=BG_COLOR, fg=TEXT_COLOR)\
        .grid(row=4, column=0, sticky="ne", padx=15, pady=6)
    reflection_entry = tk.Text(form, font=ENTRY_FONT, width=28, height=2)
    reflection_entry.grid(row=4, column=1, pady=6)
    set_text_placeholder(reflection_entry, REFLECTION_PLACEHOLDER)

    def save_log():
        sleep_raw = sleep_entry.get().strip()
        water_raw = water_entry.get().strip()
        
        # Try multiple ways to get the mood value
        selected_mood = mood_combo.get()  # Get directly from combobox
        mood_var_value = mood_var.get()    # Get from StringVar
        
        meals = meals_entry.get("1.0", "end-1c").strip()
        reflection = reflection_entry.get("1.0", "end-1c").strip()

        # Clean placeholder check
        if sleep_entry.cget('fg') == 'grey':
            sleep_raw = ""
        if water_entry.cget('fg') == 'grey':
            water_raw = ""
        if meals_entry.cget('fg') == 'grey':
            meals = ""
        if reflection_entry.cget('fg') == 'grey':
            reflection = ""

        # DEBUG: Print both values
        print(f"DEBUG - mood_combo.get(): '{selected_mood}'")
        print(f"DEBUG - mood_var.get(): '{mood_var_value}'")
        print(f"DEBUG - MOOD_VALUES: {MOOD_VALUES}")

        # Validation: Check mood is selected (and not the placeholder)
        if not selected_mood or selected_mood == "Select mood..." or selected_mood not in MOOD_VALUES:
            messagebox.showerror("Error", "Please select a mood.", parent=window)
            mood_combo.focus_set()
            return

        # Sleep validation
        if not sleep_raw:
            messagebox.showerror("Error", "Please enter your sleep hours.", parent=window)
            sleep_entry.focus_set()
            return
        try:
            sleep = float(sleep_raw)
            if sleep <= 0 or sleep >= 24:
                messagebox.showerror("Invalid Input", "Sleep hours must be greater than 0 and less than 24.", parent=window)
                sleep_entry.focus_set()
                return
            if sleep > 18:
                if not messagebox.askyesno("High Value", f"You entered {sleep} hours of sleep. Is this correct?", parent=window):
                    sleep_entry.focus_set()
                    return
        except ValueError:
            messagebox.showerror("Invalid Input", "Sleep must be a number (e.g., 7 or 7.5).", parent=window)
            sleep_entry.focus_set()
            return

        # Water validation
        if not water_raw:
            messagebox.showerror("Error", "Please enter how many litres of water.", parent=window)
            water_entry.focus_set()
            return
        if not water_raw.replace('.', '', 1).isdigit():
            messagebox.showerror("Invalid Input", "Hydration must be a number.", parent=window)
            water_entry.focus_set()
            return
        water = float(water_raw)
        if water < 0 or water > 30:
            messagebox.showerror("Invalid Input", "Hydration should be between 0 and 30 litres.", parent=window)
            water_entry.focus_set()
            return
        if water > 20:
            if not messagebox.askyesno("High Value", f"You drank {water} litres of water. Is this correct?", parent=window):
                water_entry.focus_set()
                return

        # Meals validation
        if not meals:
            messagebox.showerror("Missing Input", "Please record your meals for the day.", parent=window)
            meals_entry.focus_set()
            return
        if len(meals) < 5:
            messagebox.showerror("Input too short", "Please provide more detail about your meals (at least 5 characters).", parent=window)
            meals_entry.focus_set()
            return

        # Reflection validation
        if not reflection:
            messagebox.showerror("Missing Input", "Please write a short reflection on how you felt.", parent=window)
            reflection_entry.focus_set()
            return
        if len(reflection) < 3:
            messagebox.showerror("Input too short", "Reflection is too short.", parent=window)
            reflection_entry.focus_set()
            return

        # Check for duplicate entry
        today = datetime.now().strftime('%Y-%m-%d')
        if os.path.exists("wellness.txt"):
            try:
                with open("wellness.txt", "r", encoding="utf-8") as f:
                    if any(line.startswith(today + "|") for line in f):
                        if not messagebox.askyesno("Already Logged", f"You already have an entry for today ({datetime.now().strftime('%B %d, %Y')}).\n\nSave another entry for today?", parent=window):
                            return
            except: pass

        # Save to file - THIS IS THE KEY LINE
        try:
            save_line = f"{today}|{sleep}|{water}|{selected_mood}|{meals}|{reflection}\n"
            print(f"DEBUG - Saving line: {save_line}")  # Debug print
            
            with open("wellness.txt", "a", encoding="utf-8") as file:
                file.write(save_line)
            messagebox.showinfo("Success! 🎉", "Daily wellness log saved successfully!", parent=window)
        except Exception as e:
            messagebox.showerror("Save Failed", f"Could not save log:\n{e}", parent=window)

    def view_log_history():
        history_win = tk.Toplevel(window)
        history_win.title("Wellness Log History")
        history_win.geometry("900x750")
        history_win.configure(bg=BG_COLOR)
        history_win.grab_set()
        history_win.focus_force()

        tk.Label(history_win, text="Wellness Log History", font=("Times New Roman", 36, "bold"),
                 bg=BG_COLOR, fg=BTN_COLOR).pack(pady=40)

        log_area = scrolledtext.ScrolledText(history_win, font=("Courier New", 16), bg="#F8FBFF", fg="#2C3E50",
                                             padx=50, pady=20, spacing1=6, spacing2=2, spacing3=10,
                                             relief="flat", borderwidth=0)
        log_area.pack(fill="both", expand=True, padx=60, pady=(0, 40))

        mood_emojis = {"Happy": "😊", "Neutral": "😐", "Sad": "😔", "Stressed": "😰", "Energetic": "⚡"}

        if not os.path.exists("wellness.txt") or os.path.getsize("wellness.txt") == 0:
            log_area.insert(tk.END, "No logs yet. Your wellness journey starts today! 🌿\n")
        else:
            try:
                with open("wellness.txt", "r", encoding="utf-8") as file:
                    logs = file.readlines()
                
                # Sort by date (newest first) - extract date from each line
                logs.sort(key=lambda x: x.split("|")[0] if "|" in x else "", reverse=True)
                
                for i, line in enumerate(logs):
                    parts = line.strip().split("|")
                    if len(parts) < 6:
                        continue
                    
                    # Extract each field individually
                    date_str = parts[0]
                    sleep = parts[1]
                    water = parts[2]
                    mood = parts[3]  # This is the mood field
                    meals = parts[4]
                    reflection = parts[5]
                    
                    # DEBUG print
                    print(f"DEBUG - Reading mood: '{mood}'")
                    
                    try:
                        pretty_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
                    except:
                        pretty_date = date_str
                    
                    emoji = mood_emojis.get(mood, "❓")
                    entry = f"{pretty_date}\n• Sleep:      {sleep} hours\n• Hydration:  {water} litres\n• Mood:       {emoji} {mood}\n• Meals:      {meals if meals else 'Not recorded'}\n• Reflection: {reflection if reflection else 'No reflection'}\n"
                    log_area.insert(tk.END, entry)
                    if i < len(logs) - 1:
                        log_area.insert(tk.END, "\n" + "―" * 30 + "\n")
            except Exception as e:
                log_area.insert(tk.END, f"Error reading logs: {e}\n")

        log_area.config(state="disabled")

    def delete_selected_entries():
        try:
            with open("wellness.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
            if not lines:
                messagebox.showinfo("Info", "No entries to delete.", parent=window)
                return
            lines.sort(key=lambda x: x.split("|")[0], reverse=True)
            del_win = tk.Toplevel(window)
            del_win.title("Delete Wellness Entries")
            del_win.geometry("950x700")
            del_win.configure(bg=BG_COLOR)
            del_win.grab_set()
            del_win.focus_force()
            tk.Label(del_win, text="Select entries to delete:", font=("Times New Roman", 26), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=30)
            listbox = tk.Listbox(del_win, font=("Courier New", 15), selectmode=tk.MULTIPLE, height=18)
            listbox.pack(padx=60, pady=10, fill="both", expand=True)
            mood_emojis = {"Happy": "😊", "Neutral": "😐", "Sad": "😔", "Stressed": "😰", "Energetic": "⚡"}
            for i, line in enumerate(lines):
                parts = line.strip().split("|")
                if len(parts) < 6:
                    continue
                date_str = parts[0]
                sleep = parts[1]
                water = parts[2]
                mood = parts[3]
                try:
                    pretty_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
                except:
                    pretty_date = date_str
                emoji = mood_emojis.get(mood, "?")
                display = f"{i+1:2}. {pretty_date} | Sleep: {sleep}h | Water: {water}L | Mood: {emoji} {mood}"
                listbox.insert(tk.END, display)

            def confirm_delete():
                selected = listbox.curselection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select at least one entry to delete.", parent=del_win)
                    return
                if messagebox.askyesno("Confirm Delete", f"Permanently delete {len(selected)} selected entr{'y' if len(selected)==1 else 'ies'}?", parent=del_win):
                    remaining = [lines[i] for i in range(len(lines)) if i not in selected]
                    with open("wellness.txt", "w", encoding="utf-8") as f:
                        f.writelines(remaining)
                    messagebox.showinfo("Success", "Selected entries deleted!", parent=del_win)
                    del_win.destroy()

            tk.Button(del_win, text="Delete Selected", font=("Times New Roman", 20), bg="#D32F2F", fg="white", command=confirm_delete, relief="flat").pack(pady=20)
            tk.Button(del_win, text="Cancel", font=("Times New Roman", 18), bg=BTN_COLOR, fg="white", command=del_win.destroy, relief="flat").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load entries: {e}", parent=window)

    def confirm_exit():
        if messagebox.askyesno("Exit", "Are you sure you want to close this window?"):
            window.destroy()
        else:
            window.lift()
            window.focus_force()

    window.protocol("WM_DELETE_WINDOW", confirm_exit)

    btn_frame = tk.Frame(window, bg=BG_COLOR)
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="Save Daily Log", font=("Times New Roman", 20, "bold"),
              bg="aquamarine", activebackground="turquoise", fg="black",
              relief="solid", bd=2, highlightbackground="black",
              cursor="hand2", command=save_log, width=20, pady=10).pack(pady=12)

    blue_button_style = {"font": ("Times New Roman", 25), "width": 35, "bg": BTN_COLOR,
                         "fg": "white", "activebackground": BTN_HOVER, "relief": "flat", "cursor": "hand2"}

    for text, cmd in [("View Log History", view_log_history),
                      ("Delete Selected Entries", delete_selected_entries),
                      ("Close", confirm_exit)]:
        btn = tk.Button(btn_frame, text=text, command=cmd, **blue_button_style)
        btn.pack(pady=6)
        btn.bind("<Enter>", on_enter_blue)
        btn.bind("<Leave>", on_leave_blue)

    tk.Label(window, text="© 2025 Health & Wellness Assistant",
             font=("Times New Roman", 14), bg=BG_COLOR, fg=TEXT_COLOR).pack(side="bottom", pady=13)

    # Set focus after window is fully loaded - this ensures consistent behavior
    window.update_idletasks()
    window.after(100, lambda: sleep_entry.focus_set())