"""Score password strength: entropy, 0-100 score, and rating."""
import math
import string

from analyzer.patterns import find_patterns, is_common_password


def character_pool_size(password):
    """Size of the character set the password appears to draw from."""
    pool = 0
    if any(c in string.ascii_lowercase for c in password):
        pool += 26
    if any(c in string.ascii_uppercase for c in password):
        pool += 26
    if any(c in string.digits for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += len(string.punctuation)
    if " " in password:
        pool += 1
    known = string.ascii_letters + string.digits + string.punctuation + " "
    if any(c not in known for c in password):
        pool += 32  # unicode or other unusual characters
    return pool


def calculate_entropy(password):
    """Estimated entropy in bits: length * log2(pool size)."""
    if not password:
        return 0.0
    return round(len(password) * math.log2(character_pool_size(password)), 2)


def count_character_types(password):
    """How many of lowercase, uppercase, digit, symbol the password uses (0-4)."""
    checks = [
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(not c.isalnum() for c in password),
    ]
    return sum(checks)


def calculate_score(password):
    """Strength score from 0 (terrible) to 100 (excellent)."""
    if not password:
        return 0
    entropy_points = min(calculate_entropy(password) / 100, 1) * 60
    length_points = min(len(password) / 16, 1) * 20
    variety_points = count_character_types(password) / 4 * 20
    score = entropy_points + length_points + variety_points
    score -= 10 * len(find_patterns(password))
    if is_common_password(password):
        score = min(score, 10)
    return max(0, min(100, round(score)))


def get_rating(score):
    """Convert a numeric score into Weak / Medium / Strong / Very Strong."""
    if score < 30:
        return "Weak"
    if score < 60:
        return "Medium"
    if score < 80:
        return "Strong"
    return "Very Strong"
