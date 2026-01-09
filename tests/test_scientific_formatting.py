import unittest
from core.formatting import format_display

class TestScientificFormatting(unittest.TestCase):

    def test_scientific_integers_variants(self):
        cases = [('12345678901234567', '1,234567890123456e+16'), ('-12345678901234567', '−1,234567890123456e+16'), ('+12345678901234567', '+1,234567890123456e+16'), (' +12345678901234567', ' +1,234567890123456e+16'), ('   +12345678901234567', '   +1,234567890123456e+16'), ('\t\t+12345678901234567', '\t\t+1,234567890123456e+16')]
        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(format_display(expr), expected)

    def test_scientific_fractions_variants(self):
        cases = [('0,0000000000001234567890123456', '1,234567890123456e-13'), ('-0,0000000000001234567890123456+2', '−1,234567890123456e-13+2'), ('+0,000000000000001234', '+1,234e-15'), (' +0,000000000000001234', ' +1,234e-15'), ('    +0,000000000000001234', '    +1,234e-15'), ('\t\t+0,000000000000001234', '\t\t+1,234e-15'), ('+0,000000000000001234567890123456', '+1,234567890123456e-15'), ('    +0,0000000000000012345678901234567', '    +1,234567890123456e-15'), ('+---0,0000000000001234', '−1,234e-13')]
        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(format_display(expr), expected)

    def test_scientific_operations_mix(self):
        cases = [('12*0,0000000000001234567890123456', '12×1,234567890123456e-13'), ('1-0,0000000000001234567890123456', '1-1,234567890123456e-13'), ('2+-0,0000000000001234', '2+−1,234e-13'), ('12/0,0000000000001234567890123456', '12÷1,234567890123456e-13'), ('12/-0,0000000000001234567890123456', '12÷−1,234567890123456e-13'), ('12*-0,0000000000001234567890123456', '12×−1,234567890123456e-13')]
        for expr, expected in cases:
            with self.subTest(expr=expr):
                self.assertEqual(format_display(expr), expected)
if __name__ == '__main__':
    unittest.main()
