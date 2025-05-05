from django.test import SimpleTestCase
from . import calc


class CalcTests(SimpleTestCase):
    def test_add(self):
        """Test the add function"""
        res = calc.add(5, 6)
        self.assertEqual(res, 11, "Should be 11")
        res = calc.add(0, 0)
        self.assertEqual(res, 0, "Should be 0")
        res = calc.add(-1, 1)
        self.assertEqual(res, 0, "Should be 0")
