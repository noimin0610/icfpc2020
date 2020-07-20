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
        self.assertEqual(mod(), [0, 1, 0], str(mod))
        mod = Modulate([1])
        self.assertEqual(mod(), [0, 1, 1, 0, 0, 0, 0, 1], str(mod))
        mod = Modulate([-1])
        self.assertEqual(mod(), [1, 0, 1, 0, 0, 0, 0, 1], str(mod))
        mod = Modulate([2])
        self.assertEqual(mod(), [0, 1, 1, 0, 0, 0, 1, 0], str(mod))
        mod = Modulate([-2])
        self.assertEqual(mod(), [1, 0, 1, 0, 0, 0, 1, 0], str(mod))
        mod = Modulate([16])
        self.assertEqual(mod(), [0, 1, 1, 1, 0, 0, 0,
                                 0, 1, 0, 0, 0, 0], str(mod))
        mod = Modulate([-16])
        self.assertEqual(mod(), [1, 0, 1, 1, 0, 0, 0,
                                 0, 1, 0, 0, 0, 0], str(mod))
        mod = Modulate([255])
        self.assertEqual(mod(), [0, 1, 1, 1, 0, 1, 1,
                                 1, 1, 1, 1, 1, 1], str(mod))
        mod = Modulate([-255])
        self.assertEqual(mod(), [1, 0, 1, 1, 0, 1, 1,
                                 1, 1, 1, 1, 1, 1], str(mod))
        mod = Modulate([256])
        self.assertEqual(mod(), [0, 1, 1, 1, 1, 0, 0,
                                 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], str(mod))
        mod = Modulate([-256])
        self.assertEqual(mod(), [1, 0, 1, 1, 1, 0, 0,
                                 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], str(mod))

    def test_modulate_nil(self):
        mod = Modulate([Nil()])
        self.assertEqual(mod(), [0, 0], str(mod))

    def test_modulate_list_contains_nil(self):
        mod = Modulate([[Nil(), Nil()]])
        self.assertEqual(mod(), [1, 1, 0, 0, 0, 0], str(mod))

    def test_modulate_list(self):
        mod = Modulate([[1, 2]])
        self.assertEqual(mod(), [
            1, 1,
            0, 1, 1, 0, 0, 0, 0, 1,
            1, 1,
            0, 1, 1, 0, 0, 0, 1, 0,
            0, 0
        ], str(mod))

    def test_modulate_tuple(self):
        mod = Modulate([(1, 2)])
        self.assertEqual(mod(), [
            1, 1, 
            0, 1, 1, 0, 0, 0, 0, 1, 
            0, 1, 1, 0, 0, 0, 1, 0, 
        ], str(mod))
        mod = Modulate([[1, 2, (3, 4)]])
        self.assertEqual(mod(), [
            1, 1, 
            0, 1, 1, 0, 0, 0, 0, 1, 
            1, 1, 
            0, 1, 1, 0, 0, 0, 1, 0,
            1, 1, 
            1, 1, 
            0, 1, 1, 0, 0, 0, 1, 1,
            0, 1, 1, 0, 0, 1, 0, 0,
            0, 0
        ], str(mod))

    def test_modulate_nested_list(self):
        mod = Modulate([[1, [2, 3], 4]])
        self.assertEqual(mod(), [
            1, 1,
            0, 1, 1, 0, 0, 0, 0, 1,
            1, 1,
            1, 1,
            0, 1, 1, 0, 0, 0, 1, 0,
            1, 1,
            0, 1, 1, 0, 0, 0, 1, 1,
            0, 0,
            1, 1,
            0, 1, 1, 0, 0, 1, 0, 0,
            0, 0
        ], str(mod))

    def test_modulate_list_program_contains_nil(self):
        program = Program([Ap(), Modulate(), Nil()])
        self.assertEqual(program.eval(), [0, 0], str(program))
        program = Program([Ap(), Modulate(), Ap(), Ap(), Cons(), Nil(), Nil()])
        self.assertEqual(program.eval(), [1, 1, 0, 0, 0, 0], str(program))

    def test_modulate_list_program_suddenly_end(self):
        program = Program([Ap(), Modulate(), Ap(), Ap(), Cons(), 1, 2])
        self.assertEqual(program.eval(), [
                         1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0], str(program))

    def test_modulate_list_program(self):
        program = Program([Ap(), Modulate(), Ap(), Ap(), Cons(), 0, Nil()])
        self.assertEqual(program.eval(), [1, 1, 0, 1, 0, 0, 0], str(program))
        program = Program([Ap(), Modulate(), Ap(), Ap(),
                           Cons(), 1, Ap(), Ap(), Cons(), 2, Nil()])
        self.assertEqual(program.eval(), [
                         1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0], str(program))
        program = Program([Ap(), Modulate(), [1, 2]])
        self.assertEqual(program.eval(), [
                         1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0], str(program))
        program = Program([Ap(), Modulate(), [1, [2, 3], 4]])
        self.assertEqual(program.eval(), [1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0,
                                          1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0], str(program))


