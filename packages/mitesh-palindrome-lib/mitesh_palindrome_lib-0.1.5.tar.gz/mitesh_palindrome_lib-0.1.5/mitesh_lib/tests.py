import unittest

from validate_palindrome import ValidatePalndrome

class TestPlaindrome(unittest.TestCase):
    def test_correct_palindrome(self):
        self.assertEqual(ValidatePalndrome().validate("radar"), True)
    
    def test_incorrect_palindrome(self):
        self.assertEqual(ValidatePalndrome().validate("test"),False)


if __name__ == "__main__":
    unittest.main()