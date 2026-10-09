"""Tests for analyzer/breach.py (no real network calls are made)."""
import unittest

from analyzer.breach import check_breach, describe_breach, parse_range_response, split_hash

PASSWORD_SUFFIX = "1E4C9B93F3F0682250B6CF8331B7EE68FD8"
SAMPLE = (
    "0018A45C4D1DEF81644B54AB7F969B88D65:1\r\n"
    f"{PASSWORD_SUFFIX}:12345\r\n"
    "00D4F6E8FA6EECAD2A3AA415EEC418D38EC:0\r\n"
)


class TestHashingAndParsing(unittest.TestCase):
    def test_split_hash_known_value(self):
        self.assertEqual(split_hash("password"), ("5BAA6", PASSWORD_SUFFIX))

    def test_prefix_and_suffix_lengths(self):
        prefix, suffix = split_hash("anything")
        self.assertEqual(len(prefix), 5)
        self.assertEqual(len(suffix), 35)

    def test_finds_matching_suffix(self):
        self.assertEqual(parse_range_response(SAMPLE, PASSWORD_SUFFIX), 12345)

    def test_missing_suffix_returns_zero(self):
        self.assertEqual(parse_range_response(SAMPLE, "F" * 35), 0)

    def test_zero_count_entries_mean_not_found(self):
        self.assertEqual(parse_range_response(SAMPLE, "00D4F6E8FA6EECAD2A3AA415EEC418D38EC"), 0)

    def test_garbage_count_is_treated_as_zero(self):
        self.assertEqual(parse_range_response("ABC:xyz", "ABC"), 0)


class TestCheckBreach(unittest.TestCase):
    def test_returns_count_and_sends_only_the_prefix(self):
        def fake_fetcher(prefix):
            self.assertEqual(prefix, "5BAA6")
            return SAMPLE

        self.assertEqual(check_breach("password", fetcher=fake_fetcher), 12345)

    def test_password_not_in_response_returns_zero(self):
        self.assertEqual(check_breach("k9#Vq2!xLm8@Zt4w", fetcher=lambda prefix: SAMPLE), 0)

    def test_network_error_returns_none(self):
        def broken(prefix):
            raise OSError("offline")

        self.assertIsNone(check_breach("password", fetcher=broken))

    def test_empty_password_skips_lookup(self):
        def should_not_run(prefix):
            raise AssertionError("lookup should not happen")

        self.assertEqual(check_breach("", fetcher=should_not_run), 0)

    def test_describe_breach(self):
        self.assertIn("Not checked", describe_breach(None))
        self.assertEqual(describe_breach(0), "Not found in known breaches")
        self.assertEqual(describe_breach(1234), "Found 1,234 times in known data breaches")
