"""

"""

import sys

# DEFINED_NODE_GENERATORS = {
#     'statelessdraw': lambda: CCombinator([
#         BCombinator([
#             BCombinator(),
#             BCombinator([
#                 BCombinator([Cons([0])]),
#                 CCombinator([
#                     BCombinator([
#                         BCombinator(),
#                         Cons(),
#                     ]),
#                     CCombinator([Cons(), Nil()])
#                 ])
#             ])
#         ]),
#         CCombinator([
#             BCombinator([
#                 Cons(),
#                 CCombinator([Cons(), Nil()])
#             ]),
#             Nil()
#         ])
#     ])
# }


def list_to_cons_str(l: list) -> str:
    ret = []
    for x in l:
        ret.append('ap ap cons')
        if isinstance(x, Node):
            ret.append(x.display())
        elif isinstance(x, int):
            ret.append(str(x))
        elif isinstance(x, list):
            ret.append(list_to_cons_str(x))
    ret.append('nil')
    return ' '.join(ret)


class Node:
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def apply(self, v):
        self.argv.append(v)
        return self

    def has_full_args(self):
        return len(self.argv) == self.argc

    def __str__(self):
        n_applied_args = len(self.argv)
        args = []
        if self.argv:
            args.append(', '.join([str(arg) for arg in self.argv]))
        if n_applied_args < self.argc:
            args.append(', '.join('?'*(self.argc - len(self.argv))))
        return '{}({})'.format(self.__class__.__name__, ', '.join(args))

    def __eq__(self, other):
        return type(self) == type(other) and self.argv == other.argv

    def display(self) -> str:
        ret = []
        for i in range(len(self.argv)):
            ret.append('ap')
        ret.append(self.__class__.__name__)
        for x in self.argv:
            if isinstance(x, Node):
                ret.append(x.display())
            elif isinstance(x, int):
                ret.append(str(x))
            elif isinstance(x, list):
                ret.append(list_to_cons_str(x))

        return ' '.join(ret)


