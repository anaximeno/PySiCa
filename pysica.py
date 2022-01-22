from backend import (
    Automata,
    Rejection,
    Queue
)

import time
import sys, os
import argparse
import termcolor


__version__ = '2.0.1-beta'


PRETTY_OUTPUT_FORMAT_0 = f"""
 PySiCa {__version__}
 
 Write an expression or 'q' to quit.

--------------------------------------
 
 [0] => """

PRETTY_OUTPUT_FORMAT_1 = """
 [1] %s

--------------------------------------
 
 [0] => """

PRETTY_OUTPUT_FORMAT_2 = """
 [2] %s

 [1] %s

--------------------------------------
 
 [0] => """

PRETTY_OUTPUT_FORMAT_3 = """
 [3] %s

 [2] %s

 [1] %s

--------------------------------------
 
 [0] => """


class PySiCa(object):
    NAME = "PySiCa"

    OUTPUT_FORMAT = [
        PRETTY_OUTPUT_FORMAT_0,
        PRETTY_OUTPUT_FORMAT_1,
        PRETTY_OUTPUT_FORMAT_2,
        PRETTY_OUTPUT_FORMAT_3
    ]

    def __init__(self, debug: bool = False) -> None:
        super(PySiCa, self).__init__()
        self._debug_mode = debug
        self._out = sys.stdout
        self._in = sys.stdin
        self.automata = Automata()
        self._queue = Queue(3)

    def __str__(self) -> str:
        return f'Python Simple Calculator [{self.NAME}] {__version__}'

    def enterpoint(self, message: str = "[Click Enter]"):
        self._out.write(f"{self.NAME}: {message}")
        self._out.flush()
        self._in.read(1)

    def animate(self, string: str, secs: float = 0.05):
        skip_set = {'\n', '\t', '\a', '\r', '\b'}
        for char in string:
            if char not in skip_set:
                time.sleep(secs)
            self._out.write(char)
            self._out.flush()
        print('')

    def clear(self, force: bool = False) -> bool:
        """Clear the Console"""
        if not self._debug_mode or force is True:
            os.system('clear')
        return not self._debug_mode or force

    def talk(self, message, **kwargs) -> None:
        anim_time = 0
        if 'anim_time' in kwargs:
            anim_time = kwargs['anim_time']
        self.animate(f"\nPySiCa: {message}", anim_time)

    def run(self, tutorial: bool = False):
        self.talk("Welcome to the [Py]thon [Si]mple [Ca]lculator!", anim_time=0.04)
        time.sleep(0.5)
        self.clear()
        if tutorial is True:
            pass # TODO: create the tutorial section
        else:
            while True:
                user_sentence = self._show_output_and_get_input(pretty=True)
                if user_sentence.lower().strip() == 'q':
                    break
                res = self.automata.parse(user_sentence)
                if type(res) is Rejection:
                    if res.word == '': # Rejection by empty input
                        continue       # Ignore
                    formated_user_sentence = ''.join(
                        (
                            user_sentence[:res.index],
                            termcolor.colored(res.word, 'red'),
                            user_sentence[res.index + 1:]
                        )
                    )
                    output = f'{formated_user_sentence} -> {res.why}'
                else:
                    output = f'{user_sentence} = {res.eval()}'
                self._queue.enqueue(output)
            self.clear()
            self.talk("hope you liked it :)", anim_time=0.025)

    def _show_output_and_get_input(self, pretty: bool = True) -> str:
        self.clear()
        if pretty is True:
            user_input = input(
                self.OUTPUT_FORMAT[self._queue.lenght] % tuple(self._queue.list_all())
            )
        else:
            user_input = input("=> ")
        return user_input




if __name__ == '__main__':
    argparser = argparse.ArgumentParser(PySiCa.NAME)

    argparser.add_argument("--version",
        help="Display the version",
        action='version',
        version='%(prog)s {}'.format(__version__)
    )

    argparser.add_argument('-D', '--debug', action='store_true')

    args = argparser.parse_args()
    app = PySiCa(args.debug)
    app.run()
