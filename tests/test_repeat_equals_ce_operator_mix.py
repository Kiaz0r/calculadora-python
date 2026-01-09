import unittest
from decimal import Decimal
from core.engine import apply_op, decimal_to_str
from core.operations import clear_entry_expr, sqrt_expr, percent_expr

class TestRepeatEqualsCeOperatorMix(unittest.TestCase):

    def test_repeat_equals_addition_after_ce(self):
        expr = '20+5'
        expr_ce = clear_entry_expr(expr)
        self.assertEqual(expr_ce, '20+')
        b = Decimal('3')
        current = Decimal('20')
        res1 = apply_op('+', current, b)
        self.assertEqual(decimal_to_str(res1), '23')
        res2 = apply_op('+', res1, b)
        self.assertEqual(decimal_to_str(res2), '26')

    def test_repeat_equals_with_operator_change_after_unary_sqrt(self):
        expr = '5+9'
        expr1, err1 = sqrt_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '5+3')
        b = Decimal('3')
        current = Decimal('8')
        res1 = apply_op('+', current, b)
        self.assertEqual(decimal_to_str(res1), '11')
        res2 = apply_op('-', res1, b)
        self.assertEqual(decimal_to_str(res2), '8')
        res3 = apply_op('-', res2, b)
        self.assertEqual(decimal_to_str(res3), '5')

    def test_repeat_equals_addition_after_percent_small_decimal(self):
        expr = '50+0,1'
        expr1, err1 = percent_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '50+0,05')
        b = Decimal('0.05')
        current = Decimal('50')
        res1 = apply_op('+', current, b)
        self.assertEqual(decimal_to_str(res1), '50,05')
        res2 = apply_op('+', res1, b)
        self.assertEqual(decimal_to_str(res2), '50,1')

    def test_repeat_equals_multiplication_after_percent_small_decimal(self):
        expr = '8*0,1'
        expr1, err1 = percent_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '8*0,001')
        b = Decimal('0.001')
        current = Decimal('1')
        res1 = apply_op('*', current, b)
        self.assertEqual(decimal_to_str(res1), '0,001')
        res2 = apply_op('*', res1, b)
        self.assertEqual(decimal_to_str(res2), '0,000001')

    def test_repeat_equals_after_ce_then_operator_change_subtraction(self):
        expr = '20+5'
        expr_ce = clear_entry_expr(expr)
        self.assertEqual(expr_ce, '20+')
        b = Decimal('4')
        current = Decimal('20')
        res1 = apply_op('+', current, b)
        self.assertEqual(decimal_to_str(res1), '24')
        res2 = apply_op('-', res1, b)
        self.assertEqual(decimal_to_str(res2), '20')
        res3 = apply_op('-', res2, b)
        self.assertEqual(decimal_to_str(res3), '16')

if __name__ == '__main__':
    unittest.main()