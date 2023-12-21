#from unittest import *
from .reverser import Reverse


def test_input_1():
    x = Reverse(1)
    assert x.value == -1


def test_input_2():
    y = Reverse(2)
    assert y.value == -2


def test_add_minus1_minus2():
    z = Reverse(1) + Reverse(2)
    assert z == 1


def test_sub_minus1_minus2():
    w = Reverse(1) - Reverse(2)
    assert w == -3
