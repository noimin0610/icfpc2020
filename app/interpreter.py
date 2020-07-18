"""

"""

import sys


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
        return '{}({})'.format(self.__class__.__name__, ','.join([str(arg) for arg in self.argv]) + ','*(self.argc-1 - len(self.argv)))

    def __eq__(self, other):
        return type(self) == type(other) and self.argv == other.argv


class Inc(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return self.argv[0] + 1


class Dec(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return self.argv[0] - 1


class Add(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return self.argv[0] + self.argv[1]


class Mul(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
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
        return self.argv[0] == self.argv[1]


class Lt(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return self.argv[0] < self.argv[1]


class Modulate(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        v = self.argv[0]
        if v==0: return '010'
        ret = '01' if v>0 else '10'
        binary = bin(v)[2+(v<0):]
        l = len(binary)
        bitlen = 0--l//4*4
        ret += '1'*(bitlen//4) + '0'
        ret += '0'*(bitlen - l) + binary
        return ret


class Demodulate(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        s = self.argv[0] # must be 01-string
        if s=='010': return 0
        neg = s.startswith('10')
        i = 2
        while s[i]=='1':
            i += 1
        v = int(s[i+1:], 2)
        if neg: v *= -1
        return v


class Neg(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
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
        if not isinstance(self.argv[2], int):
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
        if not isinstance(self.argv[2], int):
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
        if not isinstance(self.argv[2], int):
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
        if not isinstance(self.argv[0], int):
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
        # 引数があればCombinator
        if not isinstance(self.argv[1], int):
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
        return self.argv[0]


class Pwr2(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return pow(2, self.argv[0])


class Cons(Node):
    def __init__(self, argv=None):
        self.argc = 2
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        if len(self.argv) < 2:
            return self
        if isinstance(self.argv[-1], Nil):
            if isinstance(self.argv[0], Nil):
                return Nil
            return self.argv[:-1]
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
        assert isinstance(self.argv[0], Cons)
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
        assert isinstance(self.argv[0], Cons)
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
        return TrueCombinator() if isinstance(self.argv[0], Nil) else FalseCombinator()


class Vec(Node):
    def __init__(self, argv=None):
        self.argc = 1
        if argv:
            self.argv = argv[:]
        else:
            self.argv = []

    def __call__(self):
        return Cons(self.argv)


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
        else:
            # number
            nodes.append(int(t))

    return Program(nodes)


def lex(s):
    return s.split()


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
