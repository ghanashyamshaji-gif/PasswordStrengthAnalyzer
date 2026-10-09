"""Tests for analyzer/display.py."""
import unittest

from analyzer.display import DEFAULT_COLOR, RATING_COLORS, bar_fraction, color_for_rating, headline


class TestDisplay(unittest.TestCase):
    def test_every_rating_has_its_own_color(self):
        self.assertEqual(set(RATING_COLORS), {"Weak", "Medium", "Strong", "Very Strong"})
        self.assertEqual(len(set(RATING_COLORS.values())), 4)

    def test_unknown_rating_gets_default_color(self):
        self.assertEqual(color_for_rating(None), DEFAULT_COLOR)
        self.assertEqual(color_for_rating("Nonsense"), DEFAULT_COLOR)

    def test_headline_text(self):
        self.assertEqual(headline({"rating": "Medium", "score": 57}), "Medium - 57/100")

    def test_bar_fraction_is_clamped(self):
        self.assertEqual(bar_fraction(0), 0.0)
        self.assertEqual(bar_fraction(50), 0.5)
        self.assertEqual(bar_fraction(100), 1.0)
        self.assertEqual(bar_fraction(250), 1.0)
        self.assertEqual(bar_fraction(-5), 0.0)
