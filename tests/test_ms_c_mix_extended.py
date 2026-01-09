import unittest
from decimal import Decimal
from core.operations import sqrt_expr, square_expr, reciprocal_expr, percent_expr, clear_entry_expr
from core.engine import decimal_to_str
from ui.utils import build_unary_overlay, format_history_ops

class TestMsCMixExtended(unittest.TestCase):

    def test_c_interleaved_with_unaries(self):
        expr = '0-9'
        expr1, err1 = sqrt_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '0-3')
        expr_c = '0'
        expr2, err2 = square_expr(expr_c)
        self.assertFalse(err2)
        self.assertEqual(expr2, '0')
        expr3, err3 = percent_expr(expr2)
        self.assertFalse(err3)
        self.assertEqual(expr3, '0')

    def test_ce_vs_c_differentiation(self):
        expr = '200+10'
        expr1, err1 = percent_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '200+20')
        ce = clear_entry_expr(expr1)
        self.assertEqual(ce, '200+')
        expr2, err2 = percent_expr(ce)
        self.assertFalse(err2)
        self.assertEqual(expr2, '200+')
        c_expr = '0'
        expr3, err3 = sqrt_expr(c_expr)
        self.assertFalse(err3)
        self.assertEqual(expr3, '0')

    def test_decimal_large_entry_percent(self):
        left = '123456789'
        right = '0,25'
        expr = left + '+' + right
        expected = decimal_to_str(Decimal(left.replace(',', '.')) * (Decimal('0.25') / Decimal('100')))
        res, err = percent_expr(expr)
        self.assertFalse(err)
        self.assertEqual(res, left + '+' + expected)

    def test_reciprocal_zero_error_after_c(self):
        expr = '0'
        res, err = reciprocal_expr(expr)
        self.assertTrue(err)
        self.assertEqual(res, expr)

    def test_overlay_after_c_sqrt(self):
        ov = build_unary_overlay('0', 'sqrt')
        self.assertEqual(ov, '√(0)')
        self.assertEqual(format_history_ops(ov), '√(0)')

    def test_percent_single_value_after_c(self):
        expr = '50'
        expected = decimal_to_str(Decimal('50') / Decimal('100'))
        res, err = percent_expr(expr)
        self.assertFalse(err)
        self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()