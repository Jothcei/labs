import unittest

from lab2.main import binary, find_binary

class BinaryTests(unittest.TestCase):

    def test_accepts_binary_digits(self):
        self.assertTrue(binary("101"))

    def test_rejects_digit_two(self):
        self.assertFalse(binary("102"))

    def test_finds_standalone_numbers(self):
        result = find_binary("102, (10), x101, 001")
        self.assertEqual(result, ["10", "001"])