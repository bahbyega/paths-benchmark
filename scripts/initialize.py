import os
import argparse
import csv

from tqdm import tqdm

import dataset as ds
import config as cfg

from rdf_edge_stat_writer import build_config
from gen_queries import gen_qs
from gen_chunks import select_number_source_verts


def txt_to_facts(graph):
    txt_path = cfg.GRAPHS.joinpath(f"txt/{graph}.txt")
    facts_path = cfg.GRAPHS.joinpath(f"facts/{graph}/edge.facts")
    os.makedirs(os.path.dirname(facts_path), exist_ok=True)

    with open(txt_path, "r") as rf, open(facts_path, "w") as wf:
        separator = "\t"
        for line in tqdm(rf.readlines(), desc=f"Converting '{graph}'"):
            wf.write(line.replace(" ", separator))

def gen_queries(graph, count=cfg.DEFAULT_NUM_Q_FOR_EACH_TEMPLATE):
    # if not present, create a mapping from labels to integers for a graph
    path_to_config = cfg.GRAPHS.joinpath(f"config/{graph}.cfg")
    path_to_txt= cfg.GRAPHS.joinpath(f"txt/{graph}.txt")

    if not os.path.isfile(path_to_config):
        build_config(path_to_txt, path_to_config)

    path_to_qs_regex = cfg.QUERIES_REGEX.joinpath(f"{graph}")
    path_to_qs_grammar = cfg.QUERIES_GRAMMAR.joinpath(f"{graph}")
    path_to_qs_datalog = cfg.QUERIES_DATALOG.joinpath(f"{graph}")
    
    paths_to_qs = [path_to_qs_regex, path_to_qs_grammar, path_to_qs_datalog]
    forms = ["regex", "grammar", "datalog"]

    for i, path_qs in enumerate(tqdm(paths_to_qs, desc=f"Generating queries for {graph}")):
        path_qs.parent.mkdir(exist_ok=True, parents=True)
        if not os.path.exists(path_qs):
            os.makedirs(path_qs)

        for query_num in range(count):
            path = path_qs.joinpath(f"{query_num}")
            if not os.path.isfile(path):
                gen_qs(path_to_config, cfg.DEFAULT_LABELS_COUNT, count, path_qs, forms[i])

def write_chunks_file(result_dir, graph, chunk_size):
    if not os.path.exists(result_dir):
            os.makedirs(result_dir)
    chunk_file_path = result_dir.joinpath(f'chunk-{graph.name}-{chunk_size}')
    chunk_csv = open(chunk_file_path, mode='a', newline='\n')
    chunk_writer = csv.writer(chunk_csv, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')

    chunks = []
    if chunk_size is None:  
        chunks = select_number_source_verts(graph.num_nodes, graph.matrices_size)
    else:
        chunks = select_number_source_verts(graph.num_nodes, chunk_size)
    
    for chunk in chunks:
        chunk_writer.writerow([chunk])

    return chunks

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare graphs, generate queries and start vertices.")
    parser.add_argument("-g", "--graphs", choices=ds.ALL_GRAPHS, nargs="+", help=f"graph to convert")
    args = parser.parse_args()

    graphs = []
    if args.graphs is not None:
        graphs = [x for x in ds.BENCH_GRAPHS if x.name in args.graphs]
    else:
        graphs = ds.BENCH_GRAPHS
    
    for graph in graphs:
        txt_to_facts(graph.name)
        gen_queries(graph.name)

        for chunk_size in tqdm(cfg.DEFAULT_CHUNK_SIZES, desc=f"Generating chunks for {graph.name}"):
            write_chunks_file(cfg.SOURCES, graph, chunk_size)
