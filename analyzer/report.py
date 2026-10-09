"""Combine all analysis modules into a single report."""
from analyzer.breach import check_breach
from analyzer.crack_time import estimate_crack_time, get_difficulty
from analyzer.feedback import build_feedback
from analyzer.strength import analyze_strength, get_rating


def analyze_password(password, breach_check=False):
    """Run every analysis and return one combined dictionary."""
    report = analyze_strength(password)
    report["crack_difficulty"] = get_difficulty(password)
    report["crack_times"] = estimate_crack_time(password)
    report.update(build_feedback(password))
    if breach_check:
        add_breach_info(report, password)
    return report


def add_breach_info(report, password):
    """Look the password up in known breaches and adjust the report if it was found."""
    count = check_breach(password)
    report["breach_count"] = count
    if count:
        report["score"] = min(report["score"], 10)
        report["rating"] = get_rating(report["score"])
        report["weaknesses"].append(f"Found in known data breaches ({count:,} times)")
        report["suggestions"].insert(0, "Stop using this password everywhere - it is publicly known")
