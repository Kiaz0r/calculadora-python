import unittest
from core.formatting import format_display

class TestFormatting(unittest.TestCase):

    def test_empty_expr(self):
        self.assertEqual(format_display(''), '0')

    def test_basic_formatting_cases(self):
        cases = [('1234', '1.234'), ('1234567', '1.234.567'), ('12,34', '12,34'), ('12345,67', '12.345,67'), ('00012', '12'), ('0000', '0'), ('12+34', '12+34'), ('12*34', '12×34'), ('12/34', '12÷34'), ('12-34', '12-34'), ('-34+5', '−34+5'), ('12*-3', '12×−3'), ('-1234567', '−1.234.567'), ('1,', '1,'), ('-,5', '−0,5'), ('1+---,5', '1+−0,5'), ('1+-+-,5', '1+0,5'), (' 2 + 3 ', ' 2 + 3 '), ('\t2\t+\t3\t', '\t2\t+\t3\t')]
        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(format_display(expr), expected)
if __name__ == '__main__':
    unittest.main()
