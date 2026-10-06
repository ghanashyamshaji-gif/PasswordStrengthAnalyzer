"""Tests for analyzer/strength.py."""
import math
import unittest

from analyzer.strength import (
    analyze_strength,
    calculate_entropy,
    calculate_score,
    character_pool_size,
    count_character_types,
    get_rating,
)


class TestPoolAndEntropy(unittest.TestCase):
    def test_pool_sizes(self):
        self.assertEqual(character_pool_size(""), 0)
        self.assertEqual(character_pool_size("abc"), 26)
        self.assertEqual(character_pool_size("aA"), 52)
        self.assertEqual(character_pool_size("aA1"), 62)
        self.assertEqual(character_pool_size("aA1!"), 94)

    def test_entropy_of_empty_password_is_zero(self):
        self.assertEqual(calculate_entropy(""), 0.0)

    def test_entropy_formula(self):
        self.assertEqual(calculate_entropy("abcd"), round(4 * math.log2(26), 2))

    def test_longer_means_more_entropy(self):
        self.assertGreater(calculate_entropy("abcdefgh"), calculate_entropy("abcd"))

    def test_character_type_count(self):
        self.assertEqual(count_character_types("abc"), 1)
        self.assertEqual(count_character_types("aB"), 2)
        self.assertEqual(count_character_types("aB1"), 3)
        self.assertEqual(count_character_types("aB1!"), 4)
