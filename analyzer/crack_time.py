"""Estimate how long it would take an attacker to crack a password."""
from analyzer.patterns import is_common_password
from analyzer.strength import calculate_entropy

# (label, guesses per second) - rough order-of-magnitude figures
SCENARIOS = [
    ("Online attack (rate-limited login)", 100),
    ("Offline attack (slow hash, e.g. bcrypt)", 10_000),
    ("Offline attack (fast hash, e.g. MD5 on GPUs)", 100_000_000_000),
]

MINUTE = 60
HOUR = 3600
DAY = 86400
YEAR = 31_557_600


def format_duration(seconds):
    """Turn a number of seconds into a readable string like '3 days'."""
    if seconds < 1:
        return "instantly"
    if seconds < MINUTE:
        return f"{seconds:.0f} seconds"
    if seconds < HOUR:
        return f"{seconds / MINUTE:.0f} minutes"
    if seconds < DAY:
        return f"{seconds / HOUR:.0f} hours"
    if seconds < YEAR:
        return f"{seconds / DAY:.0f} days"
    years = seconds / YEAR
    if years < 1_000:
        return f"{years:,.0f} years"
    if years < 1_000_000:
        return f"{years / 1_000:,.0f} thousand years"
    if years < 1_000_000_000:
        return f"{years / 1_000_000:,.0f} million years"
    if years < 1_000_000_000_000:
        return f"{years / 1_000_000_000:,.0f} billion years"
    return "over a trillion years"


def seconds_to_crack(entropy_bits, guesses_per_second):
    """Average seconds to crack: half the search space divided by guess rate."""
    entropy_bits = min(entropy_bits, 400)  # avoid float overflow on huge inputs
    return (2 ** (entropy_bits - 1)) / guesses_per_second


def estimate_crack_time(password):
    """Return {scenario: readable time} for an average-case attack."""
    if not password or is_common_password(password):
        return {label: "instantly" for label, _ in SCENARIOS}
    entropy = calculate_entropy(password)
    return {
        label: format_duration(seconds_to_crack(entropy, rate))
        for label, rate in SCENARIOS
    }


def get_difficulty(password):
    """One-word crack difficulty, judged against the fastest attack scenario."""
    if not password or is_common_password(password):
        return "Instant"
    entropy = calculate_entropy(password)
    seconds = seconds_to_crack(entropy, SCENARIOS[-1][1])
    if seconds < DAY:
        return "Very Easy"
    if seconds < YEAR:
        return "Easy"
    if seconds < 1_000 * YEAR:
        return "Hard"
    return "Very Hard"
