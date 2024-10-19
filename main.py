import argparse
from grammar import Grammar
from cyk_parser import CYKParser
import time
from typing import List, Tuple, Dict, Callable

def time_function(func: Callable, *args, **kwargs) -> Tuple[float, any]:
    # Mide el tiempo de ejecución de una función.
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time, result

def format_time(seconds: float) -> str:
    # Formatea el tiempo en segundos a una cadena legible.
    if seconds < 1e-3:
        return f"{seconds*1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds*1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"

def main():
    parser = argparse.ArgumentParser(description="CYK Parser")
    parser.add_argument("grammar", help="Grammar file or string")
    parser.add_argument("sentence", help="Sentence file or string")
    args = parser.parse_args()

    # Medir el tiempo de carga y procesamiento de la gramática
    grammar_time, grammar = time_function(Grammar, args.grammar)
    print(f"Tiempo de carga y procesamiento de la gramática: {format_time(grammar_time)}")

    # Medir el tiempo de inicialización del parser
    init_time, cyk_parser = time_function(CYKParser, grammar)
    print(f"Tiempo de inicialización del parser: {format_time(init_time)}")

    with open(args.sentence, 'r') if args.sentence.endswith('.txt') else open(args.sentence) as f:
        sentence = f.read().strip()

    # Medir el tiempo de parsing
    parse_time, parse_result = time_function(cyk_parser.parse, sentence)
    print(f"Tiempo de parsing: {format_time(parse_time)}")

    if parse_result:
        # Medir el tiempo de generación de árboles
        tree_time, _ = time_function(cyk_parser.print_trees)
        print(f"Tiempo de generación y impresión de árboles: {format_time(tree_time)}")
    else:
        print("La oración no pertenece al lenguaje generado por la gramática.")

    # Calcular y mostrar el tiempo total
    total_time = grammar_time + init_time + parse_time + (tree_time if parse_result else 0)
    print(f"Tiempo total de ejecución: {format_time(total_time)}")

if __name__ == "__main__":
    main()