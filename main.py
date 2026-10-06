"""Command-line interface for the Password Strength Analyzer."""
import argparse
import getpass
import sys

from analyzer.report import analyze_password


def score_bar(score, width=20):
    """ASCII progress bar for a 0-100 score, e.g. [##########----------]."""
    filled = round(score / 100 * width)
    return "[" + "#" * filled + "-" * (width - filled) + "]"
