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


def format_report(report):
    """Turn an analysis report dict into printable text."""
    other_weaknesses = [w for w in report["weaknesses"] if w not in report["patterns"]]
    lines = [
        "=" * 56,
        "PASSWORD STRENGTH REPORT",
        "=" * 56,
        f"Strength        : {report['rating']}",
        f"Score           : {report['score']}/100 {score_bar(report['score'])}",
        f"Entropy         : {report['entropy']} bits",
        f"Crack difficulty: {report['crack_difficulty']}",
        "",
        "Estimated time to crack (average case):",
    ]
    lines.extend(f"  - {label}: {text}" for label, text in report["crack_times"].items())
    lines += section("Common patterns found:", report["patterns"], "None detected")
    lines += section("Why it is weak:", other_weaknesses, "No length or variety problems")
    lines += section("How to improve it:", report["suggestions"], "Nothing to add")
    return "\n".join(lines)


def read_password(show):
    """Ask for a password; hide the typing when running in a real terminal."""
    if sys.stdin.isatty() and not show:
        return getpass.getpass("Enter password to analyze: ")
    return input("Enter password to analyze: ")


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze the strength of a password.")
    parser.add_argument("-p", "--password",
                        help="password to analyze (stays in shell history, so prefer the prompt)")
    parser.add_argument("--show", action="store_true",
                        help="show what you type instead of hiding it")
    # more options go here
    return parser.parse_args()


def main():
    args = parse_args()
    if args.password is not None:
        password = args.password
    else:
        password = read_password(args.show)
    report = analyze_password(password)
    print(format_report(report))


if __name__ == "__main__":
    main()
