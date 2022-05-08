from pymonad.maybe import Maybe
from queue import LifoQueue
import string

EOF: str = '$'

class Nothing(Maybe):

    def __init__(self, cause = None) -> None:
        super().__init__(None, False)
        self.__cause = cause

    @property
    def cause(self):
        return self.__cause


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
        self._stack = LifoQueue()

    def __str__(self) -> str:
        return str(self._stack.queue)

    def push(self, item):
        self._stack.put(item)

    def pop(self):
        item = None
        if not self._stack.empty():
            item = self._stack.get()
        return item


# TODO: update to the lib queue
class Queue(object):

    def __init__(self, limit: int = None):
        self._stack = Queue()

    def __str__(self) -> str:
        return str(self.__deque)

    @property
    def lenght(self):
        return self.__lenght

    @property
    def limit(self):
        return self.__lim

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
            self.__lenght += 1
            self.__deque.append(value)

    def dequeue(self):
        """Removes and return the first element on the list"""
        try:
            self.__lenght -= 1
            deq = self.__deque.popleft()
        except IndexError:
            self.__lenght = 0
            deq = None
        return deq

    def peek(self, index: int = 0):
        """Return the `index` element (default = 0, first), without dequeueing it."""
        try:
            p = self.__deque[index]
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
    SYMBOLS = {'+', '-', '*', '/'}

    def eval(self) -> Maybe:
        """Evaluates and returns the value of the Expression"""
        pass


class Const(Expression):

    def __init__(self, value) -> None:
        assert isinstance(value, (str, int, float, Just)), f'type {type(value)} is not supported as Const'
        if isinstance(value, Just):
            self.__val = value.value
        else:
            self.__val =  eval(value) if isinstance(value, str) else value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def value(self):
        return self.__val

    def eval(self) -> Just:
        return Just(self.value)


class BinaryOperation(Expression):
    SYMBOL: str
    NAME: str

    def __init__(self, left: Expression, right: Expression, **kwargs) -> None:
        super(BinaryOperation, self).__init__()
        self.__left = left if isinstance(left, Expression) else Const(left)
        self.__right = right if isinstance(right, Expression) else Const(right)
        self.__print_with_parentheses = False
        if 'parentheses' in kwargs:
            self.__print_with_parentheses = kwargs['parentheses']

    def __str__(self) -> str:
        output = f'{str(self.left)} {self.SYMBOL} {self.right}'
        if self.__print_with_parentheses is True:
            return '(%s)' % output
        return output

    def __repr__(self) -> str:
        return f'{self.NAME}({repr(self.left)}, {repr(self.right)})'

    @property
    def left(self) -> Expression:
        return self.__left

    @property
    def right(self) -> Expression:
        return self.__right


class Add(BinaryOperation):
    NAME = 'Add'
    SYMBOL = '+'

    def eval(self) -> Maybe:
        return self.left.eval() + self.right.eval()


class Sub(BinaryOperation):
    NAME = 'Sub'
    SYMBOL = '-'

    def eval(self) -> Maybe:
        return self.left.eval() - self.right.eval()


class Mult(BinaryOperation):
    NAME = 'Mult'
    SYMBOL = '*'

    def eval(self) -> Maybe:
        return self.left.eval() * self.right.eval()


class Div(BinaryOperation):
    NAME = 'Div'
    SYMBOL = '/'

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
        self.__word = word
        self.__idx = index

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        pass

    @property
    def word(self) -> str:
        """The word that were accepted or rejected"""
        return self.__word

    @property
    def index(self) -> int:
        """The index of the rejected word in the sentence."""
        return self.__idx


class Acception(Result):

    def __str__(self) -> str:
        return f'Acception [word = {self.word!a}]'

    def __repr__(self) -> str:
        return str(self)


class Rejection(Result):

    def __init__(self, word: str, index: int, why: str) -> None:
        super(Rejection, self).__init__(word, index)
        self.__reason = why

    def __str__(self) -> str:
        return f'Rejection [word = {self.word!a}]'

    def __repr__(self) -> str:
        return f'''Rejection: word {self.word!a} at index {self.index}
        \rReason: {self.reason}'''

    @property
    def reason(self) -> str:
        """The reason of the rejection of the word."""
        return self.__reason


