import unittest
from decimal import Decimal, DivisionByZero
from core.engine import evaluate_decimal_expr, normalize_decimal_tokens, decimal_to_str, result_exceeds_limits

class TestEngine(unittest.TestCase):

    def test_precedence_and_associativity(self):
        self.assertEqual(decimal_to_str(evaluate_decimal_expr('2+3*4')), '14')
        self.assertEqual(decimal_to_str(evaluate_decimal_expr('10/2*5')), '25')
        self.assertEqual(decimal_to_str(evaluate_decimal_expr('5-2-1')), '2')
        self.assertEqual(decimal_to_str(evaluate_decimal_expr('8/4/2')), '1')
        self.assertEqual(decimal_to_str(evaluate_decimal_expr('1,5+2,25')), '3,75')
        self.assertEqual(decimal_to_str(evaluate_decimal_expr('-,5+1')), '0,5')

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZero):
            evaluate_decimal_expr('1/0')

    def test_normalize_tokens(self):
        self.assertEqual(normalize_decimal_tokens(',5'), '0,5')
        self.assertEqual(normalize_decimal_tokens('-,25'), '-0,25')
        self.assertEqual(normalize_decimal_tokens('1+,5'), '1+0,5')
        self.assertEqual(normalize_decimal_tokens('1+-,5'), '1+-0,5')

    def test_decimal_to_str_fraction_trunc(self):
        d = evaluate_decimal_expr('1/3')
        s = decimal_to_str(d)
        self.assertTrue(s.startswith('0,'))
        self.assertEqual(len(s.split(',')[1]), 12)
        self.assertEqual(decimal_to_str(Decimal('1.230000000000')), '1,23')

    def test_result_exceeds_limits(self):
        d_ok_int = Decimal('1e29')
        self.assertFalse(result_exceeds_limits(d_ok_int))
        d_bad_int = Decimal('1e31')
        self.assertTrue(result_exceeds_limits(d_bad_int))
        d_ok_sig = Decimal('0.' + '1' * 60)
        self.assertFalse(result_exceeds_limits(d_ok_sig))

    def test_spaces_in_expr(self):
        self.assertEqual(decimal_to_str(evaluate_decimal_expr(' 2 + 3 * 4 ')), '14')

    def test_multiple_unary_minus(self):
        res1 = decimal_to_str(evaluate_decimal_expr('--5'))
        self.assertEqual(res1, '5')
        res2 = decimal_to_str(evaluate_decimal_expr('---5'))
        self.assertEqual(res2, '-5')

    def test_unary_on_fraction_with_comma(self):
        res = decimal_to_str(evaluate_decimal_expr('---,5'))
        self.assertEqual(res, '-0,5')
if __name__ == '__main__':
    unittest.main()
