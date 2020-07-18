import sys
from interpreter import *

sys.setrecursionlimit(200000)


def main():
    row_number = 0
    try:
        while True:
            s = input()
            row_number += 1

            print('{}\t{}'.format(row_number, s), file=sys.stderr)
            tokens = lex(s)
            # print(tokens, file=sys.stderr)
            program = None
            try:
                program = parse(tokens[2:])
            except ValueError as e:
                print('==== Error ====')
                print('\t', e)
                print('\t', s)
                continue
            # print(program, file=sys.stderr)
            try:
                result = program.eval()
                display = '{} = {} = {}'.format(tokens[0], result, tokens[2:])
                print(display)
            except EOFError:
                pass
    except EOFError:
        pass


if __name__ == "__main__":
    main()
