"""Tests for the optional breach check inside analyze_password."""
import unittest
from unittest.mock import patch

from analyzer.report import analyze_password

STRONG = "k9#Vq2!xLm8@Zt4w"


class TestBreachInReport(unittest.TestCase):
    def test_breach_check_is_off_by_default(self):
        with patch("analyzer.report.check_breach") as fake:
            report = analyze_password(STRONG)
        fake.assert_not_called()
        self.assertNotIn("breach_count", report)

    def test_breached_password_is_capped_and_explained(self):
        with patch("analyzer.report.check_breach", return_value=5):
            report = analyze_password(STRONG, breach_check=True)
        self.assertEqual(report["breach_count"], 5)
        self.assertLessEqual(report["score"], 10)
        self.assertEqual(report["rating"], "Weak")
        self.assertTrue(any("data breaches" in item for item in report["weaknesses"]))
        self.assertIn("publicly known", report["suggestions"][0])

    def test_clean_password_is_unchanged(self):
        with patch("analyzer.report.check_breach", return_value=0):
            report = analyze_password(STRONG, breach_check=True)
        self.assertEqual(report["rating"], "Very Strong")

    def test_failed_lookup_does_not_change_score(self):
        with patch("analyzer.report.check_breach", return_value=None):
            report = analyze_password(STRONG, breach_check=True)
        self.assertIsNone(report["breach_count"])
        self.assertEqual(report["rating"], "Very Strong")
