import icontract
from node import Node

class BTree:
    def __init__(self, order: int):
        self.order: int = order
        self.root: Node = Node(order=order, is_root=True)

    def height(self):
        return self.root.height()

    def insert(self, key):
        if self.root.is_full:
            self._grow_tree()
        self.root.insert_non_full(key)

    @icontract.snapshot(lambda self: self.height(), name="height")
    @icontract.ensure(lambda self, OLD: self.height() == OLD.height + 1)
    def _grow_tree(self):
        new_root = Node(order=self.order, is_root=True)
        new_root.children.append(self.root)
        new_root.split_child(0)
        self.root.is_root = False
        self.root = new_root

    def print_tree(self, node:Node = None, level:int = 0):
        if node is None:
            node = self.root

        print(("  " * level) + str(node.keys))

        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)