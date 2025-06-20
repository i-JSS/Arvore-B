from typing import List

import icontract
from node import Node

class BTree:
    def __init__(self, order: int):
        self.order: int = order
        self.root: Node = Node(order=order, is_root=True)

    def __iadd__(self, other):
        if isinstance(other, int):
            self.insert(other)
        elif isinstance(other, List):
            self.insertall(other)
        return self

    def height(self):
        return self.root.height()

    @icontract.require(lambda self, key: not self.search(key), "Chave a ser inserida não deve existir na árvore")
    @icontract.ensure(lambda self: self.root.subtree_valid())
    def insert(self, key):
        if self.root.is_full:
            self._grow_tree()
        self.root.insert_non_full(key)

    @icontract.require(lambda self, key: self.search(key), "Chave a ser removida deve existir na árvore")
    @icontract.ensure(lambda self: self.root.subtree_valid())
    def remove(self, key):
        pass

    def insertall(self, key: List[int]) -> None:
        for k in key:
            self.insert(k)

    @icontract.snapshot(lambda self: self.height(), name="height")
    @icontract.ensure(lambda self, OLD: self.height() == OLD.height + 1)
    def _grow_tree(self):
        new_root = Node(order=self.order, is_root=True)
        new_root.children.append(self.root)
        new_root.split_child(0)
        self.root.is_root = False
        self.root = new_root

    def print_tree(self):
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