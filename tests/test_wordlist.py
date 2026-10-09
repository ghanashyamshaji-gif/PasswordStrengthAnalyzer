"""Tests for loading the external password wordlist."""
import os
import tempfile
import unittest

from analyzer.patterns import COMMON_PASSWORDS, WORDLIST_PATH, is_common_password, load_wordlist


class TestWordlist(unittest.TestCase):
    def test_missing_file_returns_empty_set(self):
        self.assertEqual(load_wordlist("no/such/file.txt"), set())

    def test_words_are_lowercased_and_blank_lines_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "words.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("Hunter2\n\n  LetMeIn99  \n")
            self.assertEqual(load_wordlist(path), {"hunter2", "letmein99"})

    def test_bundled_wordlist_is_loaded(self):
        self.assertTrue(os.path.exists(WORDLIST_PATH))
        self.assertIn("superman", COMMON_PASSWORDS)
        self.assertTrue(is_common_password("Superman"))
