import unittest
from decimal import Decimal
from core.operations import sqrt_expr, square_expr, reciprocal_expr, percent_expr, clear_entry_expr
from ui.utils import get_current_entry, build_unary_overlay, format_history_ops
from core.engine import decimal_to_str

class TestMicrosoftSemanticsAdditional(unittest.TestCase):

    def test_get_current_entry_zero_minus(self):
        self.assertEqual(get_current_entry('0-9'), '9')
        self.assertEqual(get_current_entry('0-,5'), ',5')

    def test_sqrt_negative_right_operand_in_binary(self):
        res, err = sqrt_expr('3+-9')
        self.assertTrue(err)
        self.assertEqual(res, '3+-9')

    def test_percent_with_minus(self):
        res, err = percent_expr('200-10')
        self.assertFalse(err)
        self.assertEqual(res, '200-20')

    def test_clear_entry_after_unary_result(self):
        self.assertEqual(clear_entry_expr('0-3'), '0-')
        self.assertEqual(clear_entry_expr('0-'), '0-')

    def test_unary_on_decimal_entry(self):
        res, err = sqrt_expr('0-1,44')
        self.assertFalse(err)
        self.assertEqual(res, '0-1,2')
        res2, err2 = reciprocal_expr('0-,5')
        self.assertFalse(err2)
        self.assertEqual(res2, '0-2')
        res3, err3 = square_expr('0-1,5')
        self.assertFalse(err3)
        self.assertEqual(res3, '0-2,25')

    def test_overlay_format_sqrt_zero_minus(self):
        overlay = build_unary_overlay('0-9', 'sqrt')
        self.assertEqual(overlay, '0-√(9)')
        self.assertEqual(format_history_ops(overlay), '0 - √(9)')

if __name__ == '__main__':
    unittest.main()