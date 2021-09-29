from time import sleep
from functs import *
import sys
import os


DebugMode = True


def animate(string: str, secs: float = 0.1):
	for char in string:
		if char != '\n' and char != '\t':
			sleep(secs)
		sys.stdout.write(char)
		sys.stdout.flush()
	print('')	# Go to new line


if __name__ == '__main__':
    animate("\t\t*** Python Simple Calculator ***\n", 0.085 * int(not DebugMode))

    while True:
        print("What do you want to do ?\n")
        print("  a) Use the calculator for calcs without vars;")
        print("  b) Use the calculator for calcs with vars;")
        print("  q) Quit the program.")
        opt = input('\n> Your choise >> ').lower()

        if opt == 'a':
            os.system('clear')
            expr = eval_expr(input('> Your Expression >> '))
            print(f"\n{expr} = {expr.eval()}")
        elif opt == 'b': ## TODO: Finish the program
            pass
        elif opt == 'q':
            pass
        else:
            print("Unknown Option, Please Try Again!")
        
        break

