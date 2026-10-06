"""Combine all analysis modules into a single report."""
from analyzer.crack_time import estimate_crack_time, get_difficulty
from analyzer.feedback import build_feedback
from analyzer.strength import analyze_strength


def analyze_password(password):
    """Run every analysis and return one combined dictionary."""
    report = analyze_strength(password)
    report["crack_difficulty"] = get_difficulty(password)
    report["crack_times"] = estimate_crack_time(password)
    report.update(build_feedback(password))
    return report
