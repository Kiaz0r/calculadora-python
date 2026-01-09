import unittest
from core.operations import clear_entry_expr, sqrt_expr, percent_expr
from ui.utils import build_unary_overlay, format_history_ops

class TestMsCeCSequences(unittest.TestCase):

    def test_clear_entry_right_decimal_with_zero_minus(self):
        self.assertEqual(clear_entry_expr('0-1,2'), '0-')

    def test_clear_entry_negative_standalone(self):
        self.assertEqual(clear_entry_expr('-9'), '')

    def test_sqrt_with_empty_right_after_minus(self):
        res, err = sqrt_expr('0-')
        self.assertFalse(err)
        self.assertEqual(res, '0-')

    def test_percent_with_empty_right_after_minus(self):
        res, err = percent_expr('0-')
        self.assertFalse(err)
        self.assertEqual(res, '0-')

    def test_overlay_format_square_zero_minus(self):
        overlay = build_unary_overlay('0-1,5', 'square')
        self.assertEqual(overlay, '0-(1,5)²')
        self.assertEqual(format_history_ops(overlay), '0 - (1,5)²')

    def test_overlay_format_reciprocal_zero_minus(self):
        overlay = build_unary_overlay('0-9', 'reciprocal')
        self.assertEqual(overlay, '0-1/(9)')
        self.assertEqual(format_history_ops(overlay), '0 - 1 ÷ (9)')

if __name__ == '__main__':
    unittest.main()