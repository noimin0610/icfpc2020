import sys
from interpreter import *

sys.setrecursionlimit(200000)

def main(lines, root="galaxy"):
    result = {}
    has_uncalculated = True
    
    while has_uncalculated:
        has_uncalculated = False

        for row_number, s in enumerate(lines):

            print('{}\t{}'.format(row_number, s), file=sys.stderr)
            tokens = lex(s)
            var = tokens[0]

            # 計算済みの token があるなら置き換える
            # lines も更新
            for idx, token in enumerate(tokens[2:], start=2):
                if token in result:
                    tokens[idx] = result[token]
            lines[row_number] = " ".join([str(token) for token in tokens])

            print(f"tokens: {tokens}", file=sys.stderr)

            program = None
            try:
                program = parse(tokens[2:])
            except ValueError as e:
                print(e, file=sys.stderr)
                has_uncalculated = True
                continue
            print(f"program: {program}", file=sys.stderr)
            try:
                result[var] = program.eval()
                display = '{} = {} = {}'.format(
                    tokens[0], result[var], tokens[2:])
            except EOFError:
                pass
    
    return result[root]

if __name__ == "__main__":
    filename = sys.argv[1]
    lines = [line.rstrip() for line in open(filename, "r")]
    print(main(lines, root="galaxy"))