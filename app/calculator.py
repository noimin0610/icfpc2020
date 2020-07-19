import sys
from interpreter import *

sys.setrecursionlimit(200000)

def list_to_tokens(lis):
    tokens = []
    for item in lis:
        tokens += ['ap', 'ap', 'cons', str(item)]
    tokens.append('nil')

def main(lines, root="galaxy"):
    result = {}
    has_uncalculated = True
    print(f"all eqs: {len(lines)}")
    
    while has_uncalculated:
        print(f"calculated eqs: {len(result)}")
        has_uncalculated = False

        for row_number, s in enumerate(lines):

            print('{}\t{}'.format(row_number, s), file=sys.stderr)
            tokens = lex(s)
            var = tokens[0]

            # 計算済みの token があるなら置き換える
            # lines も更新
            new_tokens = []
            for idx, token in enumerate(tokens[2:], start=2):
                if token in result:
                    if type(result[token]) == list:
                        new_tokens.append(list_to_tokens(result[token]))
                    else:
                        new_tokens.append(result[token])
                else:
                    new_tokens.append(token)
            token = new_tokens
            lines[row_number] = " ".join(tokens)

            if new_tokens != token:
                print(f"tokens: {tokens}", file=sys.stderr)

            program = None
            try:
                program = parse(tokens[2:])
            except ValueError as e:
                print(e, file=sys.stderr)
                has_uncalculated = True
                continue
            # print(f"program: {program}", file=sys.stderr)
            try:
                result[var] = program.eval()
                display = '{} = {} = {}'.format(
                    tokens[0], result[var], tokens[2:])
                print(display, file=sys.stderr)
            except EOFError:
                pass
    
    return result[root]

if __name__ == "__main__":
    filename = sys.argv[1]
    lines = [line.rstrip() for line in open(filename, "r")]
    print(main(lines, root="galaxy"))