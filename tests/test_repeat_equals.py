import unittest
from decimal import Decimal
from core.engine import apply_op, decimal_to_str

class TestRepeatEquals(unittest.TestCase):

    def test_repeat_equals_addition(self):
        op = '+'
        operand = Decimal('3')
        current = Decimal('8')
        res1 = apply_op(op, current, operand)
        self.assertEqual(decimal_to_str(res1), '11')
        res2 = apply_op(op, res1, operand)
        self.assertEqual(decimal_to_str(res2), '14')

    def test_repeat_equals_subtraction(self):
        op = '-'
        operand = Decimal('2')
        current = Decimal('5')
        res1 = apply_op(op, current, operand)
        self.assertEqual(decimal_to_str(res1), '3')
        res2 = apply_op(op, res1, operand)
        self.assertEqual(decimal_to_str(res2), '1')

    def test_repeat_equals_multiplication(self):
        op = '*'
        operand = Decimal('2')
        current = Decimal('6')
        res1 = apply_op(op, current, operand)
        self.assertEqual(decimal_to_str(res1), '12')
        res2 = apply_op(op, res1, operand)
        self.assertEqual(decimal_to_str(res2), '24')

    def test_repeat_equals_division(self):
        op = '/'
        operand = Decimal('2')
        current = Decimal('8')
        res1 = apply_op(op, current, operand)
        self.assertEqual(decimal_to_str(res1), '4')
        res2 = apply_op(op, res1, operand)
        self.assertEqual(decimal_to_str(res2), '2')

if __name__ == '__main__':
    unittest.main()