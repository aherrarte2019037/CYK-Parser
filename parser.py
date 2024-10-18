import os.path
import argparse
import grammar_normal_converter as grammar_converter


class Node:
    """
    Represents a non-terminal symbol in CNF.
    Can have up to two children (Node or string).
    Handles multiple parses via alternative children.
    """

    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        """Returns string representation of the Node."""
        return self.symbol


class Parser:
    """
    CYK parser for CNF grammars.
    Accepts grammar from file or string.
    Outputs parse tree(s) as string or to console.
    """

    def __init__(self, grammar, sentence):
        """
        Initializes parser, reads grammar, and prepares for parsing.
        """
        self.parse_table = None
        self.prods = {}
        self.grammar = None
        if os.path.isfile(grammar):
            self.grammar_from_file(grammar)
        else:
            self.grammar_from_string(grammar)
        self.__call__(sentence)

    def __call__(self, sentence, parse=False):
        """
        Parses given sentence with stored grammar.
        """
        if os.path.isfile(sentence):
            with open(sentence) as inp:
                self.input = inp.readline().split()
        else:
            self.input = sentence.split()
        if parse:
            self.parse()

    def grammar_from_file(self, grammar):
        """
        Reads CFG from file, converts to CNF.
        """
        with open(grammar) as cfg:
            lines = cfg.readlines()
        self.grammar = self.convert_grammar([self.split_rule(x) for x in lines if x.strip()])

    def grammar_from_string(self, grammar):
        """
        Reads CFG from string, converts to CNF.
        """
        self.grammar = self.convert_grammar([self.split_rule(x) for x in grammar.split('\n') if x.strip()])

    def split_rule(self, rule):
        """
        Splits rule into LHS and RHS alternatives.
        Handles '|' operator.
        """
        lhs, rhs = rule.replace("->", "").split(None, 1)
        return [lhs.strip()] + [x.strip() for x in rhs.split('|')]

    def convert_grammar(self, grammar):
        """
        Converts grammar with '|' alternatives to CNF.
        """
        result = []
        for rule in grammar:
            lhs = rule[0]
            for rhs in rule[1:]:
                result.append([lhs] + rhs.split())
        return grammar_converter.convert_grammar(result)

    def parse(self):
        """
        Implements CYK parsing algorithm.
        Stores parse table in self.parse_table.
        """
        length = len(self.input)
        self.parse_table = [[[] for x in range(length - y)] for y in range(length)]

        for i, word in enumerate(self.input):
            for rule in self.grammar:
                if f"'{word}'" == rule[1]:
                    self.parse_table[0][i].append(Node(rule[0], word))
        for words_to_consider in range(2, length + 1):
            for starting_cell in range(0, length - words_to_consider + 1):
                for left_size in range(1, words_to_consider):
                    right_size = words_to_consider - left_size

                    left_cell = self.parse_table[left_size - 1][starting_cell]
                    right_cell = self.parse_table[right_size - 1][starting_cell + left_size]

                    for rule in self.grammar:
                        left_nodes = [n for n in left_cell if n.symbol == rule[1]]
                        if left_nodes:
                            right_nodes = [n for n in right_cell if n.symbol == rule[2]]
                            self.parse_table[words_to_consider - 1][starting_cell].extend(
                                [Node(rule[0], left, right) for left in left_nodes for right in right_nodes]
                            )

    def print_tree(self, output=True):
        """
        Prints or returns parse tree(s) starting from the start symbol.
        """
        start_symbol = self.grammar[0][0]
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            if output:
                print("• SI")
                print("• Parse Tree:")
            trees = [generate_tree(node) for node in final_nodes]
            if output:
                for tree in trees:
                    print(tree)
            else:
                return trees
        else:
            print("NO")


def generate_tree(node):
    """
    Generates string representation of parse tree.
    """
    if node.child2 is None:
        return f"[{node.symbol} '{node.child1}']"
    return f"[{node.symbol} {generate_tree(node.child1)} {generate_tree(node.child2)}]"


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("grammar",
                           help="File containing the grammar or string directly representing the grammar.")
    argparser.add_argument("sentence",
                           help="File containing the sentence or string directly representing the sentence.")
    args = argparser.parse_args()
    CYK = Parser(args.grammar, args.sentence)
    CYK.parse()
    CYK.print_tree()