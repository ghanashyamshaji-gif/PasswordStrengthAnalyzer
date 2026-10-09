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
