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

## Usage

```bash
python main.py                  # prompts for a password (hidden when possible)
python main.py --show           # visible typing
python main.py -p "MyPass"      # pass directly (stays in shell history)
python main.py --json -p "x"    # machine-readable output
```

## Running the tests

    python run_tests.py

The tests use only the standard library (unittest), so nothing needs installing.

## Status

🚧 Analysis engine and command-line interface complete; automated tests, pre-commit hook and CI included.