class TestDemodulate(unittest.TestCase):
    def test_simple(self):
        dem = Demodulate([[0, 0]])
        self.assertEqual(dem(), None, str(dem))
        dem = Demodulate([[0, 1, 0]])
        self.assertEqual(dem(), 0, str(dem))
        dem = Demodulate([[0, 1, 1, 0, 0, 0, 0, 1]])
        self.assertEqual(dem(), 1, str(dem))
        dem = Demodulate([[1, 0, 1, 0, 0, 0, 0, 1]])
        self.assertEqual(dem(), -1, str(dem))
        dem = Demodulate([[0, 1, 1, 0, 0, 0, 1, 0]])
        self.assertEqual(dem(), 2, str(dem))
        dem = Demodulate([[1, 0, 1, 0, 0, 0, 1, 0]])
        self.assertEqual(dem(), -2, str(dem))
        dem = Demodulate([[0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]])
        self.assertEqual(dem(), 16, str(dem))
        dem = Demodulate([[1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]])
        self.assertEqual(dem(), -16, str(dem))
        dem = Demodulate([[0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
        self.assertEqual(dem(), 255, str(dem))
        dem = Demodulate([[1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
        self.assertEqual(dem(), -255, str(dem))
        dem = Demodulate(
            [[0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(dem(), 256, str(dem))
        dem = Demodulate(
            [[1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(dem(), -256, str(dem))

    def test_demodulate_list(self):
        dem = Demodulate([[
                         1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0]])
        self.assertEqual(dem(), [1, 2], str(dem))
        dem = Demodulate([[1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0,
                           1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]])
        self.assertEqual(dem(), [1, [2, 3], 4], str(dem))
        dem = Demodulate([[
            1, 1,
            0, 1, 1, 0, 0, 0, 0, 1,
            1, 1,
            0, 1, 1, 0, 0, 0, 1, 0,
            1, 1,
            0, 0,
            1, 1,
            0, 0,
            0, 0
        ]])
        self.assertEqual(dem(), [1, 2], str(dem))

    def test_demodulate_list_practical(self):
        param = '110110000111011000011111011110000100000000110101111011110001000000000110110000111011100100000000111101110000100001101110100000000011110110000111011000101101100011110110010000001111010111101110000100001101110100000000011111111011000011101011111011000011100011100011000011110100101111011000011101100010110110001111011001000011010110111001000000110110000100110000111111010110110000111110111000011100101100011000011110100101111011000011101100010110110001111011001000011010110111001000000110110000100110000000000'
        dem = Demodulate([[int(c) for c in param]])
        actual = dem()
        self.assertEqual(actual, [
            1,
            1,
            [
                256, 0, [512, 1, 64], [16, 128], [1, 2, 3, 4]
            ],
            [
                0,
                [16, 128],
                [
                    [[1, 0, [-28, 48], [0, 0], [1, 2, 3, 4], 0, 64, 1]],
                    [[0, 1, [28, -48], [0, 0], [1, 2, 3, 4], 0, 64, 1]]
                ]
            ]
        ], str(dem))


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

    def test_ignore_second_arg(self):
        k = TrueCombinator([1, Ap()])
        self.assertEqual(k(), 1, str(k))


class TestFalseCombinator(unittest.TestCase):
    def test_simple(self):
        k = FalseCombinator([1, 5])
        self.assertEqual(k(), 5, str(k))

    def test_ignore_first_arg(self):
        k = FalseCombinator([Inc(), 2])
        self.assertEqual(k(), 2, str(k))


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


class TestVariable(unittest.TestCase):
    def test_simple(self):
        variable = Variable()
        self.assertEqual(variable(), Variable())
        inc = Inc([Variable()])
        self.assertEqual(inc(), Variable())
        dec = Dec([Variable()])
        self.assertEqual(dec(), Variable())
        add = Add([Variable(), 2])
        self.assertEqual(add(), Variable())
        mul = Mul([Variable(), 2])
        self.assertEqual(mul(), Variable())
        div = Div([Variable(), 2])
        self.assertEqual(div(), Variable())
        eq = Eq([Variable(), 2])
        self.assertEqual(eq(), Variable())
        lt = Lt([Variable(), 2])
        self.assertEqual(lt(), Variable())
        # Modulate, Demodulate は考慮しない
        neg = Neg([Variable()])
        self.assertEqual(neg(), Variable())
        pwr2 = Pwr2([Variable()])
        self.assertEqual(pwr2(), Variable())
        isnil = IsNil([Variable()])
        self.assertEqual(isnil(), Variable())


class TestVec(unittest.TestCase):
    def test_simple(self):
        vec = Vec()
        self.assertEqual(vec(), Cons()())
        argv = [1, 2]
        vec = Vec(argv)
        self.assertEqual(vec(), Cons(argv)())
        argv = [1, Nil()]
        vec = Vec(argv)
        self.assertEqual(vec(), Cons(argv)())


class TestEval(unittest.TestCase):
    def test_only_number(self):
        program = Program([2])
        self.assertEqual(program.eval(), 2, str(program))

    def test_single_ap(self):
        program = Program([Ap(), Ap(), Add(), -2, 12])
        self.assertEqual(program.eval(), 10, str(program))
        program = Program([Ap(), Ap(), Add(), -2, Variable()])
        self.assertEqual(program.eval(), Variable(), program)

    def test_multi_ap(self):
        program = Program([Ap(), Ap(), Add(), -2, Ap(), Neg(), 5])
        self.assertEqual(program.eval(), -7, str(program))

        program = Program([Ap(), Ap(), Lt(), -2, Ap(), Ap(), Mul(), 5, -1])
        self.assertEqual(program.eval(), False, str(program))

        program = Program([Ap(), Ap(), Eq(), -5, Ap(), Ap(),
                           Mul(), Ap(), Inc(), 4, Ap(), Dec(), 0])
        self.assertEqual(program.eval(), True, str(program))

        program = Program([Ap(), Ap(), Add(), -2, Ap(), Neg(), Variable()])
        self.assertEqual(program.eval(), Variable(), program)

    def test_s_combinator(self):
        program = Program([Ap(), Ap(), Ap(), SCombinator(), Add(), Inc(), 1])
        self.assertEqual(program.eval(), 3, str(program))
        program = Program(
            [Ap(), Ap(), Ap(), SCombinator(), Mul(), Ap(), Add(), 1, 6])
        self.assertEqual(program.eval(), 42, str(program))
        program = Program(
            [Ap(), Ap(), Ap(), SCombinator(), Add(), Inc(), Variable()])
        self.assertEqual(program.eval(), Variable(), program)
        program = Program(
            [Ap(), Ap(), Ap(), SCombinator(), Add(), Variable(), 1])
        self.assertEqual(program.eval(), Variable(), program)
        program = Program(
            [Ap(), Ap(), Ap(), SCombinator(), Variable(), Inc(), 1])
        self.assertEqual(program.eval(), Variable(), program)

    def test_modulate_demodulate(self):
        program = Program([Ap(), Demodulate(), Ap(), Modulate(), 999])
        self.assertEqual(program.eval(), 999, str(program))
        program = Program(
            [Ap(), Modulate(), Ap(), Demodulate(), [0, 1, 1, 0, 0, 1, 0, 1]])
        self.assertEqual(program.eval(), [
                         0, 1, 1, 0, 0, 1, 0, 1], str(program))

    def test_true_combinator(self):
        program = Program(
            [Ap(), Ap(), TrueCombinator(), [1], Ap(), Inc(), 1])
        self.assertEqual(program.eval(), [1], str(program))

        program = Program(
            [Ap(),  TrueCombinator(), Add()])
        self.assertEqual(program.eval(), Add(), str(program))

        program = Program(
            [Ap(), Ap(), TrueCombinator(), [1], Ap(), Inc(), Variable()])
        self.assertEqual(program.eval(), [1], str(program))

        program = Program(
            [Ap(), Ap(), TrueCombinator(), Variable(), Ap(), Inc(), 1])
        self.assertEqual(program.eval(), Variable(), str(program))

    def test_false_combinator(self):
        program = Program(
            [Ap(), Ap(), FalseCombinator(), [1], Ap(), Inc(), 1])
        self.assertEqual(program.eval(), 2, str(program))

        program = Program(
            [Ap(), Ap(), FalseCombinator(), Add(), Ap(), Inc(), 1])
        self.assertEqual(program.eval(), 2, str(program))

        program = Program(
            [Ap(), Ap(), FalseCombinator(), [1], Ap(), Inc(), Variable()])
        self.assertEqual(program.eval(), Variable(), str(program))

        program = Program(
            [Ap(), Ap(), FalseCombinator(), Variable(), Ap(), Inc(), 1])
        self.assertEqual(program.eval(), 2, str(program))


class TestConvert(unittest.TestCase):
    def test_flat(self):
        ap_str = 'ap ap cons 1 ap ap cons 2 ap ap cons 3 nil'
        result = execute(ap_str)
        expected = [1, 2, 3]
        self.assertEqual(expected, result)
        redo = execute(list_to_cons_str(result))
        self.assertEqual(result, redo)

        expected = list_to_cons_str(result)
        actual = list_to_cons_str(redo)
        self.assertEqual(expected, actual)

    def test_nested(self):
        ap_str = 'ap ap cons 1 ap ap cons ap ap cons 2 ap ap cons 3 nil ap ap cons 4 nil'
        result = execute(ap_str)
        expected = [1, [2, 3], 4]
        self.assertEqual(expected, result)
        self.assertEqual(ap_str, list_to_cons_str(result))
        redo = execute(list_to_cons_str(result))

        redo = execute(list_to_cons_str(result))
        self.assertEqual(result, redo)

        expected = list_to_cons_str(result)
        actual = list_to_cons_str(redo)
        self.assertEqual(expected, actual)

    def test_simple(self):
        ap_str = 'ap ap cons 0 ap ap cons ap ap cons 0 ap ap cons ap ap cons 0 nil ap ap cons 0 ap ap cons nil nil ap ap cons ap ap cons ap ap cons ap ap cons -1 -3 ap ap cons ap ap cons 0 -3 ap ap cons ap ap cons 1 -3 ap ap cons ap ap cons 2 -2 ap ap cons ap ap cons -2 -1 ap ap cons ap ap cons -1 -1 ap ap cons ap ap cons 0 -1 ap ap cons ap ap cons 3 -1 ap ap cons ap ap cons -3 0 ap ap cons ap ap cons -1 0 ap ap cons ap ap cons 1 0 ap ap cons ap ap cons 3 0 ap ap cons ap ap cons -3 1 ap ap cons ap ap cons 0 1 ap ap cons ap ap cons 1 1 ap ap cons ap ap cons 2 1 ap ap cons ap ap cons -2 2 ap ap cons ap ap cons -1 3 ap ap cons ap ap cons 0 3 ap ap cons ap ap cons 1 3 nil ap ap cons ap ap cons ap ap cons -7 -3 ap ap cons ap ap cons -8 -2 nil ap ap cons nil nil nil'
        result = execute(ap_str)
        redo = execute(list_to_cons_str(result))
        self.assertEqual(result, redo)

        expected = list_to_cons_str(result)
        actual = list_to_cons_str(redo)
        self.assertEqual(expected, actual)

# class Test(unittest.TestCase):
#     def test_simple(self):
#         self.assertEqual((),)
