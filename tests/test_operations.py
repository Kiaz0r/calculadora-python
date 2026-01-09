import unittest
from core.operations import backspace_expr, clear_entry_expr, toggle_sign_expr, percent_expr, reciprocal_expr, square_expr, sqrt_expr

class TestOperations(unittest.TestCase):

    def test_backspace(self):
        self.assertEqual(backspace_expr('123'), '12')
        self.assertEqual(backspace_expr(''), '')

    def test_clear_entry(self):
        self.assertEqual(clear_entry_expr('12+34'), '12+')
        self.assertEqual(clear_entry_expr('12+'), '12+')
        self.assertEqual(clear_entry_expr('12'), '')

    def test_toggle_sign(self):
        self.assertEqual(toggle_sign_expr('12'), '-12')
        self.assertEqual(toggle_sign_expr('-12'), '12')
        self.assertEqual(toggle_sign_expr('1+2'), '1+-2')

    def test_percent_no_op(self):
        res, err = percent_expr('50')
        self.assertFalse(err)
        self.assertEqual(res, '0,5')

    def test_percent_with_plus(self):
        res, err = percent_expr('200+10')
        self.assertFalse(err)
        self.assertEqual(res, '200+20')

    def test_percent_with_multiply(self):
        res, err = percent_expr('200*10')
        self.assertFalse(err)
        self.assertEqual(res, '200*0,1')

    def test_percent_with_divide(self):
        res, err = percent_expr('200/10')
        self.assertFalse(err)
        self.assertEqual(res, '200/0,1')

    def test_percent_right_empty(self):
        res, err = percent_expr('200+')
        self.assertFalse(err)
        self.assertEqual(res, '200+')

    def test_reciprocal(self):
        res, err = reciprocal_expr('4')
        self.assertFalse(err)
        self.assertEqual(res, '0,25')
        res2, err2 = reciprocal_expr('3+4')
        self.assertFalse(err2)
        self.assertEqual(res2, '3+0,25')
        res3, err3 = reciprocal_expr('0')
        self.assertTrue(err3)
        self.assertEqual(res3, '0')

    def test_square(self):
        res, err = square_expr('4')
        self.assertFalse(err)
        self.assertEqual(res, '16')
        res2, err2 = square_expr('3+4')
        self.assertFalse(err2)
        self.assertEqual(res2, '3+16')

    def test_sqrt(self):
        res, err = sqrt_expr('9')
        self.assertFalse(err)
        self.assertEqual(res, '3')
        res2, err2 = sqrt_expr('3+9')
        self.assertFalse(err2)
        self.assertEqual(res2, '3+3')
        res3, err3 = sqrt_expr('-9')
        self.assertTrue(err3)
        self.assertEqual(res3, '-9')
if __name__ == '__main__':
    unittest.main()