class Inc(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return self.argv[0] + 1


class Dec(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return self.argv[0] - 1


class Add(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable):
            return Variable()
        return self.argv[0] + self.argv[1]


class Mul(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable):
            return Variable()
        return self.argv[0]*self.argv[1]


class Div(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        """整数除算
        """
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable):
            return Variable()
        if self.argv[0]*self.argv[1] < 0:
            return abs(self.argv[0])//abs(self.argv[1]) * -1
        else:
            return abs(self.argv[0])//abs(self.argv[1])


class Eq(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable):
            return Variable()
        return self.argv[0] == self.argv[1]


class Lt(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable):
            return Variable()
        return self.argv[0] < self.argv[1]


class Modulate(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return Modulate.modulate(self.argv[0])

    def modulate(v):
        if v == [Nil()]:
            return [0, 0]
        if isinstance(v, Nil):
            return Modulate.modulate_nil(v)
        elif isinstance(v, list):
            return Modulate.modulate_list(v)
        elif isinstance(v, int):
            return Modulate.modulate_int(v)
        else:
            print(v, file=sys.stderr)

    def modulate_int(v):
        if v == 0:
            return [0, 1, 0]
        ret = [0, 1] if v > 0 else [1, 0]
        binary = bin(v)[2+(v < 0):]
        l = len(binary)
        bitlen = 0 - -l//4*4
        ret += [1]*(bitlen//4) + [0]
        ret += [0]*(bitlen - l) + [int(c) for c in binary]
        return ret

    def modulate_list(v):
        if not v:
            return [0, 0]
        ret = []
        for e in v:
            ret.extend([1, 1])
            ret.extend(Modulate.modulate(e))
        ret.extend([0, 0])
        return ret

    def modulate_nil(nil):
        return [0, 0]


class Demodulate(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.i = 0

    def __call__(self):
        return self.demodulate(self.argv[0])
    
    def demodulate(self, a):
        if a[:2] == [0, 1] or a[:2] == [1, 0]:
            return self.demodulate_number(a) 

        ret = []
        self.i += 2 # 最初の [1, 1] を読み飛ばす
        while self.i < len(a):
            if a[self.i:self.i+2] == [1, 1]:
                ret.append(self.demodulate(a))
            elif a[self.i:self.i+2] == [0, 1] or a[self.i:self.i+2] == [1, 0]:
                ret.append(self.demodulate_number(a))
            else:
                assert False, "Unreachable"

            if a[self.i:self.i+2] == [0, 0]:
                self.i += 2
                break
            elif a[self.i:self.i+2] == [1, 1]:
                self.i += 2
        return ret
    
    def demodulate_number(self, a):
        if a == [0, 1, 0]:
            return 0
        neg = a[self.i:self.i+2] == [1, 0]
        self.i += 2
        digit_num = 0
        while a[self.i] == 1:
            self.i += 1
            digit_num += 4
        v = 0
        k = 1
        for b in reversed(a[self.i+1:self.i+1+digit_num]):
            v += k*b
            k *= 2
        if neg:
            v *= -1
        self.i += 1 + digit_num
        return v

    def demodulate_list(self, a):
        pass
        


class Modem(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        # ap modem x0 = ap dem ap mod x0 = dem(mod(x0))
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return Demodulate([Modulate.modulate(self.argv[0])])()


# class F38(Node):
#     def __init__(self, argv=None):
#         self.argc = 2 # protorol, protorol(state, vector)
#         if argv:
#             self.argv = argv[:]
#         else:
#             self.argv = []
#
#     def __call__(self):
#         if len(self.argv) < self.argc:
#             return self
#         if isinstance(self.argv[0], Variable):
#             return Variable()
#         flag, newstate, data = argv[1]
#         if flag == 0:
#             return [Modem(newstate), Multipledraw(data)]
#         else:
#             return Interact(Modem(newstate), Send(data))
#
# class Interact(Node):
#     def __init__(self, argv=None):
#         self.argc = 2 # state, event
#         if argv:
#             self.argv = argv[:]
#         else:
#             self.argv = []
#
#     def __call__(self):
#         if len(self.argv) < self.argc:
#             return self
#         if isinstance(self.argv[0], Variable):
#             return Variable()
#         return F38('galaxy', 'protocol(state, vector)')


# class Send(Node):
#     def __init__(self, argv=None):
#         self.argc = 1
#         if argv:
#             self.argv = argv[:]
#         else:
#             self.argv = []
#
#     def __call__(self):
#         return self #TODO ?????

class Neg(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return -self.argv[0]


class Ap(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        # ap f x  =>  f(x)
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return self.argv[0].apply(self.argv[1])


class SCombinator(Node):
    def __init__(self, argv=None):
        self.argc = 3
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.is_combinator = True

    def __call__(self):
        # ap x y z  =>  x(z)(y(z))
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable) or isinstance(self.argv[2], Variable):
            return Variable()
        if not isinstance(self.argv[2], int) and not isinstance(self.argv[2], list):
            self.argv[2] = self.argv[2]()
        yz = self.argv[1].apply(self.argv[2])()
        xz = self.argv[0].apply(self.argv[2])
        return xz.apply(yz)()


class CCombinator(Node):
    def __init__(self, argv=None):
        self.argc = 3
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.is_combinator = True

    def __call__(self):
        # ap x y z  =>  x(z)(y)
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable) or isinstance(self.argv[1], Variable) or isinstance(self.argv[2], Variable):
            return Variable()
        if not isinstance(self.argv[2], int) and not isinstance(self.argv[2], list):
            self.argv[2] = self.argv[2]()
        self.argv[0].apply(self.argv[2]).apply(self.argv[1])
        return self.argv[0]()


class BCombinator(Node):
    def __init__(self, argv=None):
        self.argc = 3
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.is_combinator = True

    def __call__(self):
        # ap x y z  =>  x(y(z))
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        if not isinstance(self.argv[2], int) and not isinstance(self.argv[2], list):
            self.argv[2] = self.argv[2]()

        yz = self.argv[1].apply(self.argv[2])()
        xyz = self.argv[0].apply(yz)
        return xyz()


class TrueCombinator(Node):
    """True or K Combinator
    """

    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.is_combinator = True

    def __call__(self):
        # 引数がない場合はTrue
        if len(self.argv) == 0:
            return TrueCombinator()
        # 引数があればK Combinator
        if not isinstance(self.argv[0], int) and not isinstance(self.argv[0], list):
            self.argv[0] = self.argv[0]()
        return self.argv[0]


class FalseCombinator(Node):
    """False or Combinator
    """

    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.is_combinator = True

    def __call__(self):
        # 引数がない場合はFalse
        if len(self.argv) == 0:
            return FalseCombinator()
        if len(self.argv) < self.argc:
            return self
        # 引数があればCombinator
        if not isinstance(self.argv[1], int) and not isinstance(self.argv[1], list):
            self.argv[1] = self.argv[1]()
        return self.argv[1]


class ICombinator(Node):
    """Constant Combinator
    """

    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []
        self.is_combinator = True

    def __call__(self):
        # i(x) = x
        if len(self.argv) < self.argc:
            return self
        return self.argv[0]


class Pwr2(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return pow(2, self.argv[0])


class Cons(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[-1], Nil):
            if isinstance(self.argv[0], Nil):
                return Nil()
            return self.argv[:-1]
        if isinstance(self.argv[1], int) or isinstance(self.argv[1], Variable):
            self.argv[1] = [self.argv[1]]
        return [self.argv[0]] + self.argv[1]

    def _add__(self, other):
        if not self.argv and not other.argv:
            assert False, "unreachable"
        if not self.argv:
            return Cons([other.argv])
        if not other.argv:
            return Cons([self.argv])
        return Cons([self.argv + other.argv])

    def __getitem__(self, index):
        assert index < len(self.argv)
        return self.argv[index]


class Car(Node):
    """Car or Head
    """

    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        # TODO: impl for `ap car x2   =   ap x2 t`
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            self.argv[0] = [self.argv[0]]
        assert isinstance(self.argv[0], list)
        return self.argv[0][0]


class Cdr(Node):
    """ Cdr or Tail
    """

    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        # TODO: impl for `ap car x2   =   ap x2 f`
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            self.argv[0] = [self.argv[0]]
        assert isinstance(self.argv[0], list)
        return self.argv[0][-1]


class Nil(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if self.argv:
            return TrueCombinator()
        else:
            return Nil()


class IsNil(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Variable):
            return Variable()
        return TrueCombinator() if isinstance(self.argv[0], Nil) else FalseCombinator()


class Variable(Node):
    def __init__(self, argv=None):
        self.argc = 0
        self.argv = []

    def __call__(self):
        return self


class Vec(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return Cons(self.argv)()


class ParenOpen(Node):
    def __init__(self, argv=None):
        self.argc = 0
        self.argv = []

    def __call__(self):
        return self


class ParenClose(Node):
    def __init__(self, argv=None):
        self.argc = 0
        self.argv = []

    def __call__(self):
        return self


class Comma(Node):
    def __init__(self, argv=None):
        self.argc = 0
        self.argv = []

    def __call__(self):
        return self


class If0(Node):
    def __init__(self, argv=None):
        self.argc = 3
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        return self.argv[1] if self.argv[0] == 0 else self.argv[2]


class Picture:
    def __init__(self, dots=None):
        self.dots = set()
        if dots:
            for x, y in dots:
                self.dots.add((x, y))

    def add_dot(self, x, y):
        self.dots.add((x, y))

    def __call__(self):
        return self.dots


class Draw(Node):
    """
    Args:
        argv[0]: List<Vec<(int, int)>>
    """

    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        pic = Picture()
        for dot in self.argv[0]:
            dot = dot()
            pic.add_dot(dot[0], dot[1])
        return pic


class MultipleDraw(Node):
    """
    Args:
        argv[0]: List<List<Vec<(int, int)>>>
    """

    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < self.argc:
            return self
        if isinstance(self.argv[0], Nil):
            return []
        return [Draw(dots) for dots in self.argv[0]]


class Program:
    def __init__(self, nodes):
        self.nodes = nodes
        self.n = len(nodes)

    def __str__(self):
        return '=== PROGRAM BEGIN ===\n{}\n=== PROGRAM END ==='.format('\n'.join([str(node) for node in self.nodes]))

    def eval(self):
        """プログラムを実行する。
        """
        self.i = 0
        node = self._recursive_eval()
        return node if isinstance(node, int) or isinstance(node, list) else node()

    def _recursive_eval(self):
        if not isinstance(self.nodes[self.i], Ap):
            self.i += 1
            return self.nodes[self.i-1]
        args_num = 0
        while isinstance(self.nodes[self.i], Ap):
            args_num += 1
            self.i += 1
        op = self.nodes[self.i]
        self.i += 1
        if isinstance(op, Draw):  # ap draw ( ... ) に対応
            assert isinstance(self.nodes[self.i], ParenOpen)
            self.i += 1
            draw_args = []
            if isinstance(self.nodes[self.i], ParenClose):
                self.i += 1
            else:
                while 1:
                    draw_args.append(self._recursive_eval())
                    self.i += 1
                    if isinstance(self.nodes[self.i-1], ParenClose):
                        break
            op.apply(draw_args)
        else:
            for _ in range(args_num):
                op.apply(self._recursive_eval())
        return op() if op.has_full_args() else op


def parse(tokens):
    nodes = []
    for t in tokens:
        if t == 'inc':
            nodes.append(Inc())
        elif t == 'dec':
            nodes.append(Dec())
        elif t == 'add':
            nodes.append(Add())
        elif t == 'mul':
            nodes.append(Mul())
        elif t == 'div':
            nodes.append(Div())
        elif t == 'eq':
            nodes.append(Eq())
        elif t == 'lt':
            nodes.append(Lt())
        elif t == 'neg':
            nodes.append(Neg())
        elif t == 'ap':
            nodes.append(Ap())
        elif t == 's':
            nodes.append(SCombinator())
        elif t == 'c':
            nodes.append(CCombinator())
        elif t == 'b':
            nodes.append(BCombinator())
        elif t == 't':
            nodes.append(TrueCombinator())
        elif t == 'f':
            nodes.append(FalseCombinator())
        elif t == 'i':
            nodes.append(ICombinator())
        elif t == 'pwr2':
            nodes.append(Pwr2())
        elif t == 'cons':
            nodes.append(Cons())
        elif t == 'car':
            nodes.append(Car())
        elif t == 'cdr':
            nodes.append(Cdr())
        elif t == 'nil':
            nodes.append(Nil())
        elif t == 'isnil':
            nodes.append(IsNil())
        elif t == 'mod':
            nodes.append(Modulate())
        elif t == 'dem':
            nodes.append(Demodulate())
        elif t == 'vec':
            nodes.append(Vec())
        elif t == 'draw':
            nodes.append(Draw())
        elif t == '(':
            nodes.append(ParenOpen())
        elif t == ')':
            nodes.append(ParenClose())
        elif t == ',':
            nodes.append(Comma())
        elif t.startswith(':') or t.startswith('x'):
            nodes.append(Variable())
        elif t == 'send':
            nodes.append(None)
        # elif t == 'checkerboard':
        #     nodes.append(None)
        elif t == 'multipledraw':
            nodes.append(MultipleDraw())
        elif t == 'if0':
            nodes.append(If0())
        # elif t == 'modem':
        #     nodes.append(Modem())
        # elif t == 'interact':
        #     nodes.append(Interact())
        # elif t == 'f38':
        #     nodes.append(F38())
        # elif t == 'statelessdraw':
        #     nodes.append(DEFINED_NODE_GENERATORS[t]())

        else:
            # number
            nodes.append(int(t))

    return Program(nodes)


def lex(s):
    return s.split()


def execute(source: str) -> list:
    tokens = lex(source)
    program = parse(tokens)
    return program.eval()


def main():
    # example input: ap ap add -2 ap neg 7
    # example output: -9
    s = input()
    tokens = lex(s)
    print(tokens, file=sys.stderr)
    program = parse(tokens)
    print(program, file=sys.stderr)
    result = program.eval()
    print(result)


if __name__ == "__main__":
    main()
