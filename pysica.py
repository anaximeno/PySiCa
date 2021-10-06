from time import sleep
from functs import *
import argparse
import sys
import os


DEBUG = False


def clear(force_clear: bool = False):
    """Clear the Console"""
    if not DEBUG or force_clear is True:
        os.system('clear')
    return not DEBUG or force_clear


def enterpoint(text: str = None):
    sys.stdout.write("[Hit Enter to Continue]")
    sys.stdout.flush()
    sys.stdin.read(1)


def animate(string: str, secs: float = 0.1):
	for char in string:
		if char != '\n' and char != '\t':
			sleep(secs)
		sys.stdout.write(char)
		sys.stdout.flush()
	print('')	# Go to new line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', '--debug', action='store_true')
    args = parser.parse_args()
    DEBUG = args.debug

    clear()
    animate("\t\t Welcome to the Python Simple Calculator - PySiCa\n", 0.085 * int(not DEBUG))

    while True:
        print("What do you want to do ?\n")
        print("  a - Use the calculator for calcs without vars;")
        print("  b - Use the calculator for calcs with vars;")
        print("  q - Quit the program.")
        opt = input('\n> Your choise >> ').lower()

        if opt == 'a':
            clear()
            expr = eval_expr(input('> Your Expression >> '))
            print(f"\n = {expr.eval()}\n")
            enterpoint()
        elif opt == 'b':
            # TODO: create more operation when dealing with variables
            clear()
            env = None
            expr = eval_expr(input('> Your Expression >> '), vars_allowed=True)
            vars = expr.get_variables()

            if any(vars):
                print("\nWrite the values for the respective vars: ")
                env = {var: eval(input(f'{var}: ')) for var in vars}

            print(f"\n = {expr.eval(env)}\n")
            # print("Info: This option wasn't finished already, please choose another!")
            enterpoint()
            pass # TODO: Finish this section
        elif opt == 'q':
            clear()
            animate("PySiCa - Thank you for trying it!", 0.035 * int(not DEBUG))
            break
        else:
            print("Unknown Option, Please Try Again!")
            enterpoint()
        
        clear()

