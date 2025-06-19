import icontract
from typing import List

def implies(a, b):
    return not a or b
# @icontract.invariant(lambda self: implies(self.is_root, 1 <= len(self.keys) <= 2 * self.order - 1))
# @icontract.invariant(lambda self: implies(self.is_root, 2 <= len(self.children) <= 2 * self.order))
# @icontract.invariant(lambda self: implies(not self.is_root, 1 <= len(self.keys) <= 2 * self.order - 1))
# @icontract.invariant(lambda self: implies(not self.is_root, self.order <= len(self.children) <= 2 * self.order))
@icontract.invariant(lambda self: all(self.keys[i] <= self.keys[i + 1] for i in range(len(self.keys) - 1)))
class Node:
    def __init__(self, order: int, is_root: bool = False):
        self.order: int = order
        self.is_root: bool = is_root
        self.keys: List[int] = []
        self.children: List[Node] = []

    def insert_non_full(self, key: int):
        i = self.num_keys - 1

        if self.is_leaf:
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1

            child = self.children[i]
            if child.is_full:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    # lambda argumentos: expressão, a lambda deve falhar
    # if i < 0 or i >= len(parent.children):
    #     raise IndexError("Index 'i' is out of bounds for the child list")
    @icontract.require(
        lambda self, i: 0 <= i <= self.num_children,
        "Index 'i' is out of bounds for the child list"
    )
    def split_child(self, i: int):
        order = self.order
        child = self.children[i]
        new_node = Node(order=order)

        mid_key = child.keys[order - 1]

        new_node.keys = child.keys[order:]
        child.keys = child.keys[:order - 1]

        if not child.is_leaf:
            new_node.children = child.children[order:]
            child.children = child.children[:order]

        self.children.insert(i + 1, new_node)
        self.keys.insert(i, mid_key)

    def height(self):
        height = 0
        node = self
        while not node.is_leaf:
            node = node.children[0]
            height += 1
        return height

    def print_tree(self, level:int = 0):
        print(("  " * level), end='')
        if level > 0:
            print("- ", end='')
        print(self.keys)

        if not self.is_leaf:
            for child in self.children:
                child.print_tree(level + 1)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def min_keys(self) -> int:
        return 0 if self.is_root else self.order - 1

    @property
    def max_keys(self) -> int:
        return 2 * self.order - 1

    @property
    def is_full(self) -> bool:
        return self.max_keys == self.num_keys

    @property
    def num_children(self) -> int:
        return len(self.children)

    @property
    def num_keys(self) -> int:
        return len(self.keys)
