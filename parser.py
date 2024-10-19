import os.path
import argparse
import grammar_normal_converter as grammar_converter


class Node:
    """
    Representa un símbolo no terminal en FNC.
    Puede tener hasta dos hijos (Node o string).
    Maneja múltiples análisis mediante hijos alternativos.
    """

    def __init__(self, symbol, child1, child2=None):
        self.symbol = symbol
        self.child1 = child1
        self.child2 = child2

    def __repr__(self):
        """Retorna representación en string del Node."""
        return self.symbol


class Parser:
    """
    Parser CYK para gramáticas en FNC.
    Acepta gramática desde archivo o string.
    Muestra árbol(es) de análisis como string o en consola.
    """

    def __init__(self, grammar, sentence):
        """
        Inicializa el parser, lee la gramática y prepara para el análisis.
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
        Analiza la oración dada con la gramática almacenada.
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
        Lee GLC desde archivo, convierte a FNC.
        """
        with open(grammar) as cfg:
            lines = cfg.readlines()
        self.grammar = self.convert_grammar([self.split_rule(x) for x in lines if x.strip()])

    def grammar_from_string(self, grammar):
        """
        Lee GLC desde string, convierte a FNC.
        """
        self.grammar = self.convert_grammar([self.split_rule(x) for x in grammar.split('\n') if x.strip()])

    def split_rule(self, rule):
        """
        Divide regla en LHS y alternativas RHS.
        Maneja operador '|'.
        """
        lhs, rhs = rule.replace("->", "").split(None, 1)
        return [lhs.strip()] + [x.strip() for x in rhs.split('|')]

    def convert_grammar(self, grammar):
        """
        Convierte gramática con alternativas '|' a FNC.
        """
        result = []
        for rule in grammar:
            lhs = rule[0]
            for rhs in rule[1:]:
                result.append([lhs] + rhs.split())
        return grammar_converter.convert_grammar(result)

    def parse(self):
        """
        Implementa algoritmo de análisis CYK.
        Almacena tabla de análisis en self.parse_table.
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
        Imprime o retorna árbol(es) de análisis desde el símbolo inicial.
        """
        start_symbol = self.grammar[0][0]
        final_nodes = [n for n in self.parse_table[-1][0] if n.symbol == start_symbol]
        if final_nodes:
            if output:
                print("• SI")
                print("• Árbol de análisis:")
            trees = [generate_tree(node) for node in final_nodes]
            if output:
                for i, tree in enumerate(trees, 1):
                    if len(trees) > 1:
                        print(f"\nÁrbol {i}:")
                    print(tree)
            else:
                return trees
        else:
            print("NO")


def generate_tree(node, level=0):
    """
    Genera representación en string del árbol de análisis con indentación.
    """
    indent = "  " * level
    if node.child2 is None:
        return f"{indent}{node.symbol} → '{node.child1}'\n"
    else:
        return f"{indent}{node.symbol}\n" + \
               generate_tree(node.child1, level + 1) + \
               generate_tree(node.child2, level + 1)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("grammar",
                           help="Archivo con la gramática o string que representa directamente la gramática.")
    argparser.add_argument("sentence",
                           help="Archivo con la oración o string que representa directamente la oración.")
    args = argparser.parse_args()
    CYK = Parser(args.grammar, args.sentence)
    CYK.parse()
    CYK.print_tree()