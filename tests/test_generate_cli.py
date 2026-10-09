"""Tests for the --generate command-line option."""
import os
import subprocess
import sys
import unittest

MAIN = os.path.join(os.path.dirname(__file__), "..", "main.py")


def run_main(*args):
    return subprocess.run([sys.executable, MAIN, *args], capture_output=True, text=True)


class TestGenerateOption(unittest.TestCase):
    def test_generate_prints_password_and_report(self):
        result = run_main("--generate", "20")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Generated password:", result.stdout)
        self.assertIn("PASSWORD STRENGTH REPORT", result.stdout)

    def test_too_short_length_is_refused(self):
        result = run_main("--generate", "5")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("at least 8", result.stderr)
