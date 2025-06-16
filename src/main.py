import icontract

@icontract.invariant(lambda self: all(self.keys[i] <= self.keys[i + 1] for i in range(len(self.keys) - 1)))
class Node:

    def __init__(self, t: int, n: int, leaf: bool):
        self.t = t
        self.n = n
        self.leaf = leaf
        self.keys = []
        self.children = []



print("TOTOLA")