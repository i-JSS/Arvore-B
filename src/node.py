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

    def fill(self, i: int):
        if i > 0 and self.children[i - 1].num_keys > self.children[i - 1].min_keys:
            self._borrow_from_prev(i)
        elif i < self.num_children - 1 and self.children[i + 1].num_keys > self.children[i + 1].min_keys:
            self._borrow_from_next(i)
        else:
            if i < self.num_children - 1:
                pass # fusão do filho i com o filho i+1
            else:
                pass # fusão do filho i - 1 com o filho i

    def _borrow_from_prev(self, i: int):
        child = self.children[i]
        left_sibling = self.children[i - 1]

        child.keys.insert(0, self.keys[i - 1])

        self.keys[i - 1] = left_sibling.keys.pop()

        if not child.is_leaf:
            child.children.insert(0, left_sibling.children.pop())

    def _borrow_from_next(self, i: int):
        child = self.children[i]
        right_sibling = self.children[i + 1]

        child.keys.append(self.keys[i])
        self.keys[i] = right_sibling.keys.pop(0)

        if not child.is_leaf:
            child.children.append(right_sibling.children.pop(0))

    def height(self) -> int:
        return 0 if self.is_leaf else max([child.height() for child in self.children]) + 1

    def nodes_with_levels(self, level: int = 0):
        result = [(self, level)]
        for child in self.children:
            result.extend(child.nodes_with_levels(level + 1))
        return result

    def print_tree(self, level: int = 0):
        print(f'{level}:{"  " * level}{"- " if level > 0 else ""} {self.keys}')
        for child in self.children:
            child.print_tree(level + 1)

    def valid_num_keys(self) -> bool:
        if self.is_root:
            return self.is_leaf or (1 <= self.num_keys <= 2 * self.order - 1)
        return self.order - 1 <= self.num_keys <= 2 * self.order -1

    def valid_num_children(self) -> bool:
        if self.is_leaf:
            return self.num_children == 0
        if self.is_root:
            return 2 <= self.num_children <= 2 * self.order
        return self.order <= self.num_children <= 2 * self.order

    def subtree_valid(self) -> bool:
        if not (self.valid_num_keys() and self.valid_num_children()):
            return False
        return all(child.subtree_valid() for child in self.children)

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0
    
    @property
    def min_keys(self) -> int:
        if self.is_root:
            return 0 if self.is_leaf else 1
        return self.order - 1

    @property
    def max_keys(self) -> int:
        return 2 * self.order - 1

    @property
    def is_full(self) -> bool:
        return self.max_keys <= self.num_keys

    @property
    def num_children(self) -> int:
        return len(self.children)

    @property
    def num_keys(self) -> int:
        return len(self.keys)