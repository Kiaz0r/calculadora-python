import unittest
from decimal import Decimal
from core.operations import toggle_sign_expr, percent_expr, sqrt_expr, clear_entry_expr
from ui.utils import build_unary_overlay, format_history_ops
from core.engine import decimal_to_str

class TestMsToggleSequences(unittest.TestCase):

    def test_toggle_then_percent_on_right(self):
        expr = '100+2'
        toggled = toggle_sign_expr(expr)
        self.assertEqual(toggled, '100+-2')
        res, err = percent_expr(toggled)
        self.assertFalse(err)
        self.assertEqual(res, '100+-2')

    def test_toggle_on_decimal_comma_entry(self):
        self.assertEqual(toggle_sign_expr(',5'), '-,5')
        self.assertEqual(toggle_sign_expr('-,5'), ',5')

    def test_overlay_reciprocal_zero_minus_small_decimal(self):
        ov = build_unary_overlay('0-,05', 'reciprocal')
        self.assertEqual(ov, '0-1/(0,05)')
        self.assertEqual(format_history_ops(ov), '0 - 1 ÷ (0,05)')

    def test_multiply_percent_decimal(self):
        expr = '250*0,2'
        res, err = percent_expr(expr)
        self.assertFalse(err)
        self.assertEqual(res, '250*0,002')

    def test_divide_ce_then_unary_noop_on_empty_right(self):
        expr = '200/0,5'
        ce = clear_entry_expr(expr)
        self.assertEqual(ce, '200/')
        res, err = sqrt_expr(ce)
        self.assertFalse(err)
        self.assertEqual(res, '200/')

    def test_toggle_on_right_empty_after_ce(self):
        expr = '200+'
        self.assertEqual(toggle_sign_expr(expr), '-200+')

if __name__ == '__main__':
    unittest.main()