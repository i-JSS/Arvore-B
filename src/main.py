from btree import BTree

size = 100
ceiling = 100
samples = [40, 20, 60, 80, 10, 15, 30, 50, 70, 90, 95, 5, 7, 12, 18, 25, 35, 45, 55, 65, 75, 85, 92, 98, 99]
if __name__ == "__main__":
    tree = BTree(3)
    tree += samples
    tree.print_tree()

    print("\nBuscar chave 17:", tree.search(17))
    print("Buscar chave 20:", tree.search(20))
    print("Deleting all values")
    for i, sample in enumerate(samples[:-1]):
        print(f"Tree no {i}, removing {sample}")
        tree.remove(sample)
        tree.print_tree()
