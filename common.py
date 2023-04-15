from pymonad.maybe import Maybe
from collections import deque
from constants import *


class Nothing(Maybe):

    def __init__(self, cause = "Internal Operation Error") -> None:
        super().__init__(None, False)
        self._cause = cause

    @property
    def cause(self):
        return self._cause


class Just(Maybe):

    def __init__(self, value):
        super().__init__(value, True)

    def __eq__(self, obj):
        if isinstance(obj, Just):
            return super().__eq__(obj)
        else:
            if isinstance(obj, (int, float)):
                return self.value == obj
            else: # TODO: analyse this else
                return False

    def __add__(self, obj):
        if isinstance(obj, (int, float)):
            return Just(self.value + obj)
        elif isinstance(obj, Just):
            return Just(self.value + obj.value)
        elif isinstance(obj, Nothing):
            return obj
        else:
            return Nothing('Unsupported type operation')

    def __sub__(self, obj):
        if isinstance(obj, (int, float)):
            return Just(self.value - obj)
        elif isinstance(obj, Just):
            return Just(self.value - obj.value)
        elif isinstance(obj, Nothing):
            return obj
        else:
            return Nothing('Unsupported type operation')

    def __truediv__(self, obj):
        if isinstance(obj, (int, float)):
            if obj == 0:
                return Nothing('Division by zero')
            else:
                return Just(self.value / obj)
        elif isinstance(obj, Just):
            if obj.value == 0:
                return Nothing('Division by zero')
            else:
                return Just(self.value / obj.value)
        elif isinstance(obj, Nothing):
            return obj
        else:
            return Nothing('Unsupported type operation')

    def __mul__(self, obj):
        if isinstance(obj, (int, float)):
            return Just(self.value * obj)
        elif isinstance(obj, Just):
            return Just(self.value * obj.value)
        elif isinstance(obj, Nothing):
            return obj
        else:
            return Nothing('Unsupported type operation')


class Stack(object):

    def __init__(self):
        self._top = 0
        self._deque = deque()

    def __str__(self) -> str:
        return str(self._deque)

    def push(self, value):
        self._top += 1
        self._deque.append(value)

    def pop(self):
        try:
            self._top -= 1
            pop = self._deque.pop()
        except IndexError:
            pop = None
            self._top = 0
        return pop

    @property
    def top(self):
        return self._top



class Queue(object):

    def __init__(self, limit: int = None):
        self._deque = deque()
        self._lenght = 0
        self._lim = limit

    def __str__(self) -> str:
        return str(self._deque)

    @property
    def lenght(self):
        return self._lenght

    @property
    def limit(self):
        return self._lim

    def enqueue(self, value):
        """Add one more element to the queue.
        If a limit where specified on the instantiation of the class,
        when the lenght is equal to the limit, the stack will dequeue
        the first element and the enqueue the new one.
        """
        if self.limit and self.lenght == self.limit:
            self.dequeue()
            self.enqueue(value)
        else:
            self._lenght += 1
            self._deque.append(value)

    def dequeue(self):
        """Removes and return the first element on the list"""
        try:
            self._lenght -= 1
            deq = self._deque.popleft()
        except IndexError:
            self._lenght = 0
            deq = None
        return deq

    def peek(self, index: int = 0):
        """Return the `index` element (default = 0, first), without dequeueing it."""
        try:
            p = self._deque[index]
        except IndexError:
            p = None
        return p

    def list(self) -> list:
        """Return all the elements by order, without dequeueing any of them"""
        assert self.lenght >= 0, 'Error: lenght must be greater than or equal to zero!'
        if self.lenght == 0:
            return []
        else:
            return [self.peek(i) for i in range(self.lenght)]


class Expression(object):
    def eval(self) -> Maybe:
        """Evaluates and returns the value of the Expression"""
        pass


class Const(Expression):

    def __init__(self, value) -> None:
        assert isinstance(value, (str, int, float, Just)), f'type {type(value)} is not supported as Const'
        if isinstance(value, Just):
            self._val = value.value
        else:
            self._val =  eval(value) if isinstance(value, str) else value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def value(self):
        return self._val

    def eval(self) -> Just:
        return Just(self.value)


class BinaryOperation(Expression):
    SYMBOL: str
    NAME: str

    def __init__(self, left: Expression, right: Expression, **kwargs) -> None:
        super(BinaryOperation, self).__init__()
        self._left = left if isinstance(left, Expression) else Const(left)
        self._right = right if isinstance(right, Expression) else Const(right)
        self._show_brackets = False if not 'brackets' in kwargs else kwargs['brackets']

    def __str__(self) -> str:
        output = f'{str(self.left)} {self.SYMBOL} {self.right}'
        return '(%s)' % output if self._show_brackets else output

    def __repr__(self) -> str:
        return f'{self.NAME}({repr(self.left)}, {repr(self.right)})'

    @property
    def left(self) -> Expression:
        return self._left

    @property
    def right(self) -> Expression:
        return self._right


class Add(BinaryOperation):
    NAME = 'Add'
    SYMBOL = SYM_ADD

    def eval(self) -> Maybe:
        return self.left.eval() + self.right.eval()


class Sub(BinaryOperation):
    NAME = 'Sub'
    SYMBOL = SYM_SUB

    def eval(self) -> Maybe:
        return self.left.eval() - self.right.eval()


class Mult(BinaryOperation):
    NAME = 'Mult'
    SYMBOL = SYM_MUL

    def eval(self) -> Maybe:
        return self.left.eval() * self.right.eval()


class Div(BinaryOperation):
    NAME = 'Div'
    SYMBOL = SYM_DIV

    def eval(self) -> Maybe:
        num = self.left.eval()
        denum = self.right.eval()
        if denum == 0:
            return Nothing('Division by zero')
        res = num / denum
        round_res = round(res.value)
        if res == round_res:
            return Just(round_res)
        return res


class Result:

    def __init__(self, word: str, index: int) -> None:
        self._word = word
        self._idx = index

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    @property
    def word(self) -> str:
        """The word that were accepted or rejected"""
        return self._word

    @property
    def index(self) -> int:
        """The index of the rejected word in the sentence."""
        return self._idx


class Acception(Result):

    def __str__(self) -> str:
        return f'Acception [word = {self.word!a}]'

    def __repr__(self) -> str:
        return str(self)


class Rejection(Result):

    def __init__(self, word: str, index: int, why: str) -> None:
        super(Rejection, self).__init__(word, index)
        self._reason = why

    def __str__(self) -> str:
        return f'Rejection [word = {self.word!a}]'

    def __repr__(self) -> str:
        return f'''Rejection: word {self.word!a} at index {self.index}
        \rReason: {self.reason}'''

    @property
    def reason(self) -> str:
        """The reason of the rejection of the word."""
        return self._reason