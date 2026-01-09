import unittest
from decimal import Decimal, getcontext
from core.operations import percent_expr, sqrt_expr, square_expr, reciprocal_expr
from core.engine import decimal_to_str

class TestMsSequencesLongChain(unittest.TestCase):

    def test_percent_sqrt_square_reciprocal_chain(self):
        expr = '50+10'
        p1, e1 = percent_expr(expr)
        self.assertFalse(e1)
        self.assertEqual(p1, '50+5')
        s1, e2 = sqrt_expr(p1)
        self.assertFalse(e2)
        expected_sqrt = decimal_to_str(getcontext().sqrt(Decimal('5')))
        self.assertEqual(s1, '50+' + expected_sqrt)
        sq1, e3 = square_expr(s1)
        self.assertFalse(e3)
        sqrt_val = Decimal(expected_sqrt.replace(',', '.'))
        expected_after_sq = decimal_to_str(sqrt_val * sqrt_val)
        self.assertEqual(sq1, '50+' + expected_after_sq)
        r1, e4 = reciprocal_expr(sq1)
        self.assertFalse(e4)
        expected_recip = decimal_to_str(Decimal('1') / Decimal(expected_after_sq.replace(',', '.')))
        self.assertEqual(r1, '50+' + expected_recip)

if __name__ == '__main__':
    unittest.main()