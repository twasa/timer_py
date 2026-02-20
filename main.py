import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
import winsound
import sys
import os

from playsound3 import playsound

class TimerRow:
    def __init__(self, app, master, total_seconds):
        self.app = app
        self.app_path = self.get_path()
        self.master = master
        self.remaining = total_seconds
        self.is_running = True
        self.is_paused = False

        # UI Row Frame
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='x', padx=10, pady=5)

        self.label_name = ttk.Label(self.frame, width=12, font=('Segoe UI', 9, 'bold'))
        self.label_name.pack(side='left')

        self.label_time = ttk.Label(self.frame, text=self.format_time(), font=('Courier New', 12), width=10)
        self.label_time.pack(side='left', padx=10)

        # Control Buttons
        self.btn_remove = ttk.Button(self.frame, text="✖", width=3, command=self.remove_timer)
        self.btn_remove.pack(side='right', padx=2)

        self.btn_edit = ttk.Button(self.frame, text="✎", width=3, command=self.open_edit_window)
        self.btn_edit.pack(side='right', padx=2)

        self.btn_pause = ttk.Button(self.frame, text="‖", width=3, command=self.toggle_pause)
        self.btn_pause.pack(side='right', padx=2)

        self.thread = threading.Thread(target=self.run_countdown, daemon=True)
        self.thread.start()

    def format_time(self):
        hrs, rem = divmod(self.remaining, 3600)
        mins, secs = divmod(rem, 60)
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.btn_pause.config(text="▶" if self.is_paused else "‖")

    def open_edit_window(self):
        """Opens a popup to edit the specific timer's details without deleting it."""
        was_paused = self.is_paused
        self.is_paused = True # Pause while editing
        
        edit_win = tk.Toplevel(self.app.root)
        edit_win.geometry("250x150")
        sec_ent = ttk.Entry(edit_win)
        sec_ent.insert(0, "0")
        sec_ent.pack()

        def save_changes():
            try:
                adjustment = int(sec_ent.get())
                self.remaining = max(0, self.remaining + adjustment)
                self.label_time.config(text=self.format_time())
                self.is_paused = was_paused # Return to original state
                edit_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number for seconds.")

        ttk.Button(edit_win, text="Save", command=save_changes).pack(pady=10)

    def remove_timer(self):
        self.is_running = False
        self.frame.destroy()

    def run_countdown(self):
        while self.remaining > 0 and self.is_running:
            if not self.is_paused:
                time.sleep(1)
                self.remaining -= 1
                try:
                    self.label_time.config(text=self.format_time())
                except: break
        
        if self.remaining <= 0 and self.is_running:
            self.label_time.config(text="00:00:00", foreground="red")
            self.play_alarm()

    def play_alarm(self):
        audio_path = f"{self.app_path}/audio/alarm.wav"
        if os.path.exists(audio_path):
            playsound(audio_path)
        else:
            self.app.root.attributes('-topmost', True)
            self.app.root.attributes('-topmost', False)

    def get_path(self) -> str:
        script_invocation_path = sys.argv[0]
        absolute_script_path = os.path.abspath(script_invocation_path)
        return os.path.dirname(absolute_script_path)

class MultiTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Timer")
        self.root.geometry("450x550")

        # Input Area
        input_f = ttk.LabelFrame(root, text="Create Timer")
        input_f.pack(padx=10, pady=10, fill="x")

        self.name_ent = ttk.Entry(input_f)

        t_frame = ttk.Frame(input_f)
        t_frame.pack(pady=5)
        self.h = self.add_sb(t_frame, "H", 0)
        self.m = self.add_sb(t_frame, "M", 2)
        self.s = self.add_sb(t_frame, "S", 4)

        ttk.Button(input_f, text="Start New Timer", command=self.add_timer).pack(pady=10)

        # Scrollable List
        self.canvas = tk.Canvas(root)
        self.scroll_f = ttk.Frame(self.canvas)
        self.scroll_f.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_f, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

    def add_sb(self, p, l, c):
        ttk.Label(p, text=l).grid(row=0, column=c)
        sb = ttk.Spinbox(p, from_=0, to=59, width=3)
        sb.set(0); sb.grid(row=0, column=c+1, padx=2)
        return sb

    def add_timer(self):
        total = int(self.h.get())*3600 + int(self.m.get())*60 + int(self.s.get())
        if total > 0:
            TimerRow(self, self.scroll_f, total)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTimerApp(root)
    root.mainloop()
