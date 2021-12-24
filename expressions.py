import math


# TODO: add option to turn with vars expressions into a equation,
#       and operate over it. Could do things like:
#             -> turn into a function of n vars and, test solutions for n = k, for k in Real set
#             -> Solve it if it is a quadratic or a linear equation 
#             -> Store the previous calculation on a stack or list - The better option - The better option!


class Expression(object):
    _IS_VARIABLE: bool

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    def __add__(self, value):
        if isinstance(value, (Expression, int, float, str)):
            return Add(self, value)
        else:
            raise ValueError(f'Type {type(value)} not allowed on this operation!')

    def __eq__(self, other) -> bool:
        if isinstance(other, Expression):
            assert other.is_var() is False, 'This operation cannot be used with variable expressions!'
            return self.eval() == other.eval()
        elif isinstance(other, int) or isinstance(other, float):
            return other == self.eval()
        else:
            return False

    def is_zero(self, env=None) -> bool:
        """Returns if the value of this expression is equal zero."""
        return bool(self.eval(env) == 0)

    def is_negative(self, env=None) -> bool:
        """Returns if this expression is a negative value."""
        return bool(self.eval(env) < 0)

    def is_positive(self, env=None) -> bool:
        """Returns if this expression is a positive value."""
        return bool(self.eval(env) > 0)

    @classmethod
    def is_var(cls) -> bool:
        return cls._IS_VARIABLE

    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        pass

    def eval(self, env=None) -> float or int:
        pass


class Const(Expression):
    _IS_VARIABLE: bool = False

    def __init__(self, val):
        assert isinstance(val, int) or isinstance(val, float), " 'val' must be numeric type! "
        self.val = val

    def __str__(self):
        return str(self.val)

    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        return set()

    def eval(self, env=None):
        return self.val


class Var(Expression):
    _IS_VARIABLE: bool = True

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return str(self.name)

    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        return {self.name}

    def eval(self, env: dict):
        if isinstance(env, dict):
            return env[self.name]
        else:
            print('Error: Must give the value of the variable for the evaluation!')
            exit(1)


class BinaryOperation(Expression):
    _OPERATION_SYMBOLS: tuple = ('+', '-', '*', '/')
    _SYMBOL: str
    _OPERATION_NAME: str

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = self.get_new_expr(left)
        self.right = self.get_new_expr(right)

        self._space_when_printing_symbol = True

    def __str__(self) -> str:
        if self._space_when_printing_symbol is True:
            string = f'{str(self.left)} {self._SYMBOL} {str(self.right)}'
        else:
            string = f'{str(self.left)}{self._SYMBOL}{str(self.right)}'
        return string

    def __repr__(self) -> str:
        return f'{self._OPERATION_NAME}({self.left.__repr__()}, {self.right.__repr__()})'

    def is_var(self) -> bool:
        """Returns if this Binary operation is variable (if it has a variable)"""
        return self.left.is_var() or self.right.is_var()

    def get_variables(self) -> set:
        """Return a set with all variables of the Operation inside."""
        return self.left.get_variables().union(self.right.get_variables())

    @staticmethod
    def get_new_expr(term) -> Expression:
        if isinstance(term, Expression):
            return term
        elif isinstance(term, int) or isinstance(term, float):
            return Const(term)
        elif isinstance(term, str):
            if term.isalpha():
                return Var(term)
            elif term.isnumeric():
                return Const(eval(term))
            else: # TODO: improve this section
                try:
                    return Const(float(term))
                except ValueError:
                    pass
        raise ValueError(f"Got unsupported value: {term!r}")


class Add(BinaryOperation):
    _OPERATION_NAME = 'Add'
    _SYMBOL = '+'

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 + b*10) / 10
        else:
            res = a + b
        return res


class Sub(BinaryOperation):
    _OPERATION_NAME = 'Sub'
    _SYMBOL = '-'

    def eval(self, env=None):
        a = self.left.eval(env)
        b = self.right.eval(env)
        if 0 < a < 1 or 0 < b < 1:
            res = (a*10 - b*10) / 10
        else:
            res = a - b
        return res


class Mult(BinaryOperation):
    _OPERATION_NAME = 'Times'
    _SYMBOL = '*'

    def __init__(self, left: Expression, right: Expression):
        super(Mult, self).__init__(left, right)
        self._space_when_prSinting_symbol = False

    def eval(self, env=None):
        return self.left.eval(env) * self.right.eval(env)


class Div(BinaryOperation):
    _OPERATION_NAME = 'Div'
    _SYMBOL = '/'

    def __init__(self, left: Expression, right: Expression):
        super(Div, self).__init__(left, right)
        self._space_when_printing_symbol = False

    def eval(self, env=None):
        if self.right.is_zero(env):
            raise ZeroDivisionError(f"Can't divide a number by zero: {self.left}/{self.right.eval(env)}")

        result = self.left.eval(env) / self.right.eval(env)
        truncated_result = math.trunc(result)

        if truncated_result == result:
            return truncated_result
        else:
            return result


class Exp(BinaryOperation):
    _OPERATION_NAME = 'Exp'
    _SYMBOL = '^'

    def __init__(self, base: Expression, exp: Expression):
        super().__init__(base, exp)
        # TODO: finish this section
        pass


def expr(string: str, allow_variables: bool = False) -> Expression:
    """Read a string expression and return the object class representing the operation.

    Args:
        expression: (str) a string with the expression (e.g. `'2 + 3'`)
        allow_variables: (bool) if True the function will allow expressions with variables too (e.g. `'x + 9'`)

    Returns:
        Expression (an instantiated object of a subclass of Expression)

    Usage:
    >>> expression = expr('4 * 5 - 10')
    >>> expression
    Sub(Times(4, 5), 10)
    >>> print(expression)
    '4*5 - 10'
    >>> expression.eval()
    10
    """
    EXPRESSIONS = dict([
        (Add._SYMBOL, Add),
        (Sub._SYMBOL, Sub),
        (Mult._SYMBOL, Mult),
        (Div._SYMBOL, Div)
        ])
    expression = string if string.rstrip()[0] != Sub._SYMBOL else '0 ' + string.rstrip()
    for symbol in EXPRESSIONS.keys():
        if symbol in expression:
            left, *right = expression.split(symbol)
            expr_class = EXPRESSIONS.get(symbol)

            if expr_class is not Sub:
                new_right_expr = symbol.join(right)
            else:
                new_right_expr = Add._SYMBOL.join(right)

            return expr_class(
                expr(left.strip(), allow_variables),
                expr(new_right_expr.strip(), allow_variables)
            )
    else:
        expr_obj = BinaryOperation.get_new_expr(expression)
        if expr_obj.is_var() and not allow_variables:
            raise ValueError("Variables are not allowed on this mode!")
        return expr_obj
