import interpreter
import sys
import requests
from typing import Optional, Dict, Tuple, List
from interpreter import Modulate, execute

sys.setrecursionlimit(200000)
server_url = sys.argv[1]
player_key = sys.argv[2]


class Expr:
    def __init__(self, evaluated: Optional['Expr'] = None):
        self.evaluated = evaluated

    def __str__(self):
        return str(self.evaluated)


class Atom(Expr):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return str(self.name)


class Ap(Expr):
    def __init__(self, fun: Expr, arg: Expr):
        super().__init__()
        self.fun = fun
        self.arg = arg

    def __str__(self) -> str:
        return 'Ap({},{})'.format(str(self.fun), str(self.arg))

    def display(self) -> str:
        ret = ['ap']
        if isinstance(self.fun, Ap):
            ret.append(self.fun.display())
        elif isinstance(self.fun, Atom):
            ret.append(str(self.fun.name))
        if isinstance(self.arg, Ap):
            ret.append(self.arg.display())
        elif isinstance(self.arg, Atom):
            ret.append(str(self.arg.name))
        return ' '.join(ret)


class Vect:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


cons = Atom('cons')
t = Atom('t')
f = Atom('f')
nil = Atom('nil')

FUNCTIONS: Dict[str, Expr] = dict()


def PRINT_IMAGES(images: Expr):
    print(images)


def SEND_TO_ALIEN_PROXY(data):
    url = server_url + '/aliens/send'
    print(f"url: {url}")
    print(f"data: {data}")
    print(data.display())
    modulated_data = interpreter.execute("ap mod " + data.display())
    modulated_data_str = "".join([str(bit) for bit in modulated_data])

    res = requests.post(url, data=modulated_data_str)
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(1)

    print('Server response:', res.text)
    return res.text

    # return [Atom(0)]
    return [Atom(1), Atom(67425)]


def get_list_items_from_expr(res) -> Tuple[int, Expr, Expr]:
    flag = res.fun.arg
    new_state = res.arg.fun.arg
    data = res.arg.arg

    return [flag, new_state, data]


def interact(state: Expr,  event: Expr) -> Tuple[Expr, Expr]:
    # See https://message-from-space.readthedocs.io/en/latest/message38.html
    expr: Expr = Ap(Ap(Atom('galaxy'), state), event)
    # print('##### interact expr #####', expr, sep='\n')
    res: Expr = eval(expr)
    # print('##### interact res #####', res, sep='\n')

    # Note: res will be modulatable here(consists of cons, nil and numbers only)
    flag, new_state, data = get_list_items_from_expr(res)
    if as_num(flag) == 0:
        return (new_state, multipledraw(data))
    return interact(new_state, SEND_TO_ALIEN_PROXY(data))


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def draw(raw_dots: Expr) -> Expr:
    maxx = maxy = 0
    minx = miny = 0
    dots = []
    for d in raw_dots:
        dot = Dot(d[0], d[1])
        maxx = max(maxx, dot.x)
        maxy = max(maxy, dot.y)
        minx = min(minx, dot.x)
        miny = min(miny, dot.y)
        dots.append(dot)
    w, h = maxx-minx+5, maxy-miny+5
    pic = [[' ']*w for _ in range(h)]
    for dot in dots:
        pic[dot.y-miny][dot.x-minx] = '.'
    print('(y={}, x={})'.format(minx, miny))
    for row in pic:
        print(''.join(row))


def multipledraw(data: List) -> Expr:
    """
    Args:
        data: List<List<Vect>>>
    """
    if data == nil:
        return nil

    data_list_form = interpreter.execute(data.display())
    print(data_list_form)

    print('-' * 60)
    for dots in data_list_form[0]:
        draw(dots)
        print('-' * 60)
    return data


def eval(expr: Expr) -> Expr:
    #print(indent+'===== eval expr =====', indent + str(expr), sep='\n')
    if expr.evaluated is not None:
        #print(indent+'-> evaluated', expr)
        return expr.evaluated
    initial: Expr = expr
    while True:
        result: Expr = try_eval(expr)
        #print(indent+'-> result', result)
        if result == expr:
            initial.evaluated = result
            #print(indent+'-> tried', expr)
            return result
        expr = result


