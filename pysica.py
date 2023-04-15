from sys import stdout, stdin
from automata import Automata

from common import (
    Expression,
    Nothing,
    Rejection,
    Queue,
)

import os, time
import argparse
import termcolor


__version__ = '2.3.5-beta'


VIEW_01 = f"""
 PySiCa {__version__}

 Write an expression or 'q' to quit.

--------------------------------------

 [0] => """

VIEW_02 = """
 Write an expression or 'q' to quit.

 [1] %s

--------------------------------------

 [0] => """

VIEW_03 = """
 Write an expression or 'q' to quit.

 [2] %s

 [1] %s

--------------------------------------

 [0] => """

VIEW_04 = """
 Write an expression or 'q' to quit.

 [3] %s

 [2] %s

 [1] %s

--------------------------------------

 [0] => """


class PySiCa(object):
    VIEWS = [
        VIEW_01,
        VIEW_02,
        VIEW_03,
        VIEW_04
    ]

    def __init__(self, debug: bool = False) -> None:
        super(PySiCa, self).__init__()
        self.automata = Automata()
        self.output_queue = Queue(3)
        self._debug = debug

    def __str__(self) -> str:
        return f'Python Simple Calculator [PySiCa] {__version__}'

    def enterpoint(self, message: str = "[Click Enter]"):
        stdout.write(f"{self.NAME}: {message}")
        stdout.flush()
        stdin.read(1)

    def animate(self, string: str, secs: float = 0.05):
        skip_set = {'\n', '\t', '\a', '\r', '\b'}
        for char in string:
            if char not in skip_set:
                time.sleep(secs)
            stdout.write(char)
            stdout.flush()
        print('')

    def clear(self, force: bool = False) -> bool:
        """Clear the Console"""
        if not self._debug or force is True:
            os.system('clear')
        return not self._debug or force

    def talk(self, message, **kwargs) -> None:
        anim_time = 0
        if 'anim_time' in kwargs:
            anim_time = kwargs['anim_time']
        self.animate(f"\nPySiCa: {message}", anim_time * int(not self._debug))

    def run(self, tutorial: bool = False):
        self.talk("Welcome to the [Py]thon [Si]mple [Ca]lculator!", anim_time=0.04)
        time.sleep(0.5)
        self.clear()

        if tutorial is True:
            self._run_tutorial()
        else:
            self._run_calculator()

    def _run_calculator(self) -> None:
        while True:
            sentence = self._input(pretty=True).lower().strip()
            if sentence == '':
                continue
            elif sentence == 'q' or sentence == 'quit':
                break
            result = self.automata.parse(sentence)
            output = self._process_automata_result(sentence, result)
            self.output_queue.enqueue(output)
        self.clear()
        self.talk("hope you liked it :)", anim_time=0.025)

    def _run_tutorial(self) -> None:
        pass # TODO

    def _input(self, pretty: bool = True) -> str:
        self.clear()
        output_format = "=> "
        if pretty is True:
            index = self.output_queue.lenght
            elements = tuple(self.output_queue.list())
            output_format = self.VIEWS[index] % elements
        stdout.flush()
        return input(output_format)

    def _process_automata_result(self, sentence: str, result: Expression | Rejection) -> str:
        output = ''
        if type(result) is Rejection:
            new_sentence = ''.join((
                sentence[:result.index],
                termcolor.colored(result.word, 'red'),
                sentence[result.index + 1:]
            ))
            output = f'{new_sentence} -> {result.reason}'
        else:
            op = result.eval()
            suffix = f'-> {op.cause}' if isinstance(op, Nothing) else f'= {op.value}'
            output = f'{sentence} {suffix}'
        return output


if __name__ == '__main__':
    argparser = argparse.ArgumentParser("PySiCa")

    argparser.add_argument("--version",
        help="Display the version",
        version=f'%(prog)s {__version__}',
        action='version'
    )

    argparser.add_argument('-D', '--debug', action='store_true')

    args = argparser.parse_args()

    app = PySiCa(args.debug)
    app.run()
