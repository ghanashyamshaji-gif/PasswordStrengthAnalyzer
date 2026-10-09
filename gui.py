"""Simple graphical interface for the Password Strength Analyzer."""
import queue
import threading
import tkinter as tk
from tkinter import ttk

from analyzer.display import bar_fraction, color_for_rating, headline
from analyzer.report import analyze_password
from main import format_report

BAR_WIDTH = 480
BAR_HEIGHT = 22
IDLE_TEXT = "Type a password to see its strength"


class PasswordApp:
    """The main window: password box, strength bar and detailed report."""

    def __init__(self, root):
        self.root = root
        self.results = queue.Queue()
        self.password_var = tk.StringVar()
        self.show_var = tk.BooleanVar(value=False)
        root.title("Password Strength Analyzer")
        root.minsize(620, 600)
        self.build_input()
        self.build_results()
        self.password_var.trace_add("write", self.on_change)
        self.clear()

    def build_input(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="x")
        ttk.Label(frame, text="Password:").pack(anchor="w")
        self.entry = ttk.Entry(frame, textvariable=self.password_var, show="*", width=50)
        self.entry.pack(fill="x", pady=(2, 6))
        self.entry.focus_set()
        row = ttk.Frame(frame)
        row.pack(fill="x")
        ttk.Checkbutton(row, text="Show password", variable=self.show_var,
                        command=self.toggle_show).pack(side="left")
        self.breach_button = ttk.Button(row, text="Check data breaches",
                                        command=self.start_breach_check)
        self.breach_button.pack(side="right")
        ttk.Label(frame, foreground="#666666",
                  text="The breach check sends only the first 5 characters of a hash, never the password."
                  ).pack(anchor="w", pady=(6, 0))

    def build_results(self):
        frame = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        frame.pack(fill="both", expand=True)
        self.headline_label = tk.Label(frame, text="", font=("Segoe UI", 16, "bold"), anchor="w")
        self.headline_label.pack(fill="x")
        self.bar = tk.Canvas(frame, width=BAR_WIDTH, height=BAR_HEIGHT, highlightthickness=0)
        self.bar.pack(anchor="w", pady=8)
        box = ttk.Frame(frame)
        box.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(box)
        scrollbar.pack(side="right", fill="y")
        self.details = tk.Text(box, height=22, width=70, wrap="none", state="disabled",
                               font=("Consolas", 10), yscrollcommand=scrollbar.set)
        self.details.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.details.yview)

    def draw_bar(self, score, color):
        self.bar.delete("all")
        self.bar.create_rectangle(0, 0, BAR_WIDTH, BAR_HEIGHT, fill="#e6e6e6", outline="")
        filled = int(BAR_WIDTH * bar_fraction(score))
        self.bar.create_rectangle(0, 0, filled, BAR_HEIGHT, fill=color, outline="")

    def set_details(self, text):
        self.details.config(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text)
        self.details.config(state="disabled")

    def show_report(self, report):
        color = color_for_rating(report["rating"])
        self.headline_label.config(text=headline(report), fg=color)
        self.draw_bar(report["score"], color)
        self.set_details(format_report(report))

    def clear(self):
        self.headline_label.config(text=IDLE_TEXT, fg="#666666")
        self.draw_bar(0, color_for_rating(None))
        self.set_details("")
