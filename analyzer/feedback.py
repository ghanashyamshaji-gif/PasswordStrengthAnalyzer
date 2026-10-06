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


def explain_weaknesses(password):
    """List the reasons this password is weak (empty list if none found)."""
    if not password:
        return ["Password is empty"]
    reasons = []
    if len(password) < 8:
        reasons.append(f"Too short ({len(password)} characters): short passwords are guessed fast")
    elif len(password) < MIN_LENGTH:
        reasons.append(f"Shorter than {MIN_LENGTH} characters")
    for kind in missing_character_types(password):
        reasons.append(f"No {kind}")
    reasons.extend(find_patterns(password))
    return reasons
