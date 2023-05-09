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

query_templates = [
    "q1",
    "q2",
    "q3",

    "q4_2",
    "q4_3",
    "q4_4",
    "q4_5",
    
    "q5",
    "q6",
    "q7",
    "q8",
    
    "q9_2",
    "q9_3",
    "q9_4",
    "q9_5",
    "q10_2",
    "q10_3",
    "q10_4",
    "q10_5",
    
    "q11_2",
    "q11_3",
    "q11_4",
    "q11_5",
    
    "q12",
    "q13",
    "q14",
    "q15",
    "q16",
]

BENCH_QUERIES_PATHS = [cfg.QUERIES_REGEX/ graph.id / q_tpl / str(q_num) \
                 for graph in BENCH_GRAPHS \
                 for q_tpl in query_templates \
                 for q_num in range(cfg.DEFAULT_NUM_Q_FOR_EACH_TEMPLATE)]

BENCH_QUERIES_PATHS_GRAMMAR = [cfg.QUERIES_GRAMMAR/ graph.id / q_tpl / str(q_num) \
                 for graph in BENCH_GRAPHS \
                 for q_tpl in query_templates \
                 for q_num in range(cfg.DEFAULT_NUM_Q_FOR_EACH_TEMPLATE)]