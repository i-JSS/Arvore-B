import icontract
from btree import BTree
from random import randint

size = 100
ceiling = 100
if __name__ == "__main__":
    tree = BTree(2)
    tree += list(randint(1, ceiling) for _ in range(size))
    tree.print_tree()