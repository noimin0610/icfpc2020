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

    def test_not_determined_nodes(self):
        eq = Eq([Ap(), Ap()])
        self.assertEqual(eq(), True, str(eq))
        eq = Eq([Ap(), Inc()])
        self.assertEqual(eq(), False, str(eq))


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


class TestModulate(unittest.TestCase):
    def test_simple(self):
        mod = Modulate([0])
        self.assertEqual(mod(), [0,1,0], str(mod))
        mod = Modulate([1])
        self.assertEqual(mod(), [0,1,1,0,0,0,0,1], str(mod))
        mod = Modulate([-1])
        self.assertEqual(mod(), [1,0,1,0,0,0,0,1], str(mod))
        mod = Modulate([2])
        self.assertEqual(mod(), [0,1,1,0,0,0,1,0], str(mod))
        mod = Modulate([-2])
        self.assertEqual(mod(), [1,0,1,0,0,0,1,0], str(mod))
        mod = Modulate([16])
        self.assertEqual(mod(), [0,1,1,1,0,0,0,0,1,0,0,0,0], str(mod))
        mod = Modulate([-16])
        self.assertEqual(mod(), [1,0,1,1,0,0,0,0,1,0,0,0,0], str(mod))
        mod = Modulate([255])
        self.assertEqual(mod(), [0,1,1,1,0,1,1,1,1,1,1,1,1], str(mod))
        mod = Modulate([-255])
        self.assertEqual(mod(), [1,0,1,1,0,1,1,1,1,1,1,1,1], str(mod))
        mod = Modulate([256])
        self.assertEqual(mod(), [0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0], str(mod))
        mod = Modulate([-256])
        self.assertEqual(mod(), [1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0], str(mod))


class TestDemodulate(unittest.TestCase):
    def test_simple(self):
        dem = Demodulate([[0,1,0]])
        self.assertEqual(dem(), 0, str(dem))
        dem = Demodulate([[0,1,1,0,0,0,0,1]])
        self.assertEqual(dem(), 1, str(dem))
        dem = Demodulate([[1,0,1,0,0,0,0,1]])
        self.assertEqual(dem(), -1, str(dem))
        dem = Demodulate([[0,1,1,0,0,0,1,0]])
        self.assertEqual(dem(), 2, str(dem))
        dem = Demodulate([[1,0,1,0,0,0,1,0]])
        self.assertEqual(dem(), -2, str(dem))
        dem = Demodulate([[0,1,1,1,0,0,0,0,1,0,0,0,0]])
        self.assertEqual(dem(), 16, str(dem))
        dem = Demodulate([[1,0,1,1,0,0,0,0,1,0,0,0,0]])
        self.assertEqual(dem(), -16, str(dem))
        dem = Demodulate([[0,1,1,1,0,1,1,1,1,1,1,1,1]])
        self.assertEqual(dem(), 255, str(dem))
        dem = Demodulate([[1,0,1,1,0,1,1,1,1,1,1,1,1]])
        self.assertEqual(dem(), -255, str(dem))
        dem = Demodulate([[0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0]])
        self.assertEqual(dem(), 256, str(dem))
        dem = Demodulate([[1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0]])
        self.assertEqual(dem(), -256, str(dem))


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


class TestCCombinator(unittest.TestCase):
    def test_simple(self):
        s = SCombinator([Add(), Inc(), 1])
        self.assertEqual(s(), 3, str(s))
        s = SCombinator([Mul(), Add([1]), 6])
        self.assertEqual(s(), 42, str(s))


class TestCCombinator(unittest.TestCase):
    def test_simple(self):
        c = CCombinator([Add(), 1, 2])
        self.assertEqual(c(), 3, str(c))
        c = CCombinator([Div(), 1, 2])
        self.assertEqual(c(), 2, str(c))


class TestBCombinator(unittest.TestCase):
    def test_simple(self):
        b = BCombinator([Inc(), Dec(), 0])
        self.assertEqual(b(), 0, str(b))


class TestTrueCombinator(unittest.TestCase):
    def test_simple(self):
        k = TrueCombinator([1, 5])
        self.assertEqual(k(), 1, str(k))
        k = TrueCombinator([TrueCombinator(), 1])
        self.assertEqual(k(), TrueCombinator(), str(k))


class TestFalseCombinator(unittest.TestCase):
    def test_simple(self):
        k = FalseCombinator([1, 5])
        self.assertEqual(k(), 5, str(k))


class TestICombinator(unittest.TestCase):
    def test_simple(self):
        i = ICombinator([1])
        self.assertEqual(i(), 1, str(i))
        i = ICombinator([ICombinator()])
        self.assertEqual(i(), ICombinator(), str(i))
        i = ICombinator([Add()])
        self.assertEqual(i(), Add(), str(i))


class TestPwr2(unittest.TestCase):
    def test_simple(self):
        p = Pwr2([1])
        self.assertEqual(p(), 2, str(p))
        p = Pwr2([0])
        self.assertEqual(p(), 1, str(p))
        p = Pwr2([8])
        self.assertEqual(p(), 256, str(p))


class TestCons(unittest.TestCase):
    def test_simple(self):
        cons = Cons([1, [2]])
        self.assertEqual(cons(), [1, 2])
        cons = Cons([1, Nil()])
        self.assertEqual(cons(), [1])


class TestCar(unittest.TestCase):
    def test_simple(self):
        car = Car([[1, 2]])
        self.assertEqual(car(), 1)
        car = Car([[10]])
        self.assertEqual(car(), 10)


class TestCdr(unittest.TestCase):
    def test_simple(self):
        cdr = Cdr()
        cdr.apply([1, 2])
        self.assertEqual(cdr(), 2)
        cdr = Cdr([[10]])
        self.assertEqual(cdr(), 10)


class TestNil(unittest.TestCase):
    def test_simple(self):
        nil = Nil()
        self.assertEqual(nil(), Nil())
        nil = Nil([1])
        self.assertEqual(nil(), TrueCombinator())


class TestIsNil(unittest.TestCase):
    def test_simple(self):
        isnil = IsNil([Nil()])
        self.assertEqual(isnil(), TrueCombinator())
        isnil = IsNil([Cons([1, 2])])
        self.assertEqual(isnil(), FalseCombinator())


class TestVec(unittest.TestCase):
    def test_simple(self):
        vec = Vec()
        self.assertEqual(vec(), Cons())
        argv = [1, 2]
        vec = Vec(argv)
        self.assertEqual(vec(), Cons(argv))
        argv = [1, Nil()]
        vec = Vec(argv)
        self.assertEqual(vec(), Cons(argv))


class TestEval(unittest.TestCase):
    def test_only_number(self):
        program = Program([2])
        self.assertEqual(program.eval(), 2, str(program))

    def test_single_ap(self):
        program = Program([Ap(), Ap(), Add(), -2, 12])
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

    def test_modulate_demodulate(self):
        program = Program([Ap(), Demodulate(), Ap(), Modulate(), 999])
        self.assertEqual(program.eval(), 999, str(program))
        program = Program([Ap(), Modulate(), Ap(), Demodulate(), [0,1,1,0,0,1,0,1]])
        self.assertEqual(program.eval(), [0,1,1,0,0,1,0,1], str(program))

# class Test(unittest.TestCase):
#     def test_simple(self):
#         self.assertEqual((),)
