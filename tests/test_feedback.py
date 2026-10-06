"""Tests for analyzer/feedback.py."""
import unittest

from analyzer.feedback import (
    build_feedback,
    explain_weaknesses,
    missing_character_types,
    suggest_improvements,
)

MANAGER_TIP = "Use a unique password for every account and store them in a password manager"


class TestFeedback(unittest.TestCase):
    def test_missing_types(self):
        self.assertEqual(missing_character_types("abc"), ["uppercase letters", "numbers", "symbols"])
        self.assertEqual(missing_character_types("aB1!"), [])

    def test_empty_password(self):
        self.assertEqual(explain_weaknesses(""), ["Password is empty"])

    def test_short_password_is_flagged(self):
        self.assertTrue(explain_weaknesses("abc")[0].startswith("Too short"))

    def test_strong_password_has_no_weaknesses(self):
        self.assertEqual(explain_weaknesses("k9#Vq2!xLm8@Zt4w"), [])

    def test_suggestions_always_end_with_manager_tip(self):
        for pw in ["", "password", "k9#Vq2!xLm8@Zt4w"]:
            self.assertEqual(suggest_improvements(pw)[-1], MANAGER_TIP)

    def test_short_password_gets_length_advice(self):
        self.assertTrue(any("at least 12" in tip for tip in suggest_improvements("abc")))

    def test_build_feedback_keys(self):
        self.assertEqual(set(build_feedback("abc")), {"weaknesses", "suggestions"})
