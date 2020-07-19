from typing import Optional, Dict, Tuple


class Expr:
    def __init__(self, evaluated: Optional[Expr] = None):
        self.evaluated = evaluated


class Atom(Expr):
    def __init__(self, name: str):
        self.name = name


class Ap(Expr):
    def __init__(self, fun: Expr, arg: Expr):
        self.fun = fun
        self.arg = arg


class Vect:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


cons = Atom("cons")
t = Atom("t")
f = Atom("f")
nil = Atom("nil")

functions: Dict[str, Expr] = PARSE_FUNCTIONS("galaxy.txt")

# See https://message-from-space.readthedocs.io/en/latest/message39.html


def main():
    state: Expr = nil
    vector: Vect = Vect(0, 0)
    while True:
        click: Expr = Ap(Ap(cons, Atom(vector.x)), Atom(vector.y))
        var(new_state, images) = interact(state, click)
        PRINT_IMAGES(images)
        vector = REQUEST_CLICK_FROM_USER()
        state = new_state

# See https://message-from-space.readthedocs.io/en/latest/message38.html


def interact(state: Expr,  event: Expr) -> Tuple[Expr, Expr]:
    expr: Expr = Ap(Ap(Atom("galaxy"), state), event)
    res: Expr = eval(expr)
    # Note: res will be modulatable here(consists of cons, nil and numbers only)
    flag, new_state, date = GET_LIST_ITEMS_FROM_EXPR(res)
    if as_num(flag) == 0:
        return (new_state, data)
    return interact(new_state, SEND_TO_ALIEN_PROXY(data))


def eval(expr: Expr) -> Expr:
    if expr.evaluated is None:
        return expr.evaluated
    initial: Expr = expr
    while True:
        result: Expr = try_eval(expr)
        if result == expr:
            initial.evaluated = result
            return result
        expr = result


def try_eval(expr: Expr) -> Expr:
    if (expr.evaluated is not None):
        return expr.evaluated
    if (isinstance(expr, Atom) and functions[expr.name] is not None):
        return functions[expr.name]
    if (isinstance(expr, Ap)):
        fun: Expr = eval(expr.Fun)
        x: Expr = expr.arg
        if (isinstance(fun, Atom)):
            if (fun.name == "neg"):
                return Atom(-as_num(eval(x)))
            if (fun.name == "i"):
                return x
            if (fun.name == "nil"):
                return t
            if (fun.name == "isnil"):
                return Ap(x, Ap(t, Ap(t, f)))
            if (fun.name == "car"):
                return Ap(x, t)
            if (fun.name == "cdr"):
                return Ap(x, f)
            if (isinstance(fun, Ap)):
                fun2: Expr = eval(fun.Fun)
                y: Expr = fun.arg
                if (isinstance(fun2, Atom)):
                    if (fun2.name == "t"):
                        return y
                    if (fun2.name == "f"):
                        return x
                    if (fun2.name == "add"):
                        return Atom(as_num(eval(x)) + as_num(eval(y)))
                    if (fun2.name == "mul"):
                        return Atom(as_num(eval(x)) * as_num(eval(y)))
                    if (fun2.name == "div"):
                        return Atom(as_num(eval(y)) / as_num(eval(x)))
                    if (fun2.name == "lt"):
                        return t if as_num(eval(y)) < as_num(eval(x)) else f
                    if (fun2.name == "eq"):
                        return t if as_num(eval(x)) == as_num(eval(y)) else f
                    if (fun2.name == "cons"):
                        return eval_cons(y, x)
                    if (isinstance(fun2, Ap)):
                        fun3: Expr = eval(fun2.Fun)
                        z: Expr = fun2.arg
                        if (isinstance(fun3, Atom)):
                            if (fun3.name == "s"):
                                return Ap(Ap(z, x), Ap(y, x))
                            if (fun3.name == "c"):
                                return Ap(Ap(z, x), y)
                            if (fun3.name == "b"):
                                return Ap(z, Ap(y, x))
                            if (fun3.name == "cons"):
                                return Ap(Ap(x, z), y)
    return expr


def eval_cons(a: Expr, b: Expr) -> Expr:
    res: Expr = Ap(Ap(cons, eval(a), eval(b)))
    res.evaluated = res
    return res


def as_num(n: Expr) -> int:
    if isinstance(n, Atom):
        return PARSE_NUMBER(n.name)
    raise ValueError("not a number")


if __name__ == "__main__":
    main()
