import argparse
from grammar import Grammar
from cyk_parser import CYKParser

def main():
    parser = argparse.ArgumentParser(description="CYK Parser")
    parser.add_argument("grammar", help="Grammar file or string")
    parser.add_argument("sentence", help="Sentence file or string")
    args = parser.parse_args()

    grammar = Grammar(args.grammar)
    cyk_parser = CYKParser(grammar)

    with open(args.sentence, 'r') if args.sentence.endswith('.txt') else open(args.sentence) as f:
        sentence = f.read().strip()

    if cyk_parser.parse(sentence):
        cyk_parser.print_trees()
    else:
        print("La oración no pertenece al lenguaje generado por la gramática")

if __name__ == "__main__":
    main()