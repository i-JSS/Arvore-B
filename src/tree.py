import icontract
from node import Node

class Tree:
    def __init__(self, order: int):
        self.order: int = order
        self.root: Node = Node(order=order, is_leaf=True, is_root=True)


    def print_tree(self, node:Node = None, level:int = 0):
        if node is None:
            node = self.root

        print(("  " * level) + str(node.values))

        if not node.is_leaf:
            for child in node.children:
                self.print_tree(child, level + 1)


    def insert(self, value:int):
        root: Node = self.root

        if len(root.values) == 2 * self.order - 1:
            new_root = Node(order=self.order, is_leaf=False, is_root=True)
            new_root.children.append(root)
            root.is_root = False
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, value)
            self.root = new_root
        else:
            self._insert_non_full(root, value)


    def _insert_non_full(self, node:Node, value:int):
        i: int = len(node.values) - 1

        if node.is_leaf:
            node.values.append(None)
            while i >= 0 and value < node.values[i]:
                node.values[i + 1] = node.values[i]
                i -= 1
            node.values[i + 1] = value
        else:
            while i >= 0 and value < node.values[i]:
                i -= 1
            i += 1
            if len(node.children[i].values) == 2 * self.order - 1:
                self._split_child(node, i)
                if value > node.values[i]:
                    i += 1
            self._insert_non_full(node.children[i], value)


    def _split_key(self, child, new, degree):
        new.values = child.values[degree:]
        child.values = child.values[:degree - 1]

    # lambda argumentos: expressão, a lambda deve falhar
    # if i < 0 or i >= len(parent.children):
    #     raise IndexError("Index 'i' is out of bounds for the child list")
    @icontract.require(
        lambda parent, i: 0 <= i < len(parent.children),
        "Index 'i' is out of bounds for the child list"
    )
    def _split_child(self, parent, i):

        order: int = self.order
        child_split: Node = parent.children[i]
        new_node: Node = Node(order = order, is_leaf = child_split.is_leaf)
        mid_value: int = child_split.values[order - 1]

        self._split_key(child_split, new_node, order)

        if not child_split.is_leaf:
            new_node.children = child_split.children[slice(order, None)]
            child_split.children = child_split.children[slice(0, order)]

        parent.children.insert(i+1, new_node)
        parent.values.insert(i, mid_value)
