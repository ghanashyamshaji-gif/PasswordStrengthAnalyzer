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
