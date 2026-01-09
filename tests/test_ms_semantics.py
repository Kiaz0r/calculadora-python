import unittest
from decimal import Decimal
from core.operations import sqrt_expr, square_expr, reciprocal_expr, percent_expr
from core.engine import decimal_to_str
from ui.utils import build_unary_overlay, format_history_ops

class TestMicrosoftSemantics(unittest.TestCase):

    def test_sqrt_on_right_operand_after_initial_minus(self):
        res, err = sqrt_expr('0-9')
        self.assertFalse(err)
        self.assertEqual(res, '0-3')

    def test_sqrt_on_positive_standalone(self):
        res, err = sqrt_expr('9')
        self.assertFalse(err)
        self.assertEqual(res, '3')

    def test_sqrt_on_negative_standalone(self):
        res, err = sqrt_expr('-9')
        self.assertTrue(err)
        self.assertEqual(res, '-9')

    def test_overlay_format_for_sqrt_with_prefix(self):
        expr = '0-9'
        overlay = build_unary_overlay(expr, 'sqrt')
        self.assertEqual(overlay, '0-√(9)')
        hist = format_history_ops(overlay)
        self.assertEqual(hist, '0 - √(9)')

    def test_square_on_right_operand_after_initial_minus(self):
        res, err = square_expr('0-9')
        self.assertFalse(err)
        self.assertEqual(res, '0-81')

    def test_reciprocal_on_right_operand_after_initial_minus(self):
        res, err = reciprocal_expr('0-9')
        self.assertFalse(err)
        expected_right = decimal_to_str(Decimal('1') / Decimal('9'))
        self.assertEqual(res, '0-' + expected_right)

    def test_percent_on_zero_minus(self):
        res, err = percent_expr('0-9')
        self.assertFalse(err)
        self.assertEqual(res, '0-0')

if __name__ == '__main__':
    unittest.main()