from collections import deque
from typing import Any


class Stack(object):

    def __init__(self, limit: int = None, input_type=None) -> None:
        if type(limit) is int or limit is None:
            self._limit = limit
        else:
            raise TypeError('Limit if given must be an integer value!')
        self._input_type = input_type
        self._stack_block = deque(maxlen=self._limit)
        self._top = -1

    @property
    def limit(self) -> int:
        return self._limit

    def number_of_elements(self) -> int:
        return self._top + 1

    def _walk(self, step: int) -> bool:
        prev_top = self._top
        if type(step) is int:
            if step == -1:
                self._top += step if not self.isempty() else 0
            elif step == 1:
                self._top += step if not self.isfull() else 0
            else:
                raise ValueError(
                    'The value of the parameter inc must be -1 or 1'
                )
        else:
            raise TypeError('The type of the inc value must be int!')
        return not self._top == prev_top

    def isfull(self) -> bool:
        return self.limit == self.number_of_elements if self.limit is not None else False

    def isempty(self) -> bool:
        return not bool(self.number_of_elements)

    def push(self, value: Any) -> bool:
        if not self.isfull():
            if self._input_type is None or type(value) is self._input_type:
                self._stack_block.append(value)
            else:
                raise TypeError(
                    f'This stack only acepts inputs of the type {str(self._input_type)}')
        return self._walk(1)

    def pop(self) -> Any:
        if not self.isempty():
            self._walk(-1)
            out = self._stack_block.pop()
            return out
        return None
