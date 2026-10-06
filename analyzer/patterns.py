"""Detect common weak patterns in passwords."""
import re

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "12345678", "12345", "qwerty",
    "abc123", "letmein", "welcome", "admin", "iloveyou", "monkey",
    "dragon", "football", "baseball", "sunshine", "princess", "login",
    "master", "hello", "freedom", "whatever", "trustno1", "passw0rd",
    "password1", "qwerty123", "1q2w3e4r", "000000", "111111", "123123", "zaq12wsx", "pass123", "1qaz2wsx", "starwars",
}

# Maps "leetspeak" substitutions back to letters (p@ssw0rd -> password)
LEET_MAP = str.maketrans({
    "@": "a", "4": "a", "3": "e", "1": "i", "!": "i",
    "0": "o", "$": "s", "5": "s", "7": "t",
})


def is_common_password(password):
    """True if the password (or its leetspeak-decoded form) is a known weak password."""
    lowered = password.lower()
    if lowered in COMMON_PASSWORDS:
        return True
    return lowered.translate(LEET_MAP) in COMMON_PASSWORDS


def has_repeated_chars(password, run=3):
    """True if any character repeats `run` or more times in a row."""
    return re.search(r"(.)\1{%d,}" % (run - 1), password) is not None


SEQUENCES = ["abcdefghijklmnopqrstuvwxyz", "0123456789"]


def has_sequence(password, length=3):
    """True if the password contains an ascending or descending run like abc or 321."""
    lowered = password.lower()
    for seq in SEQUENCES:
        for candidate in (seq, seq[::-1]):
            for i in range(len(candidate) - length + 1):
                if candidate[i:i + length] in lowered:
                    return True
    return False


KEYBOARD_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]


def has_keyboard_pattern(password, length=4):
    """True if the password contains 4+ neighbouring keys in a row."""
    lowered = password.lower()
    for row in KEYBOARD_ROWS:
        for candidate in (row, row[::-1]):
            for i in range(len(candidate) - length + 1):
                if candidate[i:i + length] in lowered:
                    return True
    return False
