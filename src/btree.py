import icontract
from node import Node

class BTree:
    def __init__(self, order: int):
        self.order: int = order
        self.root: Node = Node(order=order, is_root=True)

    def insert(self, key):
        if self.root.is_full:
            new_root = Node(order=self.order, is_root=True)
            new_root.children.append(self.root)
            new_root.split_child(0)
            self.root.is_root = False
            self.root = new_root
        self.root.insert_non_full(key)

    def print_tree(self, node:Node = None, level:int = 0):
        if node is None:
            node = self.root

        print(("  " * level) + str(node.keys))

        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)