"""
Usage
python calculator.py [input file path] 2> [stderr file] > [stdout file]
"""
import sys
from interpreter import *

sys.setrecursionlimit(200000)

def flatten(data):
    return [
        element
            for item in data
            for element in (flatten(item) if hasattr(item, '__iter__') else [item])
    ]

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

            # トークン列の書き換えがあった場合はトークン列を出力
            # if new_tokens != token:
            #     print(f"tokens: {tokens}", file=sys.stderr)

            program = None
            try:
                program = parse(tokens[2:])
            except ValueError as e:
                # print(e, file=sys.stderr)
                has_uncalculated = True
                continue
            # print(f"program: {program}", file=sys.stderr)
            try:
                res = program.eval()
                # 結果に Variable が含まれる場合は計算未完了とみなす
                if "Variable" in str(res):
                    has_uncalculated = True
                else:
                    result[var] = res
                display = '{} = {} = {}'.format(
                    tokens[0], res, tokens[2:])
                # print(display, file=sys.stderr)
            except EOFError:
                pass
    
    return result[root]

if __name__ == "__main__":
    filename = sys.argv[1]
    lines = [line.rstrip() for line in open(filename, "r")]
    print(main(lines, root="galaxy"))