"""Unit tests for PySiCa."""
from expressions import (
    BinaryOperation,
    Expression,
    Const,
    Mult,
    Var,
    Div,
    Add,
    Sub,
    expr,
)


def test_add():
    a = Add(3, 4)
    assert a.eval() == 7


def test_sub():
    s = Sub(-19, 43)
    assert s.eval() == -62

def test_times():
    t = Mult(6, 5)
    assert t.eval() == 30


def test_div():
    d = Div(9, 3)
    assert d.eval() == 3


def test_full_expr():
    expression = Add(Mult(8, Div(50, 25)), Sub(12, 8))
    assert expression.eval() == 20


def test_full_expression_with_vars():
    expression = Add(Mult('x', 'x'), Div(5, Sub('x', 'y')))
    env = {
        'x': 2,
        'y': 1
    }
    assert expression.eval(env) == 9


def test_parse_expression():
    assert expr('2 - 5 / 25 - 7 + 3').eval() == -2.2


def test_parse_with_vars():
    env = {
        'x': 3,
        'y': 12
    }
    assert expr('5 - x - 9 + y', allow_variables=True).eval(env) == 5


def test_parse_beginning_with_minus():
    assert expr('- 8 + 3').eval() == -5


def test_float_values():
    assert expr ('0.569') == 0.569


def test_values_beginning_with_zero():
    assert expr ('09').eval() == 9