from typing import List, Tuple

import icontract
from node import Node

@icontract.invariant(lambda self: len({level for node, level in self.nodes_with_levels() if node.is_leaf}) == 1)
class BTree:
    def __init__(self, order: int):
        self.order: int = order
        self.root: Node = Node(t=order, is_root=True)

    def __iadd__(self, other):
        if isinstance(other, int):
            self.insert(other)
        elif isinstance(other, List):
            self.insert_all(other)
        return self

    def height(self) -> int:
        return self.root.height()

    @icontract.require(lambda self, key: not self.search(key), "Chave a ser inserida não deve existir na árvore")
    @icontract.ensure(lambda self: self.root.subtree_valid())
    def insert(self, key: int):
        if self.root.is_full:
            self._grow_tree()
        self.root.insert_non_full(key)

    @icontract.require(lambda self, key: self.search(key), "Chave a ser removida deve existir na árvore")
    @icontract.ensure(lambda self: self.root.valid_num_children(), "Subtree must have a valid number of children")
    @icontract.ensure(lambda self: self.root.valid_num_keys(), "Subtree must have a valid number of keys")
    def remove(self, key: int):
        self.root.remove(key)
        if self.root.num_keys == 0 and self.root.num_children == 0:
            raise ValueError("Deleting from empty tree")
        elif self.root.num_keys == 0:
            self.root = self.root.children[0]
            self.root.is_root = True

    def insert_all(self, key: List[int]) -> None:
        for k in key:
            self.insert(k)

    @icontract.snapshot(lambda self: self.height(), name="height")
    @icontract.ensure(lambda self, OLD: self.height() == OLD.height + 1)
    def _grow_tree(self):
        new_root = Node(t=self.order, is_root=True)
        new_root.children.append(self.root)
        new_root.split_child(0)
        self.root.is_root = False
        self.root = new_root

    def nodes_with_levels(self) -> list[Tuple[Node, int]]:
        return self.root.nodes_with_levels()

    def print_tree(self):
        if self.root is None:
            print("Empty btree")
        self.root.print_tree()

    def search(self, key: int, node: Node = None) -> bool:
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.is_leaf:
            return False

        return self.search(key, node.children[i])