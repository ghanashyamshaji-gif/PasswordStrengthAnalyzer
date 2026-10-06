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


class TestCrackEstimates(unittest.TestCase):
    def test_seconds_to_crack_math(self):
        self.assertEqual(seconds_to_crack(11, 1), 1024)
        self.assertEqual(seconds_to_crack(11, 2), 512)

    def test_huge_entropy_does_not_overflow(self):
        self.assertGreater(seconds_to_crack(100000, 1), 0)

    def test_common_password_cracks_instantly(self):
        times = estimate_crack_time("password")
        self.assertEqual(len(times), len(SCENARIOS))
        self.assertTrue(all(value == "instantly" for value in times.values()))

    def test_difficulty_labels(self):
        self.assertEqual(get_difficulty("password"), "Instant")
        self.assertEqual(get_difficulty("Hello123!"), "Very Easy")
        self.assertEqual(get_difficulty("k9#Vq2!xLm8@Zt4w"), "Very Hard")

    def test_patterns_reduce_effective_entropy(self):
        self.assertLess(effective_entropy("Hello123!"), calculate_entropy("Hello123!"))
        self.assertEqual(effective_entropy("k9#Vq2!xLm8@Zt4w"), calculate_entropy("k9#Vq2!xLm8@Zt4w"))
