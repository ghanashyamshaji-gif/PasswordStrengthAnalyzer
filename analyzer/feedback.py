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


def pattern_suggestions(password):
    """Advice that targets the specific weak patterns found."""
    tips = []
    if is_common_password(password):
        tips.append("Avoid common passwords and simple swaps like @ for a or 0 for o")
    if has_repeated_chars(password):
        tips.append("Don't repeat the same character several times in a row")
    if has_sequence(password):
        tips.append("Avoid sequences like abc or 123")
    if has_keyboard_pattern(password):
        tips.append("Avoid keyboard runs like qwer or asdf")
    if has_year(password):
        tips.append("Don't use years or dates; they are easy to guess")
    return tips


def suggest_improvements(password):
    """List concrete steps that would make this password stronger."""
    tips = []
    if len(password) < MIN_LENGTH:
        tips.append(f"Use at least {MIN_LENGTH} characters (16 or more is even better)")
    missing = missing_character_types(password)
    if missing:
        tips.append("Mix in " + ", ".join(missing))
    tips.extend(pattern_suggestions(password))
    if len(password) < 16:
        tips.append("Try a passphrase of 4+ random words, e.g. correct-horse-battery-staple")
    tips.append("Use a unique password for every account and store them in a password manager")
    return tips


def build_feedback(password):
    """Return both the weaknesses and the improvement tips."""
    return {
        "weaknesses": explain_weaknesses(password),
        "suggestions": suggest_improvements(password),
    }
