import icontract
from tree import Tree

if __name__ == "__main__":
    tree = Tree(2)
    for k in [10, 20, 5, 6, 12, 30, 7, 17, 21, 22, 34, 23, 24, 35]:
        tree.print_tree()
        tree.insert(k)
        print("\n\n")
    tree.print_tree()