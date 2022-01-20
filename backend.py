from collections import deque
import string


class Stack(object):

    def __init__(self):
        self._top = 0
        self._block = deque()

    def push(self, value):
        self._top += 1
        self._block.append(value)

    def pop(self):
        try:
            self._top -= 1
            pop = self._block.pop()
        except IndexError:
            pop = None
            self._top = 0
        return pop

    @property
    def top(self):
        return self._top

class Expression(object):
    SYMBOLS = {'+', '-', 'x', '/'}

    def eval(env: dict = None):
        pass

    def __repr__(self) -> str:
        return super().__repr__()
    
    def __str__(self) -> str:
        return super().__str__()
    
    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o)
    
    @property
    def is_variable(self) -> bool:
        pass


class SingleExpression(Expression):
    pass


class Var(SingleExpression):
    pass


class Const(SingleExpression):
    pass


class BinaryOperation(Expression):
    SYMBOL: str

    def __init__(self, left: Expression, right: Expression) -> None:
        super(BinaryOperation, self).__init__()
        self._left = left
        self._right = right
    
    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def is_variable(self) -> bool:
        return self._left.is_variable or self._right.is_variable


class Add(BinaryOperation):
    pass


class Sub(BinaryOperation):
    pass


class Mult(BinaryOperation):
    pass


class Div(BinaryOperation):
    pass


class AutomataResult:
    
    def __init__(self, word: str) -> None:
        self._word = word

    @property
    def word(self):
        return self._word


class Acception(AutomataResult):
    pass


class Rejection(AutomataResult):
    
    def __init__(self, word: str, why: str) -> None:
        super(Rejection, self).__init__(word)
        self._reason = why

    @property
    def why(self):
        return self._reason


class Automata:

    def __init__(self) -> None:
        self.stack = Stack()
        self.stack.push('$')
        self._left_parentheses = '('
        self._right_parentheses = ')'
        self.stack_alphabet = {
            self._left_parentheses,
            self._right_parentheses
        }
        self.alphabet = Expression.SYMBOLS.union(
            string.digits + ' '
        )

    def _read(self, word: str) -> AutomataResult:
        if word in self.alphabet:
            return Acception(word)
        elif word in self.stack_alphabet:            
            if word == self._left_parentheses:
                self.stack.push(word)
                return Acception(word)
            else:
                pop = self.stack.pop()
                return Acception(word) if pop == self._left_parentheses          \
                         else Rejection(word, 'Syntax Error: Unclosed Parentheses.')
        else:
            return Rejection(word, 'Syntax Error: Word not Recognized.')

    def analyze(self, sentence: str) -> AutomataResult:
        result = Rejection('', 'Syntax Error: Empty Value.')
        for char in sentence.strip():
            if isinstance(result := self._read(char), Rejection):
                return result
        return result