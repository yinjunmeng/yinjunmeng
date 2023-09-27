import unittest
from fractions import Fraction
from unittest.mock import patch
from io import StringIO
import sys

from homework import operation_yunsuan, factor_yunsuan, product, start_yunsuan, generate_expression, reset_result, \
    repeat_yunsuan


class TestHomework(unittest.TestCase):

    def test_operation_yunsuan(self):
        result = operation_yunsuan(4, 2, '+')
        self.assertEqual(result, 6)
        result = operation_yunsuan(4, 2, '-')
        self.assertEqual(result, 2)
        result = operation_yunsuan(4, 2, '*')
        self.assertEqual(result, 8)
        result = operation_yunsuan(4, 2, '/')
        self.assertEqual(result, 2)

    def test_factor_yunsuan(self):
        result = factor_yunsuan()
        self.assertIsInstance(result, Fraction)

    def test_product(self):
        result, two_index = product()
        self.assertIsInstance(result, Fraction)

    def test_start_yunsuan(self):
        global result_list
        result = start_yunsuan()
        self.assertIsInstance(result, Fraction)

    def test_generate_expression(self):
        expression = generate_expression([2, 3, 5, 'nohav', 'none', '+', '-'])
        self.assertEqual(expression, '2+3-5')

    def test_repeat_yunsuan(self):
        global result_list
        there = [[1, 2, 3, 'nohav', 'none', '+', '-'],
                 [2, 3, 4, 'nohav', 'none', '+', '-'],
                 [1, 2, 3, 'nohav', 'none', '+', '-']]
        result_list = [Fraction(3, 2), Fraction(5, 2), Fraction(3, 2)]
        type_list = [3, 3, 3]
        check = [0, 0, 0]
        n = 3
        m = repeat_yunsuan(n)
        self.assertEqual(m, 3)


if __name__ == '__main__':
    result_list = []  # Initialize result_list globally
    unittest.main()
