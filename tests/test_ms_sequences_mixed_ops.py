import unittest
from decimal import Decimal
from core.operations import percent_expr, sqrt_expr, clear_entry_expr
from core.engine import decimal_to_str
from ui.utils import build_unary_overlay, format_history_ops

class TestMsSequencesMixedOps(unittest.TestCase):

    def test_ce_then_change_operator_and_percent(self):
        expr = '200+10'
        expr1, err1 = percent_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '200+20')
        ce = clear_entry_expr(expr1)
        self.assertEqual(ce, '200+')
        expr_changed = '200-'
        expr2 = expr_changed + '5'
        expr3, err3 = percent_expr(expr2)
        self.assertFalse(err3)
        expected_right = decimal_to_str(Decimal('200') * (Decimal('5') / Decimal('100')))
        self.assertEqual(expr3, '200-' + expected_right)

    def test_percent_right_starts_with_comma_and_negative_comma(self):
        left = '100'
        expr1 = left + '+' + ',5'
        res1, err1 = percent_expr(expr1)
        self.assertFalse(err1)
        expected1 = decimal_to_str(Decimal(left) * (Decimal('0.5') / Decimal('100')))
        self.assertEqual(res1, left + '+' + expected1)
        expr2 = left + '+' + '-,5'
        res2, err2 = percent_expr(expr2)
        self.assertFalse(err2)
        expected2 = decimal_to_str(Decimal(left) * (Decimal('-0.5') / Decimal('100')))
        self.assertEqual(res2, left + '+' + expected2)

    def test_sqrt_on_decimal_right_after_ce_and_operator_change(self):
        expr = '100+0,25'
        ce = clear_entry_expr(expr)
        self.assertEqual(ce, '100+')
        expr_changed = '100-0,25'
        res, err = sqrt_expr(expr_changed)
        self.assertFalse(err)
        expected_right = decimal_to_str(Decimal('0.5'))
        self.assertEqual(res, '100-' + expected_right)

    def test_overlay_zero_minus_decimal_comma(self):
        ov = build_unary_overlay('0-,5', 'sqrt')
        self.assertEqual(ov, '0-√(0,5)')
        self.assertEqual(format_history_ops(ov), '0 - √(0,5)')

    def test_divide_percent_reduces_right(self):
        expr = '10/0,25'
        res, err = percent_expr(expr)
        self.assertFalse(err)
        expected_right = decimal_to_str(Decimal('0.25') / Decimal('100'))
        self.assertEqual(res, '10/' + expected_right)

if __name__ == '__main__':
    unittest.main()