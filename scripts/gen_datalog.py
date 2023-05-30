"""
Souffle programs generator
"""

import re
from pyformlang import cfg
from pyformlang.regular_expression import Regex


def regex_to_cfg(regex, out_relation="S"):
    """
    Converts a regex given in pyformlang format into cfg

    Parameters
    ----------
    regex : string
        Regular expression in pyformlang.Regex format

    out_relation : string
        A starting symbol for the grammar which represents an out relation here
    
    Returns
    ----------
    cfg : cfg.CFG
        context-free grammar representation of given regex
    """
    grammar = (
        Regex(regex)
        .to_cfg(starting_symbol=f"{out_relation}")
        .remove_epsilon()
        .remove_useless_symbols()
        .eliminate_unit_productions()
        .to_normal_form()
    )

    return grammar


def init_datalog_program(grammar, in_relation, out_relation):
    """
    Initialize datalog program.
    For that we need to declare input and output relations.
    """
    facts = [
        f".decl {in_relation}(x:number, l:symbol, y:number)",
        f".input {in_relation}",
    ]
    facts.extend(
        [f".decl {out_relation}(x:number, y:number)", f".output {out_relation}"]
    )
    facts.extend(
        [".decl source(x:number)", ".input source"]
    )

    vars = grammar.variables.copy()
    vars.remove(grammar.start_symbol)
    
    for var in vars:
        decl_number = re.findall(r'\d+', var.to_text())
        facts.append(f".decl {out_relation}{decl_number[0]}(x:number, y:number)")

    return facts


def regex_to_datalog_facts(regex: str, in_relation, out_relation):
    """
    Convert regex to a list of facts.
    """
    grammar = regex_to_cfg(regex, out_relation)
    facts = init_datalog_program(grammar, in_relation, out_relation)

    for prod in grammar.productions:
        head = re.sub(r"([0-9]+)", "\\1", f"{prod.head}").replace(
            "A", f"{out_relation}"
        )

        b = ""
        for body in prod.body:
            if type(body) is cfg.Terminal:
                b = f'{in_relation}(x, "{body.to_text()}", y)'
            else:
                vars = ["x"]    
                for j in range(len(prod.body) - 1):
                    vars.append(f"z{j}")
                vars.append("y")
                b = ", ".join(
                    [
                        f"""{x.to_text().replace('VAR:', '').replace('"','').replace('A', f'{out_relation}') + f'({vars[num]}, {vars[num + 1]})'}"""
                        for num, x in enumerate(prod.body)
                    ]
                )
        if head == "path" and "path(" not in b:
            facts.append(f"{head}(x, y) :- source(x), {b}.")
        else:
            facts.append(f"{head}(x, y) :- {b}.")
    return facts


def generate_datalog_program(regex, input_rel, output_rel):
    """
    Converts a regex given in a pyformlang format to a souffle program.
    For that we create a list of facts. 
    
    regex : string
        Regular expression in pyformlang.Regex format

    input_rel : string
        Input relation

    output_rel : string
        Output relation
    
    Returns
    ----------
    program : string
        Valid souffle program to evaluate given RPQ 
    """
    return "\n".join(regex_to_datalog_facts(regex, input_rel, output_rel))


if __name__ == "__main__":
    program = generate_datalog_program(input, "edge", "path")
    print(program)
