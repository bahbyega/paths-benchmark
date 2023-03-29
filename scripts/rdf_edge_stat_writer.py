import rdflib, sys

from src.graph.graph import Graph


def get_labels_count(g):
    d = {}
    with open(f"{g}", "r") as f:
        lines = f.readlines()
        for line in lines:
            _s, p, _o = line.split(" ")
        d[p] = d.get(p, 0) + 1

    sorted_d = [(k, v) for k, v in sorted(d.items(), key=lambda item: item[1])]
    sorted_d.reverse()

    return sorted_d


def print_config(lst, path_to_config):
    i = 0
    with open(path_to_config, "w") as config:
        for x in lst:
            config.write(x[0] + " " + str(i) + "\n")
            i = i + 1


def build_config(from_txt, to_filename):
    # g=rdflib.Graph()
    # print("Loading graph")
    # g.load(from_rdf, format="n3")
    # print("Loaded")

    r = get_labels_count(from_txt)

    for x in r:
        print(x[0], ": ", x[1])

    print_config(r, to_filename)
    return len(r)
