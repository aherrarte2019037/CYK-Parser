from typing import List, Dict
from grammar import Grammar
from node import Node

class CYKParser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar.to_cnf()
        self.start_symbol = grammar.start_symbol
        self.parse_table: List[List[List[Node]]] = []

    def parse(self, sentence: str) -> bool:
        words = sentence.split()
        n = len(words)
        self.parse_table = [[[] for _ in range(n)] for _ in range(n)]

        # Fill the base case of the table
        for i, word in enumerate(words):
            for lhs, rhs in self.grammar:
                if len(rhs) == 1 and rhs[0] == f"'{word}'":
                    self.parse_table[0][i].append(Node(lhs, word))

        # Fill the table
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                for k in range(i, j):
                    self._check_cell(i, j, k)

        # Check if the start symbol is in the top-left cell
        return any(node.symbol == self.start_symbol for node in self.parse_table[n-1][0])

    def _check_cell(self, i: int, j: int, k: int):
        for lhs, rhs in self.grammar:
            if len(rhs) == 2:
                for node_b in self.parse_table[k-i][i]:
                    if node_b.symbol == rhs[0]:
                        for node_c in self.parse_table[j-k-1][k+1]:
                            if node_c.symbol == rhs[1]:
                                self.parse_table[j-i][i].append(Node(lhs, node_b, node_c))

    def print_trees(self):
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == self.start_symbol]
        
        if final_nodes:
            print("• Si")
            print("• Árbol(es) de análisis:")
            for i, node in enumerate(final_nodes, 1):
                print(f"\nÁrbol {i}:")
                print(self._generate_tree(node))
        else:
            print("NO")

    def _generate_tree(self, node: Node, level: int = 0) -> str:
        indent = "  " * level
        if isinstance(node.child1, str):
            return f"{indent}{node.symbol} → '{node.child1}'\n"
        else:
            return (f"{indent}{node.symbol}\n" +
                    self._generate_tree(node.child1, level + 1) +
                    self._generate_tree(node.child2, level + 1))