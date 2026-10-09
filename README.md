# Password Strength Analyzer

![Tests](https://github.com/ghanashyamshaji-gif/PasswordStrengthAnalyzer/actions/workflows/tests.yml/badge.svg)

A Python tool that analyzes password strength and provides a detailed security assessment.

## Features

- Strength rating
- Password score from 0-100
- Password entropy calculation
- Estimated crack difficulty
- Detection of weak characteristics
- Suggestions for improving password security

## Tech Stack
- Python 3
- tkinter (graphical interface, included with the standard Python installer on Windows)

## Usage

```bash
python main.py                  # prompts for a password (hidden when possible)
python main.py --show           # visible typing
python main.py -p "MyPass"      # pass directly (stays in shell history)
python main.py --json -p "x"    # machine-readable output
python main.py --check-breach       # also look it up in known data breaches (needs internet)
python main.py --gui                # open the graphical interface
```

## Running the tests

    python run_tests.py

The tests use only the standard library (unittest), so nothing needs installing.

## Breach check (optional)

With --check-breach the tool asks the Have I Been Pwned "Pwned Passwords" service whether a password has appeared in a data breach. Your password is never sent: only the first 5 characters of its SHA-1 hash leave your computer, and the match is done locally (a technique called k-anonymity). If you are offline the check is skipped and the rest of the report still works.

## Status

🚧 Analysis engine and command-line interface complete; automated tests, pre-commit hook, CI, optional breach check and a graphical interface included.
