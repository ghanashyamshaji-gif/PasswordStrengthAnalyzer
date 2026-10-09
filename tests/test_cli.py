"""Tests for analyzer/report.py and the formatting in main.py."""
import unittest

from analyzer.report import analyze_password
from main import format_report, score_bar


class TestReport(unittest.TestCase):
    def test_report_has_all_sections(self):
        report = analyze_password("Hello123!")
        expected = {"score", "rating", "entropy", "patterns", "crack_difficulty",
                    "crack_times", "weaknesses", "suggestions"}
        self.assertEqual(set(report), expected)

    def test_strong_password_report(self):
        self.assertEqual(analyze_password("k9#Vq2!xLm8@Zt4w")["rating"], "Very Strong")


class TestFormatting(unittest.TestCase):
    def test_score_bar(self):
        self.assertEqual(score_bar(0), "[" + "-" * 20 + "]")
        self.assertEqual(score_bar(50), "[" + "#" * 10 + "-" * 10 + "]")
        self.assertEqual(score_bar(100), "[" + "#" * 20 + "]")

    def test_report_text(self):
        text = format_report(analyze_password("password"))
        self.assertIn("PASSWORD STRENGTH REPORT", text)
        self.assertIn("Weak", text)
        self.assertIn("Common password", text)


class TestBreachFormatting(unittest.TestCase):
    def test_breach_section_only_appears_when_checked(self):
        report = analyze_password("password")
        self.assertNotIn("Data breach check", format_report(report))
        report["breach_count"] = 0
        text = format_report(report)
        self.assertIn("Data breach check", text)
        self.assertIn("Not found in known breaches", text)

    def test_breach_count_is_shown(self):
        report = analyze_password("password")
        report["breach_count"] = 1234
        self.assertIn("Found 1,234 times", format_report(report))
