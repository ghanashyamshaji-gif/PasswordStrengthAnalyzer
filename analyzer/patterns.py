"""Detect common weak patterns in passwords."""
import re

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "12345678", "12345", "qwerty",
    "abc123", "letmein", "welcome", "admin", "iloveyou", "monkey",
    "dragon", "football", "baseball", "sunshine", "princess", "login",
    "master", "hello", "freedom", "whatever", "trustno1", "passw0rd",
    "password1", "qwerty123", "1q2w3e4r", "000000", "111111", "123123",
}

# Maps "leetspeak" substitutions back to letters (p@ssw0rd -> password)
LEET_MAP = str.maketrans({
    "@": "a", "4": "a", "3": "e", "1": "i", "!": "i",
    "0": "o", "$": "s", "5": "s", "7": "t",
})
