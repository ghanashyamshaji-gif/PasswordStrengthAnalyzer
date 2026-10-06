"""Tests for analyzer/crack_time.py."""
import unittest

from analyzer.crack_time import (
    SCENARIOS,
    YEAR,
    effective_entropy,
    estimate_crack_time,
    format_duration,
    get_difficulty,
    seconds_to_crack,
)
from analyzer.strength import calculate_entropy


class TestFormatDuration(unittest.TestCase):
    def test_units(self):
        self.assertEqual(format_duration(0.5), "instantly")
        self.assertEqual(format_duration(30), "30 seconds")
        self.assertEqual(format_duration(120), "2 minutes")
        self.assertEqual(format_duration(7200), "2 hours")
        self.assertEqual(format_duration(172800), "2 days")
        self.assertEqual(format_duration(5 * YEAR), "5 years")
        self.assertEqual(format_duration(5000 * YEAR), "5 thousand years")

    def test_huge_values(self):
        self.assertEqual(format_duration(1e13 * YEAR), "over a trillion years")
