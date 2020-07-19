import sys
from collections import defaultdict
import itertools

class Detector:
    def __init__(self, eqs):
        self.eqs = eqs
        self.dependencies = self.get_dependencies()
        self.used = defaultdict(lambda: False)

    def get_dependencies(self):
        # 変数間の依存関係の隣接リスト
        # value の変数を計算しないと key の式は計算できない
        dependencies = defaultdict(set)

        # 変数間の依存関係を dependencies に入れる
        for eq in self.eqs:
            terms = eq.split(" ")
            key = terms[0]
            for term in terms[1:]:
                if key == term:
                    continue
                if term.startswith(":"):
                    value = term
                    dependencies[key].add(value)
        
        return dependencies

    def print_loop(self, hist, loop_node):
        for node in itertools.dropwhile(lambda node: node != loop_node, hist):
            print(node, end="->")
        print(loop_node)

    def dfs(self, node, hist):
        hist.append(node)
        for nxt in self.dependencies[node]:
            if nxt in hist:
                self.print_loop(hist, nxt)
                continue
            else:
                self.dfs(nxt, hist)
        hist.pop()

    def detect(self, root_node):
        self.dfs(root_node, [])

        
if __name__ == "__main__":
    # example: python3 loop_detector.py ../galaxy.txt galaxy
    filename = sys.argv[1]
    root_node = sys.argv[2]
    equations = [line.rstrip() for line in open(filename, "r") if line]
    detector = Detector(equations)
    detector.detect(root_node)