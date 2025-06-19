import icontract
from typing import List

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
        return 0 if self.is_leaf else max([child.height() for child in self.children]) + 1

    def print_tree(self, level:int = 0):
        print(f'{level}:{"  " * level}{"- " if level > 0 else ""} {self.keys}')
        for child in self.children:
            child.print_tree(level + 1)

    def valid_num_keys(self) -> bool:
        if self.is_root:
            return self.is_leaf or (1 <= self.num_keys <= 2 * self.order - 1)
        else:
            return self.order - 1 <= self.num_keys <= 2 * self.order -1

    def valid_num_children(self) -> bool:
        if self.is_leaf:
            return self.num_children == 0
        if self.is_root:
            return 2 <= self.num_children <= 2 * self.order
        return self.order <= self.num_children <= 2 * self.order

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