def try_eval(expr: Expr) -> Expr:
    #print(indent+'===== try_eval expr =====', indent + str(expr), sep='\n')
    if expr.evaluated is not None:
        #print(indent+'-> evaluated', expr)
        return expr.evaluated
    if isinstance(expr, Atom) and FUNCTIONS.get(expr.name) is not None:
        return FUNCTIONS.get(expr.name)
    if isinstance(expr, Ap):
        #print(indent+'expr is Ap')
        fun: Expr = eval(expr.fun)
        expr.fun = fun
        #print(indent + 'fun:' + str(fun))
        x: Expr = expr.arg
        if isinstance(fun, Atom):
            if fun.name == 'neg':
                return Atom(-as_num(eval(x)))
            if fun.name == 'inc':
                return Atom(as_num(eval(x))+1)
            if fun.name == 'dec':
                return Atom(as_num(eval(x))-1)
            if fun.name == 'i':
                return x
            if fun.name == 'nil':
                return t
            if fun.name == 'isnil':
                return Ap(x, Ap(t, Ap(t, f)))
            if fun.name == 'car':
                return Ap(x, t)
            if fun.name == 'cdr':
                return Ap(x, f)
            if fun.name == 'modem':
                return Ap(x, f)
        if isinstance(fun, Ap):
            #print(indent+'>>>>> fun is Ap')
            fun2: Expr = eval(fun.fun)
            expr.fun.fun = fun2
            #print(indent + 'fun2:' + str(fun2))
            y: Expr = fun.arg
            if isinstance(fun2, Atom):
                if fun2.name == 't':
                    return y
                if fun2.name == 'f':
                    return x
                if fun2.name == 'add':
                    return Atom(as_num(eval(x)) + as_num(eval(y)))
                if fun2.name == 'mul':
                    return Atom(as_num(eval(x)) * as_num(eval(y)))
                if fun2.name == 'div':
                    return Atom(as_num(eval(y)) // as_num(eval(x)))
                if fun2.name == 'lt':
                    return t if as_num(eval(y)) < as_num(eval(x)) else f
                if fun2.name == 'eq':
                    return t if as_num(eval(x)) == as_num(eval(y)) else f
                if fun2.name == 'cons':
                    return eval_cons(y, x)
            if isinstance(fun2, Ap):
                fun3: Expr = eval(fun2.fun)
                expr.fun.fun.fun = fun3
                z: Expr = fun2.arg
                if isinstance(fun3, Atom):
                    if fun3.name == 's':
                        return Ap(Ap(z, x), Ap(y, x))
                    if fun3.name == 'c':
                        return Ap(Ap(z, x), y)
                    if fun3.name == 'b':
                        return Ap(z, Ap(y, x))
                    if fun3.name == 'cons':
                        return Ap(Ap(x, z), y)
    #print(indent+'-> unupdated', expr)
    return expr


def eval_cons(a: Expr, b: Expr) -> Expr:
    res: Expr = Ap(Ap(cons, eval(a)), eval(b))
    res.evaluated = res
    return res


def as_num(n: Expr) -> int:
    if isinstance(n, Atom):
        return int(n.name)
    print(n)
    raise ValueError('not a number')


def parse_formula(tokens: List[str]) -> Expr:
    def dfs(index: int) -> Tuple[int, Expr]:
        if index >= len(tokens):
            # incomipeted ap formula
            raise ValueError
        if tokens[index] == 'ap':
            used_index, fun = dfs(index+1)
            used_index, arg = dfs(used_index+1)
            return used_index, Ap(fun, arg)
        if tokens[index] == 'b':
            return index, Ap(Ap(Atom('s'), Ap(t, Atom('s'))), t)
        if tokens[index] == 'c':
            return index, Ap(Ap(Atom('s'), Ap(Ap(Atom('s'), Ap(t, Ap(Ap(Atom('s'), Ap(t, Atom('s'))), t))), Atom('s'))), Ap(t, t))
        else:
            return index, Atom(tokens[index])

    return dfs(0)[1]


def parse_functions(lines: List[str]) -> Dict[str, Expr]:
    functions: Dict[str, Expr] = dict()
    for line in lines:
        tokens = line.split()
        function_name = tokens[0]
        # print(tokens)
        expr = parse_formula(tokens[2:])
        # print(expr)
        functions[function_name] = expr
    return functions


def REQUEST_CLICK_FROM_USER() -> Vect:
    print('input x y > ', end='')
    x, y = map(int, input().split())
    return Vect(x, y)


def main():
    # See https://message-from-space.readthedocs.io/en/latest/message39.html
    global FUNCTIONS
    with open('./galaxy.txt') as galaxy:
        FUNCTIONS = parse_functions(galaxy.readlines())
    with open('functions.tsv', 'w') as fout:
        for k, v in sorted(FUNCTIONS.items(), key=lambda x: x[0]):
            fout.write('{}\t{}\n'.format(k, str(v)))

    state: Expr = nil
    vector: Vect = Vect(0, 0)
    click = Ap(Ap(cons, Atom(vector.x)), Atom(vector.y))
    # ap ap ap interact galaxy state click
    expr: Expr = Ap(Ap(Atom('galaxy'), state), click)

    # # repl
    # while True:
    #     print('> ', end='')
    #     tokens = input().split()
    #     try:
    #         expr = parse_formula(tokens)
    #         print(expr)
    #         print(eval(expr))
    #     except TypeError as e:
    #         print(e)

    print('##### interact expr #####', expr, sep='\n')
    res: Expr = eval(expr)
    print('##### interact res #####', res, sep='\n')
    while True:
        click: Expr = Ap(Ap(cons, Atom(vector.x)), Atom(vector.y))
        (new_state, images) = interact(state, click)
        PRINT_IMAGES(images)
        vector = REQUEST_CLICK_FROM_USER()
        state = new_state


if __name__ == '__main__':
    main()
