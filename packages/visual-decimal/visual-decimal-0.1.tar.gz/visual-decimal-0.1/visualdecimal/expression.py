from decimal import Decimal
from math import floor
from typing import List, Dict


def _marshal_decimal(value, *args, **kwargs) -> Decimal:
    if isinstance(value, Expression):
        return value(*args, **kwargs)
    elif isinstance(value, Decimal):
        return value
    else:
        raise ValueError("value must be either a decimal or an expression")


def _marshal_repr(value, *args, **kwargs) -> str:
    if isinstance(value, Symbol):
        return str(value(*args, **kwargs))
    elif isinstance(value, Expression):
        return "({})".format(value.pprint(*args, **kwargs))
    elif isinstance(value, Decimal):
        return str(value)
    else:
        raise ValueError("value must be either a decimal or an expression")


class Expression:
    """
    Expression is the base class for all mathematical expressions.
    """
    def __call__(self, *args, **kwargs) -> Decimal:
        """
        Evaluates the mathematical expression.
        """
        raise NotImplementedError

    def pprint(self, *args, **kwargs) -> str:
        raise NotImplementedError


class ABExpression(Expression):
    """
    ABExpression is the base class for mathematical expressions involving two operands.
    """
    def __init__(self, a, b, calc, pprint):
        self.a = a
        self.b = b
        self.calc_func = calc
        self.pprint_func = pprint

    def __call__(self, *args, **kwargs):
        a = _marshal_decimal(self.a, *args, **kwargs)
        b = _marshal_decimal(self.b, *args, **kwargs)
        return self.calc_func(a, b)

    def pprint(self, *args, **kwargs) -> str:
        a = _marshal_repr(self.a, *args, **kwargs)
        b = _marshal_repr(self.b, *args, **kwargs)
        return self.pprint_func(a, b)


class Mul(ABExpression):

    def __init__(self, a, b):
        super().__init__(
            a, b,
            lambda x, y: x * y,
            lambda x, y: "{} * {}".format(x, y)
        )


def _pprint_division(a: str, b: str):
    max_len = max(len(a), len(b))
    pad_a = floor(max_len - len(a) / 2)
    pad_b = floor(max_len - len(b) / 2)
    return "{}\n{}\n{}".format(
        a.rjust(pad_a),
        "―" * max_len,
        b.rjust(pad_b),
    )


class Div(ABExpression):
    def __init__(self, a, b):
        super().__init__(
            a, b,
            lambda x, y: x / y,
            _pprint_division,
        )


class Add(ABExpression):
    def __init__(self, a, b):
        super().__init__(
            a, b,
            lambda x, y: x + y,
            lambda x, y: "{} + {}".format(x, y)
        )


class Sub(ABExpression):
    def __init__(self, a, b):
        super().__init__(
            a, b,
            lambda x, y: x - y,
            lambda x, y: "{} - {}".format(x, y)
        )


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs) -> Decimal:
        bag = kwargs.pop("bag", None)
        if isinstance(bag, dict):
            return self.eval(bag)
        raise ValueError("Bag must be a dictionary")

    def eval(self, bag: Dict[str, Decimal]) -> Decimal:
        if self.name not in bag:
            raise ValueError(f'Symbol {self.name} not found in bag')
        return bag[self.name]


def symbols(template: str) -> List[Symbol]:
    return [
        Symbol(name)
        for name in template.split(' ')
    ]
