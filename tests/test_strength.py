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


class TestScoreAndRating(unittest.TestCase):
    def test_empty_password_scores_zero(self):
        self.assertEqual(calculate_score(""), 0)

    def test_common_password_is_capped_low(self):
        self.assertLessEqual(calculate_score("password"), 10)

    def test_random_password_scores_high(self):
        self.assertGreaterEqual(calculate_score("k9#Vq2!xLm8@Zt4w"), 80)

    def test_score_stays_between_0_and_100(self):
        for pw in ["", "a", "password", "Hello123!", "x" * 200, "k9#Vq2!xLm8@Zt4w"]:
            self.assertTrue(0 <= calculate_score(pw) <= 100)

    def test_rating_boundaries(self):
        self.assertEqual(get_rating(0), "Weak")
        self.assertEqual(get_rating(29), "Weak")
        self.assertEqual(get_rating(30), "Medium")
        self.assertEqual(get_rating(59), "Medium")
        self.assertEqual(get_rating(60), "Strong")
        self.assertEqual(get_rating(79), "Strong")
        self.assertEqual(get_rating(80), "Very Strong")
        self.assertEqual(get_rating(100), "Very Strong")

    def test_analyze_strength_keys(self):
        result = analyze_strength("Hello123!")
        self.assertEqual(set(result), {"score", "rating", "entropy", "patterns"})
        self.assertEqual(result["rating"], "Medium")
