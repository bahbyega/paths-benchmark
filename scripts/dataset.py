import json

import config as cfg

GRAPHS_JSON = json.loads((cfg.META / "graphs.json").read_text())["data"]

class PropertyGraph:
    def __init__(self, id) -> None:
        self.json = next(filter(lambda d: d["source"] == f"{id}.txt", GRAPHS_JSON))
        self.id = id
        self.source = self.json["source"]
        self.num_nodes = int(self.json["num_nodes"])
        self.num_edges = int(self.json["num_edges"])
        self.num_labels = int(self.json["num_labels"])
        self.filepath = cfg.GRAPHS / self.json["type"] / self.json["source"]


GRAPH_NAME_core = "core"
GRAPH_NAME_enzyme = "enzyme"
GRAPH_NAME_eclass = "eclass"
GRAPH_NAME_go = "go"
GRAPH_NAME_advogato = "advogato"
GRAPH_NAME_youtube = "youtube"
GRAPH_NAME_geospecies = "geospecies"
GRAPH_NAME_taxonomy = "taxonomy"

ALL_GRAPHS = [
    GRAPH_NAME_core,
    GRAPH_NAME_enzyme,
    GRAPH_NAME_eclass,
    GRAPH_NAME_go,
    GRAPH_NAME_advogato,
    GRAPH_NAME_youtube,
    GRAPH_NAME_geospecies,
    GRAPH_NAME_taxonomy
]

GRAPH_core = PropertyGraph(GRAPH_NAME_core)
GRAPH_enzyme = PropertyGraph(GRAPH_NAME_enzyme)
GRAPH_eclass = PropertyGraph(GRAPH_NAME_eclass)
GRAPH_go = PropertyGraph(GRAPH_NAME_go)
GRAPH_advogato = PropertyGraph(GRAPH_NAME_advogato)
GRAPH_youtube = PropertyGraph(GRAPH_NAME_youtube)
GRAPH_geospecies = PropertyGraph(GRAPH_NAME_geospecies)
GRAPH_taxonomy = PropertyGraph(GRAPH_NAME_taxonomy)

BENCH_GRAPHS = [
    GRAPH_core,
    GRAPH_enzyme,
    GRAPH_eclass,
    GRAPH_go,
    GRAPH_advogato,
    GRAPH_youtube,
    GRAPH_geospecies,
    GRAPH_taxonomy
]


query_regex = [
    (1, "%s*", "q1"),
    (2, "%s %s*", "q2"),
    (3, "%s %s* %s*", "q3"),
    (2, "(%s | %s)*", "q4_2"),
    (3, "(%s | %s | %s)*", "q4_3"),
    (4, "(%s | %s | %s | %s)*", "q4_4"),
    (5, "(%s | %s | %s | %s | %s)*", "q4_5"),
    (3, "%s %s* %s", "q5"),
    (2, "%s* %s*", "q6"),
    (3, "%s %s %s*", "q7"),
    (2, "%s? %s*", "q8"),
    (2, "(%s | %s)+", "q9_2"),
    (3, "(%s | %s | %s)+", "q9_3"),
    (4, "(%s | %s | %s | %s)+", "q9_4"),
    (5, "(%s | %s | %s | %s | %s)+", "q9_5"),
    (3, "(%s | %s) %s*", "q10_2"),
    (4, "(%s | %s | %s) %s*", "q10_3"),
    (5, "(%s | %s | %s | %s) %s*", "q10_4"),
    (6, "(%s | %s | %s | %s | %s) %s*", "q10_5"),
    (2, "%s %s", "q11_2"),
    (3, "%s %s %s", "q11_3"),
    (4, "%s %s %s %s", "q11_4"),
    (5, "%s %s %s %s %s", "q11_5"),
    (4, "((%s %s)+) | (%s %s)+", "q12"),
    (5, "((%s (%s %s)*)+) | (%s %s)+", "q13"),
    (6, "((%s %s (%s %s)*)+) | (%s | %s)*", "q14"),
    (4, "(%s | %s)+ (%s | %s)+", "q15"),
    (5, "%s %s (%s | %s | %s)", "q16"),
]

query_templates = [x[2] for x in query_regex]

BENCH_QUERIES_PATHS = [cfg.QUERIES_REGEX/ graph.id / q_tpl / str(q_num) \
                 for graph in BENCH_GRAPHS \
                 for q_tpl in query_templates \
                 for q_num in range(cfg.DEFAULT_NUM_Q_FOR_EACH_TEMPLATE)]

BENCH_QUERIES_PATHS_GRAMMAR = [cfg.QUERIES_GRAMMAR/ graph.id / q_tpl / str(q_num) \
                 for graph in BENCH_GRAPHS \
                 for q_tpl in query_templates \
                 for q_num in range(cfg.DEFAULT_NUM_Q_FOR_EACH_TEMPLATE)]