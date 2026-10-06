"""Explain why a password is weak and how to improve it."""
from analyzer.patterns import (
    find_patterns,
    has_keyboard_pattern,
    has_repeated_chars,
    has_sequence,
    has_year,
    is_common_password,
)

MIN_LENGTH = 12


def missing_character_types(password):
    """Names of the character types the password does not use."""
    missing = []
    if not any(c.islower() for c in password):
        missing.append("lowercase letters")
    if not any(c.isupper() for c in password):
        missing.append("uppercase letters")
    if not any(c.isdigit() for c in password):
        missing.append("numbers")
    if all(c.isalnum() for c in password):
        missing.append("symbols")
    return missing
