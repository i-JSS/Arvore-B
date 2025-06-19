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

    # @icontract.require(lambda self: self.CHAVE INSERIDA NAO EXISTE NA ARVORE)
    @icontract.ensure(lambda self: self.root.subtree_valid())
    def insert(self, key):
        if self.root.is_full:
            self._grow_tree()
        self.root.insert_non_full(key)

    # @icontract.require(lambda self: self.CHAVE A SER REMOVIDA EXISTE NA ARVORE)
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