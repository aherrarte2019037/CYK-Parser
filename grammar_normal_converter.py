# Diccionario global para almacenar reglas
RULE_DICT = {}

def read_grammar(grammar_file):
    """
    Lee el archivo de gramática y lo divide en reglas.
    :param grammar_file: archivo de gramática.
    :return: lista de reglas.
    """
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]

def add_rule(rule):
    """
    Añade una regla al diccionario de reglas.
    :param rule: regla a añadir.
    """
    global RULE_DICT
    if rule[0] not in RULE_DICT:
        RULE_DICT[rule[0]] = []
    RULE_DICT[rule[0]].append(rule[1:])

def convert_grammar(grammar):
    """
    Convierte una GLC a Forma Normal de Chomsky (FNC).
    Las reglas resultantes tienen un terminal o dos no terminales en el lado derecho.
    Puede crear nuevos símbolos no terminales con índices añadidos.
    :param grammar: GLC a convertir.
    :return: gramática en FNC.
    """
    global RULE_DICT
    unit_productions, result = [], []
    res_append = result.append
    index = 0

    for rule in grammar:
        new_rules = []
        if len(rule) == 2 and rule[1][0] != "'":
            # Regla A -> X: se guarda para procesar después
            unit_productions.append(rule)
            add_rule(rule)
            continue
        elif len(rule) > 2:
            # Regla A -> X B C [...] o A -> X a
            terminals = [(item, i) for i, item in enumerate(rule) if item[0] == "'"]
            if terminals:
                for item in terminals:
                    # Reemplaza terminal por nuevo no terminal
                    rule[item[1]] = f"{rule[0]}{str(index)}"
                    new_rules += [f"{rule[0]}{str(index)}", item[0]]
                index += 1
            while len(rule) > 3:
                new_rules.append([f"{rule[0]}{str(index)}", rule[1], rule[2]])
                rule = [rule[0]] + [f"{rule[0]}{str(index)}"] + rule[3:]
                index += 1
        # Añade reglas modificadas o no modificadas
        add_rule(rule)
        res_append(rule)
        if new_rules:
            result.extend(new_rules)
    
    # Procesa producciones unitarias (A -> X)
    while unit_productions:
        rule = unit_productions.pop()
        if rule[1] in RULE_DICT:
            for item in RULE_DICT[rule[1]]:
                new_rule = [rule[0]] + item
                if len(new_rule) > 2 or new_rule[1][0] == "'":
                    result.insert(0, new_rule)
                else:
                    unit_productions.append(new_rule)
                add_rule(new_rule)
    return result