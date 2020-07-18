"""
Usage
python calculator.py [input file path] 2> [stderr file] > [stdout file]
"""
import sys
import collections
from interpreter import *

sys.setrecursionlimit(200000)


def main(lines, root="galaxy"):
    n = len(lines)
    determined_variables = {}
    updated = True
    print(f"all eqs: {len(lines)}")

    # init
    blocks = collections.defaultdict(set)
    is_blocked_by = collections.defaultdict(set)
    eqs = {}
    for s in lines:
        tokens = lex(s)
        var_label = tokens[0]
        eqs[var_label] = tokens
        program = parse(tokens[2:])
        nodes = []
        for node in program.nodes:
            if isinstance(node, Variable):
                is_blocked_by[var_label].add(node.argv[0])
                blocks[node.argv[0]].add(var_label)

    while updated:
        print(f"calculated eqs: {len(determined_variables)}")
        updated_keys = []
        unupdated_keys = []
        updated = False

        for label in eqs.keys():
            if label in determined_variables:
                continue
            if len(is_blocked_by[label]) > 0:
                continue
            tokens = eqs[label]
            program = parse(tokens[2:])
            nodes = []
            for node in program.nodes:
                if isinstance(node, Variable):
                    if node.argv[0] in determined_variables:
                        nodes.append(determined_variables[node.argv[0]])
                    else:
                        nodes.append(node)
                else:
                    nodes.append(node)
            if program.nodes != nodes:
                program.nodes = nodes

            res = program.eval()
            # 結果に Variable が含まれる場合は計算未完了とみなす
            if "Variable" in str(res):
                unupdated_keys.append(label)
                print(label, res, file=sys.stderr)
                continue
            determined_variables[label] = res
            for k in blocks[label]:
                is_blocked_by[k].remove(label)
            updated_keys.append(label)
            updated = True
        # print(updated_keys)
        print(unupdated_keys)
    print(f"calculated eqs: {len(determined_variables)}")
    with open('is_blocked_by.dot', 'w') as fout:
        for k, v in is_blocked_by.items():
            for e in list(v):
                fout.write('{} -> {};\n'.format(k[1:], e[1:]))
    return determined_variables[root] if root in determined_variables else None


if __name__ == "__main__":
    filename = sys.argv[1]
    lines = [line.rstrip() for line in open(filename, "r")]
    print(main(lines, root="galaxy"))
