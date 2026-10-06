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


class TestRepeatsAndSequences(unittest.TestCase):
    def test_repeated_characters_found(self):
        self.assertTrue(has_repeated_chars("hellooo"))

    def test_two_in_a_row_is_allowed(self):
        self.assertFalse(has_repeated_chars("hello"))

    def test_ascending_sequence(self):
        self.assertTrue(has_sequence("xxabcxx"))

    def test_descending_sequence(self):
        self.assertTrue(has_sequence("cba"))

    def test_number_sequence(self):
        self.assertTrue(has_sequence("a789b"))

    def test_non_sequence(self):
        self.assertFalse(has_sequence("ace"))


class TestKeyboardAndYear(unittest.TestCase):
    def test_keyboard_run(self):
        self.assertTrue(has_keyboard_pattern("xqwerx"))

    def test_reversed_keyboard_run(self):
        self.assertTrue(has_keyboard_pattern("poiu"))

    def test_not_a_keyboard_run(self):
        self.assertFalse(has_keyboard_pattern("q1w2"))

    def test_year_found(self):
        self.assertTrue(has_year("pass1999"))

    def test_no_year(self):
        self.assertFalse(has_year("abc12"))


class TestFindPatterns(unittest.TestCase):
    def test_strong_password_has_no_patterns(self):
        self.assertEqual(find_patterns("k9#Vq2!xLm8@Zt4w"), [])

    def test_multiple_patterns_reported(self):
        found = find_patterns("Qwerty2024!")
        self.assertEqual(len(found), 2)
        self.assertTrue(any("Keyboard" in item for item in found))
        self.assertTrue(any("year" in item for item in found))

    def test_common_password_reported(self):
        self.assertTrue(any("Common" in item for item in find_patterns("password")))
