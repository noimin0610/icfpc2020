"""
Usage:
    $ python -m unittest tests
"""

import unittest
from app.interpreter import *


class TestInc(unittest.TestCase):
    def test_simple(self):
        inc = Inc([1])
        self.assertEqual(inc(), 2)
        inc = Inc()
        inc.apply(-1)
        self.assertEqual(inc(), 0)


class TestDec(unittest.TestCase):
    def test_simple(self):
        dec = Dec([1])
        self.assertEqual(dec(), 0)
        dec = Dec([0])
        self.assertEqual(dec(), -1)
        dec = Dec([23])
        self.assertEqual(dec(), 22)


class TestAdd(unittest.TestCase):
    def test_simple(self):
        add = Add([1, 2])
        self.assertEqual(add(), 3)
        add = Add([2, 1])
        self.assertEqual(add(), 3)
        add = Add([0, 1])
        self.assertEqual(add(), 1)
        add = Add([3, 5])
        self.assertEqual(add(), 8)


class TestMul(unittest.TestCase):
    def test_simple(self):
        mul = Mul([4, 2])
        self.assertEqual(mul(), 8)
        mul = Mul([2, 4])
        self.assertEqual(mul(), 8)
        mul = Mul([3, -2])
        self.assertEqual(mul(), -6)
        mul = Mul([1, 0])
        self.assertEqual(mul(), 0)
        mul = Mul([6, 1])
        self.assertEqual(mul(), 6)


class TestDiv(unittest.TestCase):
    def test_simple(self):
        div = Div([4, 2])
        self.assertEqual(div(), 2, str(div))
        div = Div([4, 3])
        self.assertEqual(div(), 1, str(div))
        div = Div([4, 4])
        self.assertEqual(div(), 1, str(div))
        div = Div([4, 5])
        self.assertEqual(div(), 0, str(div))
        div = Div([6, -2])
        self.assertEqual(div(), -3, str(div))
        div = Div([5, 3])
        self.assertEqual(div(), 1, str(div))
        div = Div([5, -3])
        self.assertEqual(div(), -1, str(div))
        div = Div([-5, 3])
        self.assertEqual(div(), -1, str(div))
        div = Div([-5, -3])
        self.assertEqual(div(), 1, str(div))


class TestEq(unittest.TestCase):
    def test_simple(self):
        eq = Eq([0, -2])
        self.assertEqual(eq(), False, str(eq))
        eq = Eq([-4, -2])
        self.assertEqual(eq(), False, str(eq))
        eq = Eq([-2, -2])
        self.assertEqual(eq(), True, str(eq))
        eq = Eq([1, 1])
        self.assertEqual(eq(), True, str(eq))


class TestLt(unittest.TestCase):
    def test_simple(self):
        lt = Lt([0, -1])
        self.assertEqual(lt(), False, str(lt))
        lt = Lt([0, 0])
        self.assertEqual(lt(), False, str(lt))
        lt = Lt([0, 1])
        self.assertEqual(lt(), True, str(lt))
        lt = Lt([1, 2])
        self.assertEqual(lt(), True, str(lt))
        lt = Lt([-19, -20])
        self.assertEqual(lt(), False, str(lt))
        lt = Lt([-20, -20])
        self.assertEqual(lt(), False, str(lt))
        lt = Lt([-21, -20])
        self.assertEqual(lt(), True, str(lt))


class TestNeg(unittest.TestCase):
    def test_simple(self):
        neg = Neg([0])
        self.assertEqual(neg(), 0)
        neg = Neg([1])
        self.assertEqual(neg(), -1)
        neg = Neg([-1])
        self.assertEqual(neg(), 1)
        neg = Neg([2])
        self.assertEqual(neg(), -2)


class TestSCombinator(unittest.TestCase):
    def test_simple(self):
        s = SCombinator([Add(), Inc(), 1])
        self.assertEqual(s(), 3, str(s))
        s = SCombinator([Mul(), Add([1]), 6])
        self.assertEqual(s(), 42, str(s))


class TestEval(unittest.TestCase):
    def test_only_number(self):
        program = Program([2])
        self.assertEqual(program.eval(), 2, str(program))

    def test_single_ap(self):
        program = Program([Ap(), Add(), -2, 12])
        self.assertEqual(program.eval(), 10, str(program))

    def test_multi_ap(self):
        program = Program([Ap(), Ap(), Add(), -2, Ap(), Neg(), 5])
        self.assertEqual(program.eval(), -7, str(program))

        program = Program([Ap(), Ap(), Lt(), -2, Ap(), Ap(), Mul(), 5, -1])
        self.assertEqual(program.eval(), False, str(program))

        program = Program([Ap(), Ap(), Eq(), -5, Ap(), Ap(),
                           Mul(), Ap(), Inc(), 4, Ap(), Dec(), 0])
        self.assertEqual(program.eval(), True, str(program))

    def test_s_combinator(self):
        program = Program([Ap(), Ap(), Ap(), SCombinator(), Add(), Inc(), 1])
        self.assertEqual(program.eval(), 3, str(program))
        program = Program(
            [Ap(), Ap(), Ap(), SCombinator(), Mul(), Ap(), Add(), 1, 6])
        self.assertEqual(program.eval(), 42, str(program))

# class Test(unittest.TestCase):
#     def test_simple(self):
#         self.assertEqual((),)
