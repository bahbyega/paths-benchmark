from pyformlang import cfg
from pyformlang.regular_expression import Regex
import re


def regex_to_cfg(regex: str, out_relation):
    grammar = (
        Regex(regex)
        .to_cfg(starting_symbol=f"{out_relation}(x, y)")
        .remove_epsilon()
        .remove_useless_symbols()
        .eliminate_unit_productions()
        .to_normal_form()
    )

    return grammar


def init_datalog_program(grammar, in_relation, out_relation):
    facts = [
        f".decl {in_relation}(x:number, l:symbol, y:number)",
        f".input {in_relation}",
    ]
    facts.extend(
        [f".decl {out_relation}(x:number, y:number)", f".output {out_relation}"]
    )
    facts.extend(
        [
            f".decl {out_relation}{i}(x:number, y:number)"
            for i in range(len(grammar.variables) - 1)
        ]
    )

    return facts


def regex_to_datalog_facts(regex: str, in_relation, out_relation):
    grammar = regex_to_cfg(regex, out_relation)
    facts = init_datalog_program(grammar, in_relation, out_relation)

    for prod in grammar.productions:
        head = re.sub(r"([0-9]+)", "\\1(x, y)", f"{prod.head}").replace(
            "A", f"{out_relation}"
        )

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
                        f'{x.to_text().replace("A", f"{out_relation}") + f"({vars[num]}, {vars[num + 1]})"}'
                        for num, x in enumerate(prod.body)
                    ]
                )
        facts.append(f"{head} :- {b}.")
    return facts


def generate_datalog_program(regex, input, output):
    return "\n".join(regex_to_datalog_facts(regex, input, output))


if __name__ == "__main__":
    program = generate_datalog_program(input, "edge", "path")
    print(program)
