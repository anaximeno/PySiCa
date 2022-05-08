from scanner import *
from backend import Stack
from backend import Expression
from backend import EOF


class Parser:

    def __init__(self, sentence: str) -> None:
        self._sentence = sentence
        self._scanner = Scanner(sentence=sentence)
        self._tokens = self._scanner.lazy_tokens()
        self._expr: Expression = None
        self._stack = Stack()
        self._stack.put(EOF)
