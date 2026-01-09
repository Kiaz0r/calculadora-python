import unittest
from decimal import Decimal
from core.engine import apply_op, decimal_to_str
from core.operations import sqrt_expr, percent_expr, reciprocal_expr

class TestRepeatEqualsUnaryMix(unittest.TestCase):

    def _get_right_decimal(self, expr: str) -> Decimal:
        i = len(expr) - 1
        last_op_idx = None
        while i >= 0:
            ch = expr[i]
            if ch in '+*/':
                last_op_idx = i
                break
            if ch == '-':
                if not (i == 0 or expr[i - 1] in '+-*/'):
                    last_op_idx = i
                    break
            i -= 1
        if last_op_idx is None:
            right = expr
        else:
            right = expr[last_op_idx + 1:]
        if right.startswith(','):
            right = '0' + right
        elif right.startswith('-,'):
            right = '-0' + right[1:]
        return Decimal(right.replace(',', '.'))

    def test_addition_after_sqrt_then_repeat_equals(self):
        expr = '5+9'
        expr1, err1 = sqrt_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '5+3')
        b = self._get_right_decimal(expr1)
        current = Decimal('8')
        res1 = apply_op('+', current, b)
        self.assertEqual(decimal_to_str(res1), '11')
        res2 = apply_op('+', res1, b)
        self.assertEqual(decimal_to_str(res2), '14')

    def test_subtraction_after_sqrt_then_repeat_equals(self):
        expr = '5-4'
        expr1, err1 = sqrt_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '5-2')
        b = self._get_right_decimal(expr1)
        current = Decimal('5')
        res1 = apply_op('-', current, b)
        self.assertEqual(decimal_to_str(res1), '3')
        res2 = apply_op('-', res1, b)
        self.assertEqual(decimal_to_str(res2), '1')

    def test_multiplication_after_percent_then_repeat_equals(self):
        expr = '2*50'
        expr1, err1 = percent_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '2*0,5')
        b = self._get_right_decimal(expr1)
        current = Decimal('1')
        res1 = apply_op('*', current, b)
        self.assertEqual(decimal_to_str(res1), '0,5')
        res2 = apply_op('*', res1, b)
        self.assertEqual(decimal_to_str(res2), '0,25')

    def test_division_after_reciprocal_then_repeat_equals(self):
        expr = '10/4'
        expr1, err1 = reciprocal_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '10/0,25')
        b = self._get_right_decimal(expr1)
        current = Decimal('40')
        res1 = apply_op('/', current, b)
        self.assertEqual(decimal_to_str(res1), '160')
        res2 = apply_op('/', res1, b)
        self.assertEqual(decimal_to_str(res2), '640')

    def test_addition_with_negative_right_then_repeat_equals(self):
        expr = '5+-3'
        b = self._get_right_decimal(expr)
        current = Decimal('2')
        res1 = apply_op('+', current, b)
        self.assertEqual(decimal_to_str(res1), '-1')
        res2 = apply_op('+', res1, b)
        self.assertEqual(decimal_to_str(res2), '-4')

if __name__ == '__main__':
    unittest.main()