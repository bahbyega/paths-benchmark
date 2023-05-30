import numpy, os, shutil

from pyformlang.regular_expression import Regex

from dataset import query_regex as templates
from gen_datalog import generate_datalog_program

def gen(tpl, n, lst, k):
    res = set()
    i = 0
    while len(res) < n:
        i += 1
        perm = numpy.random.permutation(lst)
        res.add(((tpl % tuple(perm[0:k])), tuple(perm[0:k])))
        if i > 100:
            break
    return res


def gen_from_config(config, num_of_labels, num_of_queries):
    lbls = [
        l.split(" ")[0].rstrip() for l in open(config, "r").readlines()
    ]
    enough_lbls = num_of_labels - len(lbls)
    if enough_lbls > 0:
        for _ in range(enough_lbls):
            lbls.append(lbls[0])
    return [
        (tpl[2], gen(tpl[1], num_of_queries, lbls[0:num_of_labels], tpl[0]))
        for tpl in templates
    ]


def write_qs(qs, root_dir, form):
    for qd in qs:
        path = os.path.join(root_dir, qd[0])
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        i = 0
        for q in qd[1]:
            with open(os.path.join(path, str(i)), "w") as out:
                if form == "regex":
                    out.write(q[0] + "\n")
                elif form == "grammar":
                    out.write(Regex(q[0])
                            .to_cfg()
                            .remove_epsilon()
                            .remove_useless_symbols()
                            .eliminate_unit_productions()
                            .to_normal_form())
                elif form == "datalog":
                    out.write(generate_datalog_program(q[0], "edge", "path"))
                else:
                    print(f"Error: invalid form:{form}")
                i = i + 1


def gen_qs(path_to_config, num_labels, count, path_to_qs, form, seed):
    numpy.random.seed(seed)

    # print("Generating queries")
    # print(path_to_config, num_labels,int(count))
    r = gen_from_config(path_to_config, num_labels, count)

    write_qs(r, path_to_qs, form)
