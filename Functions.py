from math import trunc


def adicao(x, y):
    if (x + y) % 1 == 0:
        return trunc(x + y)
    else:
        return x + y


def subtracao(x, y):
    if (x - y) % 1 == 0:
        return trunc(x - y)
    else:
        return x - y


def multiplicacao(x, y):
    if (x * y) % 1 == 0:
        return trunc(x * y)
    else:
        return x * y


def divisao(x, y):
    if (x / y) % 1 == 0:
        return trunc(x / y)
    else:
        return x / y


def potencia(x, y):
    if pow(x, y) % 1 == 0:
        return trunc(pow(x, y))
    else:
        return pow(x, y)

