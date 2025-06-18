import icontract
from typing import List

# TODO CORRIGIR ESSE CONTRATO
# @icontract.invariant(
#     lambda self:
#         (
#             (1 <= len(self.keys) <= 2 * self.order - 1)
#             if self.is_root else
#             (self.order - 1 <= len(self.keys) <= 2 * self.order - 1)
#         )
#     and
#         (
#             (2 <= len(self.children) <= 2 * self.order)
#             if self.is_root else
#             (self.order <= len(self.children) <= 2 * self.order)
#         )
#     and
#         (
#             all(self.keys[i] <= self.keys[i + 1] for i in range(len(self.keys) - 1))
#         )
# )
class Node:
    def __init__(self, order: int, is_leaf: bool = False, is_root: bool = False):
        self.order: int = order
        self.is_leaf: bool = is_leaf
        self.is_root: bool = is_root
        self.values: List[int] = []
        self.children: List[Node] = []