import unittest
from dataclasses import FrozenInstanceError

from strings_oo import PhoneNumber, StringComparison


class StringComparisonTests(unittest.TestCase):
    def test_content_and_length_are_independent(self):
        for first, second, content, length in [
            ("abc", "abc", True, True),
            ("abc", "xyz", False, True),
            ("abc", "abcd", False, False),
            ("", "", True, True),
        ]:
            with self.subTest(first=first, second=second):
                comparison = StringComparison(first, second)
                self.assertEqual(comparison.same_content, content)
                self.assertEqual(comparison.same_length, length)

    def test_pair_cannot_be_reassigned(self):
        comparison = StringComparison("a", "b")
        with self.assertRaises(FrozenInstanceError):
            comparison.first = "other"


class PhoneNumberTests(unittest.TestCase):
    def test_supported_inputs(self):
        for source, expected in [
            ("461-0133", "34610133"), ("4610133", "34610133"),
            ("9461-0133", "94610133"), ("94610133", "94610133"),
            ("0123456", "30123456"),
        ]:
            with self.subTest(source=source):
                phone = PhoneNumber(source)
                self.assertEqual(phone.corrected, expected)
                self.assertEqual(phone.formatted, expected[:4] + "-" + expected[4:])

    def test_existing_eight_digits_do_not_announce_correction(self):
        self.assertNotIn("Vou acrescentar", PhoneNumber("94610133").report())

    def test_invalid_input_is_rejected(self):
        for source in ["123", "abcdefg", "1234567x", ""]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                PhoneNumber(source)


if __name__ == "__main__":
    unittest.main()
