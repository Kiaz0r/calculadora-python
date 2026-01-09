import unittest
from decimal import Decimal
from core.operations import sqrt_expr, square_expr, reciprocal_expr, percent_expr, clear_entry_expr
from core.engine import decimal_to_str
from ui.utils import build_unary_overlay, format_history_ops

class TestMsSequencesExtended(unittest.TestCase):

    def test_unary_chain_zero_minus_nine(self):
        expr = '0-9'
        expr1, err1 = sqrt_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '0-3')
        expr2, err2 = square_expr(expr1)
        self.assertFalse(err2)
        self.assertEqual(expr2, '0-9')
        expr3, err3 = reciprocal_expr(expr2)
        self.assertFalse(err3)
        expected_right = decimal_to_str(Decimal('1') / Decimal('9'))
        self.assertEqual(expr3, '0-' + expected_right)
        expr4, err4 = percent_expr(expr3)
        self.assertFalse(err4)
        self.assertEqual(expr4, '0-0')

    def test_clear_entry_after_chain(self):
        expr = '0-9'
        expr1, err1 = sqrt_expr(expr)
        self.assertFalse(err1)
        self.assertEqual(expr1, '0-3')
        ce = clear_entry_expr(expr1)
        self.assertEqual(ce, '0-')

    def test_overlay_variants_after_zero_minus(self):
        ov1 = build_unary_overlay('0-9', 'sqrt')
        self.assertEqual(ov1, '0-√(9)')
        self.assertEqual(format_history_ops(ov1), '0 - √(9)')
        ov2 = build_unary_overlay('0-9', 'square')
        self.assertEqual(ov2, '0-(9)²')
        self.assertEqual(format_history_ops(ov2), '0 - (9)²')
        ov3 = build_unary_overlay('0-9', 'reciprocal')
        self.assertEqual(ov3, '0-1/(9)')
        self.assertEqual(format_history_ops(ov3), '0 - 1 ÷ (9)')
        ov4 = build_unary_overlay('0-9', 'percent')
        self.assertEqual(ov4, '0-9%')
        self.assertEqual(format_history_ops(ov4), '0 - 9%')

if __name__ == '__main__':
    unittest.main()