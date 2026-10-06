"""Command-line interface for the Password Strength Analyzer."""
import argparse
import getpass
import sys

from analyzer.report import analyze_password


def score_bar(score, width=20):
    """ASCII progress bar for a 0-100 score, e.g. [##########----------]."""
    filled = round(score / 100 * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def section(title, items, empty_message):
    """Format a titled bullet list; show empty_message when there are no items."""
    lines = ["", title]
    if items:
        lines.extend(f"  - {item}" for item in items)
    else:
        lines.append(f"  {empty_message}")
    return lines
