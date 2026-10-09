"""Tests for analyzer/generator.py."""
import unittest

from analyzer.generator import CHARACTER_SETS, generate_clean_password, generate_password
from analyzer.patterns import find_patterns


class TestGenerator(unittest.TestCase):
    def test_length_is_respected(self):
        for length in (4, 8, 16, 64):
            self.assertEqual(len(generate_password(length)), length)

    def test_every_character_type_is_present(self):
        for _ in range(50):
            password = generate_password(8)
            for group in CHARACTER_SETS:
                self.assertTrue(any(c in group for c in password))

    def test_too_short_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_password(3)

    def test_passwords_differ_between_calls(self):
        self.assertEqual(len({generate_password(16) for _ in range(20)}), 20)

    def test_clean_password_has_no_weak_patterns(self):
        for _ in range(20):
            self.assertEqual(find_patterns(generate_clean_password(16)), [])
