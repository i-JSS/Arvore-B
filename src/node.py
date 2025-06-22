import icontract
from typing import List

@icontract.invariant(lambda self: all(self.keys[i] <= self.keys[i + 1] for i in range(len(self.keys) - 1)))
class Node:
    def __init__(self, t: int, is_root: bool = False):
        self.t: int = t
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

    def split_child(self, i: int):
        order = self.t
        child = self.children[i]
        new_node = Node(t=order)

        mid_key = child.keys[order - 1]

        new_node.keys = child.keys[order:]
        child.keys = child.keys[:order - 1]

        if not child.is_leaf:
            new_node.children = child.children[order:]
            child.children = child.children[:order]

        self.children.insert(i + 1, new_node)
        self.keys.insert(i, mid_key)

    def print_tree(self, level: int = 0):
        print(f'{level}:{"  " * level}{"- " if level > 0 else ""} {self.keys}')
        for child in self.children:
            child.print_tree(level + 1)

    def valid_num_keys(self) -> bool:
        if self.is_root:
            return self.is_leaf or (1 <= self.num_keys <= 2 * self.t - 1)
        return self.t - 1 <= self.num_keys <= 2 * self.t -1

    def valid_num_children(self) -> bool:
        if self.is_leaf:
            return self.num_children == 0
        if self.is_root:
            return 2 <= self.num_children <= 2 * self.t
        return self.t <= self.num_children <= 2 * self.t

    def subtree_valid(self) -> bool:
        if not (self.valid_num_keys() and self.valid_num_children()):
            return False
        return all(child.subtree_valid() for child in self.children)

    def remove(self, key: int) -> None:
        if key in self.keys:
            # Case 1 - leaf
            if self.is_leaf:
                self.keys.remove(key)
                return

            # Case 2 - internal node
            child_idx = self.keys.index(key)
            predecessor_child = self.children[child_idx]
            successor_child = self.children[child_idx+1]

            # Case 2.a
            if predecessor_child.num_keys >= self.t:
                predecessor = self._find_predecessor(child_idx)
                predecessor_child.remove(predecessor)
                self.keys[child_idx] = predecessor
            # Case 2.b
            elif successor_child.num_keys >= self.t:
                successor = self._find_successor(child_idx)
                successor_child.remove(successor)
                self.keys[child_idx] = successor
            # Case 2.c
            else:
                merged_node = self._merge(child_idx)
                merged_node.remove(key)
        # Case 3 - k not in internal node
        else:
            child_idx = 0
            while child_idx < self.num_keys and key > self.keys[child_idx]:
                child_idx += 1

            if self.is_leaf:
                raise RuntimeError("Key not found")

            child = self.children[child_idx]
            if child.num_keys == self.t - 1:
                left_sibling = self.children[child_idx-1] if child_idx > 0 else None
                right_sibling = self.children[child_idx+1] if child_idx < len(self.children)-1 else None
                #Case 3.a sibling with atleast t keys
                if left_sibling and left_sibling.num_keys >= self.t:
                    self._borrow_from_prev(child_idx)
                elif right_sibling and right_sibling.num_keys >= self.t:
                    self._borrow_from_next(child_idx)
                # Case 3.b - siblings have t - 1 keys
                else:
                    if left_sibling:
                        child = self._merge(child_idx - 1)
                    else:
                        child = self._merge(child_idx)
            child.remove(key)

    def _find_minimum_key(self):
        if self.is_leaf:
            return self.keys[0]
        return self.children[0]._find_minimum_key()

    def _find_maximum_key(self):
        if self.is_leaf:
            return self.keys[-1]
        return self.children[-1]._find_maximum_key()

    # Assumes the key exists
    def _find_predecessor(self, key_idx: int):
        return self.children[key_idx]._find_maximum_key()

    def _find_successor(self, key_idx: int):
        return self.children[key_idx+1]._find_minimum_key()

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

    def _merge(self, key_idx: int):
        left_child = self.children[key_idx]
        right_child = self.children[key_idx+1]
        parent_key = self.keys[key_idx]

        left_child.keys = left_child.keys + [parent_key] + right_child.keys
        if not left_child.is_leaf:
            left_child.children = left_child.children + right_child.children

        self.keys.pop(key_idx)
        self.children.pop(key_idx+1)

        return left_child

    def nodes_with_levels(self, level: int = 0):
        result = [(self, level)]
        for child in self.children:
            result.extend(child.nodes_with_levels(level + 1))
        return result

    def height(self) -> int:
        return 0 if self.is_leaf else max([child.height() for child in self.children]) + 1

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def min_keys(self) -> int:
        if self.is_root:
            return 0 if self.is_leaf else 1
        return self.t - 1

    @property
    def max_keys(self) -> int:
        return 2 * self.t - 1

    @property
    def is_full(self) -> bool:
        return self.max_keys <= self.num_keys

    @property
    def num_children(self) -> int:
        return len(self.children)

    @property
    def num_keys(self) -> int:
        return len(self.keys)