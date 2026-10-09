"""Check whether a password appears in known data breaches (Have I Been Pwned)."""
import hashlib
import urllib.request

API_URL = "https://api.pwnedpasswords.com/range/"


def split_hash(password):
    """SHA-1 hash the password; return (first 5 hex chars, remaining 35 hex chars)."""
    digest = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return digest[:5], digest[5:]
