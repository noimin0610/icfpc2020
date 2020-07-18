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
        return node if isinstance(node, int) else node()

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
