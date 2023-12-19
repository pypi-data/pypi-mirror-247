import unittest
from decimal import Decimal

from visualdecimal.expression import symbols, Mul, Add, Div


class ExpressionTestCase(unittest.TestCase):
    def test_multiply(self):
        x, = symbols('x')
        expr = Mul(Decimal(23), x)
        result = expr(bag={
            'x': Decimal(42),
        })
        self.assertEqual(result, Decimal(966))

    def test_multiply_multiple_variables(self):
        x, y = symbols('x y')
        expr = Mul(x, y)
        result = expr(bag={
            'x': Decimal(42),
            'y': Decimal(23),
        })
        self.assertEqual(result, Decimal(966))

    def test_nested(self):
        x, y = symbols('x y')
        expr = Mul(
            Add(
                Div(Decimal(1), Decimal(3)),
                Div(y, Decimal(3))
            ),
            x
        )
        result = expr(bag={
            'x': Decimal(2),
            'y': Decimal(5)
        })
        self.assertEqual(Decimal(4), result)

    def test_pprint(self):
        expr = Mul(Decimal(1), Decimal(2))
        self.assertEqual("1 * 2", expr.pprint())

    def test_pprint_nested(self):
        x, = symbols('x')
        expr = Mul(
            Add(Decimal(23), Decimal(42)),
            x,
        )
        result = expr.pprint(bag={
            'x': Decimal(100)
        })
        self.assertEqual("(23 + 42) * 100", result)


if __name__ == '__main__':
    unittest.main()
