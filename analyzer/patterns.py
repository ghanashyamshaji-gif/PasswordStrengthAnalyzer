"""Detect common weak patterns in passwords."""
import os
import re

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "12345678", "12345", "qwerty",
    "abc123", "letmein", "welcome", "admin", "iloveyou", "monkey",
    "dragon", "football", "baseball", "sunshine", "princess", "login",
    "master", "hello", "freedom", "whatever", "trustno1", "passw0rd",
    "password1", "qwerty123", "1q2w3e4r", "000000", "111111", "123123", "zaq12wsx", "pass123", "1qaz2wsx", "starwars",
}


def load_wordlist(path):
    """Read one password per line from a text file (empty set if the file is missing)."""
    try:
        with open(path, encoding="utf-8") as handle:
            return {line.strip().lower() for line in handle if line.strip()}
    except OSError:
        return set()


WORDLIST_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "common_passwords.txt")
COMMON_PASSWORDS |= load_wordlist(WORDLIST_PATH)

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


def has_year(password):
    """True if the password contains a year from 1900 to 2099."""
    return re.search(r"(19|20)\d{2}", password) is not None


def find_patterns(password):
    """Return a list of human-readable descriptions of every weak pattern found."""
    found = []
    if is_common_password(password):
        found.append("Common password (appears in known password lists)")
    if has_repeated_chars(password):
        found.append("Repeated characters (e.g. aaa, 111)")
    if has_sequence(password):
        found.append("Sequential characters (e.g. abc, 123, cba)")
    if has_keyboard_pattern(password):
        found.append("Keyboard pattern (e.g. qwer, asdf)")
    if has_year(password):
        found.append("Contains a year (e.g. 1998, 2024)")
    return found
