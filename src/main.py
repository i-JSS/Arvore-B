import icontract
from btree import BTree

if __name__ == "__main__":
    tree = BTree(3)
    for k in [40, 20, 60, 80, 10, 15, 30, 50, 70, 90, 95, 5, 7, 12, 18, 25, 35, 45, 55, 65, 75, 85, 92, 98, 99]:
        tree.print_tree()
        tree.insert(k)
        print("\n\n")
    tree.print_tree()