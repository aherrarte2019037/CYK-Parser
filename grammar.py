from typing import List, Tuple, Dict

class Grammar:
    def __init__(self, source: str):
        self.rules = self._parse_grammar(source)
        self.start_symbol = self.rules[0][0]

    def _parse_grammar(self, source: str) -> List[Tuple[str, List[str]]]:
        if source.endswith('.txt'):
            with open(source, 'r') as file:
                lines = file.readlines()
        else:
            lines = source.split('\n')
        
        return [self._split_rule(line.strip()) for line in lines if line.strip()]

    def _split_rule(self, rule: str) -> Tuple[str, List[str]]:
        lhs, rhs = rule.replace("->", "").split(None, 1)
        return (lhs.strip(), [alt.strip() for alt in rhs.split('|')])

    def to_cnf(self) -> List[Tuple[str, List[str]]]:
        cnf_rules: List[Tuple[str, List[str]]] = []
        rule_dict: Dict[str, List[List[str]]] = {}
        unit_productions: List[Tuple[str, List[str]]] = []
        index = 0

        # Step 1: Eliminate ε-productions and unit productions
        for lhs, rhs_list in self.rules:
            new_rhs_list = []
            for rhs in rhs_list:
                symbols = rhs.split()
                if len(symbols) == 1 and symbols[0][0] != "'":
                    unit_productions.append((lhs, symbols))
                else:
                    new_rhs_list.append(symbols)
            
            if new_rhs_list:
                if lhs not in rule_dict:
                    rule_dict[lhs] = []
                rule_dict[lhs].extend(new_rhs_list)

        # Step 2: Eliminate unit productions
        while unit_productions:
            lhs, rhs = unit_productions.pop(0)
            if rhs[0] in rule_dict:
                for production in rule_dict[rhs[0]]:
                    if len(production) == 1 and production[0][0] != "'":
                        unit_productions.append((lhs, production))
                    else:
                        if lhs not in rule_dict:
                            rule_dict[lhs] = []
                        rule_dict[lhs].append(production)

        # Step 3: Convert to CNF
        for lhs, rhs_list in rule_dict.items():
            for rhs in rhs_list:
                if len(rhs) > 2:
                    new_lhs = lhs
                    while len(rhs) > 2:
                        new_symbol = f"X{index}"
                        index += 1
                        cnf_rules.append((new_lhs, [rhs[0], new_symbol]))
                        new_lhs = new_symbol
                        rhs = rhs[1:]
                    cnf_rules.append((new_lhs, rhs))
                else:
                    cnf_rules.append((lhs, rhs))

        return cnf_rules