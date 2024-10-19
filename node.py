from typing import Union

class Node:
    def __init__(self, symbol: str, child1: Union['Node', str], child2: Union['Node', str, None] = None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        return self.symbol