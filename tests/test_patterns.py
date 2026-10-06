"""Tests for analyzer/patterns.py."""
import unittest

from analyzer.patterns import (
    find_patterns,
    has_keyboard_pattern,
    has_repeated_chars,
    has_sequence,
    has_year,
    is_common_password,
)


class TestCommonPasswords(unittest.TestCase):
    def test_plain_common_password(self):
        self.assertTrue(is_common_password("password"))

    def test_case_is_ignored(self):
        self.assertTrue(is_common_password("PASSWORD"))

    def test_leetspeak_is_decoded(self):
        self.assertTrue(is_common_password("P@ssw0rd"))

    def test_random_password_is_not_common(self):
        self.assertFalse(is_common_password("k9#Vq2!xLm8@Zt4w"))
