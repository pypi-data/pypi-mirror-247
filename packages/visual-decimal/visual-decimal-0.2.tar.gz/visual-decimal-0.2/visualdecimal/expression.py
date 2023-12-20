from decimal import Decimal
from typing import List, Dict


def _marshal_decimal(value, *args, **kwargs) -> Decimal:
    if isinstance(value, Expression):
        return value.eval(*args, **kwargs)
    elif isinstance(value, Decimal):
        return value
    else:
        raise ValueError("value must be either a decimal or an expression")


class Expression:
    """
    Expression is the base class for all mathematical expressions.
    """
    def eval(self, *args, **kwargs) -> Decimal:
        """
        Evaluates the mathematical expression.
        """
        raise NotImplementedError

    def accept(self, visitor: 'ExpressionVisitor'):
        """
        Accepts the expression visitor, traversing the tree structure.
        """
        visitor.before_expression(self)
        self.accept_children(visitor)
        visitor.after_expression(self)

    def accept_children(self, visitor: 'ExpressionVisitor'):
        raise NotImplementedError


class ExpressionVisitor:
    """
    ExpressionVisitor is the base class for custom visitors of an expression tree.
    """
    def before_expression(self, expression: Expression):
        """
        Called before an expression is encountered.
        """
        return

    def before_children(self, expression: Expression):
        """
        Called before children are visited.
        """
        return

    def after_children(self, expression: Expression):
        """
        Called after children have been visited.
        """
        return

    def after_expression(self, expression: Expression):
        """
        Called after an expression is encountered.
        """
        return

    def on_decimal(self, value: Decimal):
        """
        Called when a Decimal object is encountered inside an expression.
        """
        return


class ABExpression(Expression):
    """
    ABExpression is the base class for mathematical expressions involving two operands.
    """
    def __init__(self, a, b, calc):
        self.a = a
        self.b = b
        self.calc_func = calc

    def eval(self, *args, **kwargs):
        a = _marshal_decimal(self.a, *args, **kwargs)
        b = _marshal_decimal(self.b, *args, **kwargs)
        return self.calc_func(a, b)

    def accept_children(self, visitor: 'ExpressionVisitor'):
        visitor.before_children(self)

        if isinstance(self.a, Expression):
            self.a.accept(visitor)
        elif isinstance(self.a, Decimal):
            visitor.on_decimal(self.a)

        if isinstance(self.b, Expression):
            self.b.accept(visitor)
        elif isinstance(self.b, Decimal):
            visitor.on_decimal(self.b)

        visitor.after_children(self)

class Const(Expression):
    def __init__(self, name: str, value: Decimal):
        self.name = name
        self.value = value

    def eval(self, *args, **kwargs):
        return self.value

    def accept_children(self, visitor: 'ExpressionVisitor'):
        visitor.on_decimal(self.value)


class Mul(ABExpression):

    def __init__(self, a, b):
        super().__init__(a, b, lambda x, y: x * y)


class Div(ABExpression):
    def __init__(self, a, b):
        super().__init__(a, b, lambda x, y: x / y)


class Add(ABExpression):
    def __init__(self, a, b):
        super().__init__(a, b, lambda x, y: x + y)


class Sub(ABExpression):
    def __init__(self, a, b):
        super().__init__(a, b, lambda x, y: x - y)


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def eval(self, *args, **kwargs) -> Decimal:
        variables = kwargs.pop("variables", None)
        if isinstance(variables, dict):
            return self.substitute(variables)
        raise ValueError("Variables must be a dictionary")

    def substitute(self, variables: Dict[str, Decimal]) -> Decimal:
        if self.name not in variables:
            raise ValueError(f'Symbol {self.name} not found in variables')
        return variables[self.name]

    def accept_children(self, visitor: 'ExpressionVisitor'):
        return


def symbols(template: str) -> List[Symbol]:
    return [
        Symbol(name)
        for name in template.split(' ')
    ]
