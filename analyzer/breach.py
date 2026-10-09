"""Check whether a password appears in known data breaches (Have I Been Pwned)."""
import hashlib
import urllib.request

API_URL = "https://api.pwnedpasswords.com/range/"


def split_hash(password):
    """SHA-1 hash the password; return (first 5 hex chars, remaining 35 hex chars)."""
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return digest[:5], digest[5:]


def parse_range_response(text, suffix):
    """Find our hash suffix in the API response; return how many breaches contain it."""
    for line in text.splitlines():
        candidate, _, count = line.partition(":")
        if candidate.strip().upper() == suffix:
            try:
                return int(count.strip())
            except ValueError:
                return 0
    return 0


def fetch_range(prefix, timeout=5):
    """Download all breached-hash suffixes that share this 5-character prefix."""
    request = urllib.request.Request(
        API_URL + prefix,
        headers={"User-Agent": "PasswordStrengthAnalyzer-learning-project"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8")