# TODO: improve automata for different use case, and to recognize possible errors
class Automata:
    OPERATIONS = dict([
        (Add.SYMBOL, Add),
        (Sub.SYMBOL, Sub),
        (Mult.SYMBOL, Mult),
        (Div.SYMBOL, Div)
    ])

    def __init__(self) -> None:
        self.__inner_stack = Stack()
        self.__inner_stack.push('$')
        self.__par_left = '('
        self.__par_right = ')'
        self.__alphabet_subset_01 = {
            self.__par_left,
            self.__par_right
        }
        self.__alphabet_subset_02 = (
            Expression
                .SYMBOLS
                .union(string.digits + '. ')
        )
        self.__alphabet = (
            self.__alphabet_subset_01
                .union(self.__alphabet_subset_02)
        )
        self.__parentheses_decoder = {}

    def __read(self, word: str, index: int) -> Result:
        """Read a word (or characters) and analyze if it should be `accepted` or `rejected`."""
        if word in self.alphabet:
            if word == self.__par_left:
                self.__inner_stack.push((word, index))
                return Acception(word, index)
            elif word == self.__par_right:
                pop = self.__inner_stack.pop()
                if pop is not None and pop != '$':
                    return Acception(word, index)
                else:
                    return Rejection(word, index, 'Unclosed Parentheses.')
            else:
                return Acception(word, index)
        else:
            return Rejection(word, index, 'Word not Recognized!')

    def analyze(self, sentence: str):
        """Analyzes the sentence and if the respects the rules of the grammar of this
        automata it will return a `Acception` object, else a `Rejection` will be returned.
        """
        if sentence.strip() == '':
            return Rejection('', 0, 'Empty Value.')
        for idx, char in enumerate(sentence.strip()):
            if isinstance(result := self.__read(char, idx), Rejection):
                return result
        pop = self.__inner_stack.pop()
        if pop is not None and pop != '$':
            return Rejection(*pop, 'Unclosed Parentheses')
        return Acception(char, idx)

    def parse(self, sentence: str):
        """Parses the sentence and returns the respective `Expression` object if all characters (words)
        of the sentence respect the gramatical rules of the automata, else it'll return a `Rejection` object.
        """
        if isinstance(res := self.analyze(sentence), Rejection):
            return res # If rejection return
        else: # Else, Acception, then parse it
            return self.__parse_expression(
                self.__encode_parentheses(sentence.strip())
            )

    def __search_parentheses_index(self, sentence: str):
        s = Stack()
        for i, char in enumerate(sentence):
            if char == self.__par_left:
                s.push(i)
            elif char == self.__par_right:
                return s.pop(), i
            else:
                continue
        return None

    def __encode_parentheses(self, sentence: str) -> str:
        """This function substitutes all parts on the sentence where is a parenthesis
        to an encoded value, which will be used after to decode and parse the expression
        in between the parentheses.
        """
        counter = 0
        new_sentence = sentence
        while (idx := self.__search_parentheses_index(new_sentence)):
            l, r = idx
            par = new_sentence[l:r+1]
            par_id = f'par{counter}'
            self.__parentheses_decoder[par_id] = par[1:-1]
            new_sentence = par_id.join(new_sentence.split(par))
            counter += 1
        return new_sentence

    def __parse_expression(self, sentence: str, **kwargs) -> Expression:
        """Inner method for recursively parsing expressions in a sentence."""
        sent_expr = sentence.strip()
        if sent_expr[0] in {Sub.SYMBOL, Add.SYMBOL}:
            sent_expr = '0 ' + sent_expr
        elif sent_expr[-1] == Add.SYMBOL:
            sent_expr = sent_expr + ' 0'
        used_symbols = set(self.OPERATIONS.keys()).intersection(sent_expr)
        for symbol in used_symbols:
            left, *right = sent_expr.split(symbol)
            if symbol == Sub.SYMBOL:
                new_right_sent_expr = Add.SYMBOL.join(right)
            else:
                new_right_sent_expr = symbol.join(right)
            return self.OPERATIONS[symbol](
                left = self.__parse_expression(
                    left.strip()
                ),
                right = self.__parse_expression(
                    new_right_sent_expr.strip(),
                    parentheses = symbol == Sub.SYMBOL
                ),
                parentheses = kwargs['parentheses'] if 'parentheses' in kwargs else False
            )
        return self.__get_expression_object(sentence)

    def __get_expression_object(self, word) -> Expression:
        """Return the respective Expression for each type of word."""
        if isinstance(word, Expression):
            return word
        elif word in self.__parentheses_decoder:
            return self.__parse_expression(
                self.__parentheses_decoder[word].strip(),
                parentheses=True
            )
        else:
            return Const(word)

    @property
    def alphabet(self):
        return self.__alphabet
