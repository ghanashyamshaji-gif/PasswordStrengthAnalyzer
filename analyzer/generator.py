"""Generate random passwords with Python's cryptographically secure secrets module."""
import secrets
import string

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"
CHARACTER_SETS = [string.ascii_lowercase, string.ascii_uppercase, string.digits, SYMBOLS]


def generate_password(length=16):
    """Random password of the given length with at least one of each character type."""
    if length < len(CHARACTER_SETS):
        raise ValueError(f"length must be at least {len(CHARACTER_SETS)}")
    everything = "".join(CHARACTER_SETS)
    chars = [secrets.choice(group) for group in CHARACTER_SETS]
    chars += [secrets.choice(everything) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)
