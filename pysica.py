from collections import deque
from time import sleep
from expressions import expr
import argparse
import sys
import os


class PySiCa(object):
    _NAME: str = 'PySiCa'

    def __init__(self, args, debug: bool = False) -> None:
        super(PySiCa, self).__init__()
        # TODO: implement stack
        self._expr_stack = deque()
        self._args = args
        self._debug = debug
        self._out = sys.stdout
        self._in = sys.stdin

    def enterpoint(self, message: str = "[Click Enter]"):
        self._out.write(f"{self._NAME}: {message}")
        self._out.flush()
        self._in.read(1)
    
    def animate(self, string: str, secs: float = 0.05):
        for char in string:
            if char != '\n' and char != '\t':
                sleep(secs)
            self._out.write(char)
            self._out.flush()
        print('')

    def clear(self, force: bool = False) -> bool:
        """Clear the Console"""
        if not self._debug or force is True:
            os.system('clear')
        return not self._debug or force

    def talk(self, message, animation_time: float = 0.05) -> None:
        self.animate(f"{self._NAME}: {message}", animation_time * int(not self._debug))

    def run(self):
        if self._debug is True:
            self.talk('Debug Mode\n')
        else:
            self.clear()
            self.talk("Welcome to the Python Simple Calculator! \n", 0.025)
        while True:
            self.talk("What do you want to do ?\n")
            print("  a -> Use the calculator for calcs without vars(e.g. 30 * 3 - 12 / 4 );")
            print("  b -> Use the calculator for calcs with vars(e.g. k - k / 4 );")
            print("  q -> Quit the program.")
            opt = input('\n> ').lower()
            if opt == 'a':
                self.clear()
                entry = input((' .' * 5) + '\r')
                print(f"\n = {expr(entry).eval()}\n")
                self.enterpoint()
            elif opt == 'b':
                self.clear()
                expression = expr(input((' .' * 10) + '\r'), allow_variables=True)
                variables = expression.get_variables()

                env = None
                if any(variables):
                    print("\nWrite the value of: ")
                    env = {var: eval(input(f'\t -> {var}: ')) for var in variables}

                print(f"\n = {expression.eval(env)}\n")
                self.enterpoint()
            elif opt == 'q':
                self.clear()
                self.talk("Looking forward for the next try ;)", 0.030)
                break
            else:
                self.talk("Unknown Option, Try Again!")
                self.enterpoint()
            self.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('PySiCa')
    parser.add_argument('-D', '--debug', action='store_true')
    args = parser.parse_args()
    app = PySiCa(args, args.debug)
    app.run()
