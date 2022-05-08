import string

class Token:
    counter = 0
    TYPE: str
    
    def __init__(self, word: str) -> None:
        self._word = word
        self._id = hex(Token.counter)
        Token.counter += 1

    def __str__(self) -> str:
        return f"<{self.TYPE} tk{self.id}, {self.word!r}>"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def word(self) -> str:
        return self._word
    
    @property
    def id(self) -> int:
        return self._id

class IdentifierToken(Token):
    TYPE: str = "IDENTIFIER"

class NumberToken(Token):
    TYPE: str = "NUMBER"

class SignalToken(Token):
    TYPE: str = "SIGNAL"

class ParenthesesToken(Token):
    TYPE: str = "PARENTHESES"

class UnknownToken(Token):
    TYPE: str = "UNKNOWN"

class Scanner:

    def __init__(self, sentence: str) -> None:
        self._sentence = sentence
        self._dictionary: dict = {
            'identifiers': (set(string.ascii_letters), IdentifierToken),
            'numbers': (set(string.digits), NumberToken),
            'signals': (set('+-*/'), SignalToken),
            'parentheses': (set('()'), ParenthesesToken)}
        self._tokens: list = None

    def _tokenize(self, word: str) -> Token:
        token: Token = None
        for term_set, token_class in self._dictionary.values():
            intersection: set = term_set.intersection(word)
            if set(word).issubset(intersection):
                token = token_class(word)
                break
        else:
            token = UnknownToken(word=word)
        return token

    def lazy_tokens(self):
        splitted_sentence = self._sentence.split(' ')
        for item in splitted_sentence:
            token = self._tokenize(item)
            yield token

    def tokens(self) -> list:
        split_sent = self._sentence.split(' ')
        tokens = [self._tokenize(word) for word in split_sent]
        return tokens
