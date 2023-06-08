import time
import csv
import os
import datetime
import shutil
import sys
import subprocess
from os.path import exists
from tqdm import tqdm
from time import time

from deps.CFPQ_PyAlgo.src.graph.graph import Graph
from deps.CFPQ_PyAlgo.src.problems.MultipleSource.algo.matrix_bfs_ms.reg_automaton import RegAutomaton
from deps.CFPQ_PyAlgo.deps.CFPQ_Data.cfpq_data.grammars.readwrite.cfg import cfg_from_txt

import scripts.dataset as ds
import scripts.config as config
from scripts.gen_chunks import select_number_source_verts


def result_folder(folder):
    """
    Creates and returns an unused result directory
    @param folder: Path to result folder
    @return: path to new directory
    """
    if not os.path.exists(folder):
        os.mkdir(folder)

    now = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
    result_folder = os.path.join(folder, now)

    os.mkdir(result_folder)
    return result_folder

def parse_config():
    """
    Returns information about which graph with which grammar to run
    @param config: Path to csv file with header:["Graph", "Grammar"]
    @return: dictionary in which keys are paths to graphs and values are paths to grammars
    """
    graph_grammar = dict()
    for graph in ds.BENCH_GRAPHS:
        for query in ds.BENCH_QUERIES_PATHS_DATALOG:
            if graph.filepath in graph_grammar:
                graph_grammar[graph.filepath].append(query)
            else:
                graph_grammar[graph.filepath] = [query]

    return graph_grammar

def init_result_csv(graph_name, algo_name, result_dir):
    header_index = ['graph', 'grammar', 'size_chunk', 'time', 'num_reachable']
    result_file_path = result_dir.joinpath(f'{graph_name}-{algo_name}')

    append_header = False
    if not exists(result_file_path):
        append_header = True

    result_csv = open(result_file_path, mode='a', newline='\n')
    csv_writer_index = csv.writer(result_csv, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')

    if append_header:
        csv_writer_index.writerow(header_index)

    if not exists(result_file_path):
        csv_writer_index.writerow(header_index)

def write_chunks_file(result_dir, graph, graph_name, chunk_size):
    if not os.path.exists(result_dir):
            os.makedirs(result_dir)
    chunk_file_path = result_dir.joinpath(f'chunk-{graph_name}-{chunk_size}')
    chunk_csv = open(chunk_file_path, mode='a', newline='\n')
    chunk_writer = csv.writer(chunk_csv, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')

    chunks = []
    if chunk_size is None:  
        chunks = select_number_source_verts(graph.matrices_size, graph.matrices_size)
    else:
        chunks = select_number_source_verts(graph.matrices_size, chunk_size)
    
    for chunk in chunks:
        chunk_writer.writerow([chunk])

    return chunks

def read_chunks_file(chunk_file):
    chunks = []
    chunk_csv = open(chunk_file, mode='a', newline='\n')
    for line in chunk_csv.readlines():
        chunks.append(int(line.rstrip()))
    
    return chunks


def benchmark(algo, data_dir, result_dir, chunk_sizes=config.DEFAULT_CHUNK_SIZES, rounds=1):
    for _ in rounds:
        if algo[0] == "msbfs":
            benchmark_msbfs(algo, data_dir, result_dir, chunk_sizes)
        if algo[0] == "tensor":
            benchmark_tensor(algo, data_dir, result_dir, chunk_sizes)
        if algo[0] == "datalog":
            benchmark_datalog(algo, data_dir, result_dir, chunk_sizes)

def benchmark_msbfs(algo, data, result_dir, chunk_sizes=config.DEFAULT_CHUNK_SIZES, generate_chunks=False):
    """
    Measurement function for finding paths from set of vertices
    @param algo: concrete implementation of the algorithm
    @param data: dictionary in format {path to graph: list of paths to grammars}
    @param result_dir: directory for uploading results of measurement
    """
    algo_impl, algo_name = algo
    for graph in data:
        result_csv_writer = init_result_csv(graph.stem, algo_name, config.SOURCES)

        g = Graph.from_txt(graph)
        g.load_bool_graph()
        
        for chunk_size in chunk_sizes:
            if generate_chunks:
                chunks = write_chunks_file(result_dir, g, graph.stem, chunk_size)
            else:
                chunk_file = config.SOURCES.joinpath(f'chunk-{graph.stem}-{chunk_size}')
                chunks = read_chunks_file(chunk_file)

            for grammar in data[graph]:
                algo_impl.prepare(algo_impl, g, RegAutomaton.from_regex_txt(grammar))

                start = time()
                res = algo_impl.solve(algo_impl, chunks)
                finish = time()

                result_csv_writer.writerow(
                    [graph.stem, f"{grammar.parent.stem}-{grammar.stem}", len(chunks), finish - start, res[1]])

def benchmark_tensor(algo, data, result_dir, chunk_sizes=config.DEFAULT_CHUNK_SIZES, generate_chunks=False):
    """
    Measurement function for finding paths from set of vertices
    @param algo: concrete implementation of the algorithm
    @param data: dictionary in format {path to graph: list of paths to grammars}
    @param result_dir: directory for uploading results of measurement
    """
    algo_impl, algo_name = algo
    for graph in data:
        result_csv_writer = init_result_csv(graph.stem, algo_name, result_dir)

        g = Graph.from_txt(graph)
        g.load_bool_graph()

        for chunk_size in chunk_sizes:
            if generate_chunks:
                chunks = write_chunks_file(config.SOURCES, g, graph.stem, chunk_size)
            else:
                chunk_file = config.SOURCES.joinpath(f'chunk-{graph.stem}-{chunk_size}')
                chunks = read_chunks_file(chunk_file)

            for grammar in data[graph]:                
                algo_impl.prepare(algo_impl, g, cfg_from_txt(grammar))
                algo_impl.clear_src(algo)

                start = time()
                res = algo_impl.solve(algo_impl, chunks)
                finish = time()

                result_csv_writer.writerow(
                    [graph.stem, f"{grammar.parent.stem}-{grammar.stem}", len(chunks), finish - start, res[0].matrix_S.nvals])

def init_datalog_interpretation(grammar_path, facts_path):
    interpret_cmd = []
    interpret_cmd.append("souffle") # instance (use globally installed)
    interpret_cmd.append(f"{grammar_path}")
    interpret_cmd.append(f"-p {facts_path}/profile --emit-statistics")
    interpret_cmd.append("-F")
    interpret_cmd.append(f"{facts_path}")
    interpret_cmd.append("-j")
    interpret_cmd.append(f"4") # num cores

    return " ".join(interpret_cmd)

def init_datalog_compilation(grammar_path, facts_path, binary_path):
    compile_cmd = []
    compile_cmd.append("souffle") # instance
    compile_cmd.append("--magic-transform=path")
    compile_cmd.append("-c")
    compile_cmd.append(f"{grammar_path}")
    # compile_cmd.append(f"--auto-schedule={facts_path}/profile") 
    compile_cmd.append("-F")
    compile_cmd.append(f"{facts_path}")
    compile_cmd.append("-j")
    compile_cmd.append(f"4") # num cores
    compile_cmd.append(f"-o")
    compile_cmd.append(binary_path)

    return " ".join(compile_cmd)

def benchmark_datalog(algo, data, result_dir, chunk_sizes=config.DEFAULT_CHUNK_SIZES, generate_chunks=False):
    _, algo_name = algo
    for graph in data:
        result_csv_writer = init_result_csv(graph.stem, algo_name, result_dir)

        for chunk_size in chunk_sizes:
            for grammar in data[graph]:
                if not generate_chunks:
                    facts_path = config.GRAPHS / "facts" / graph.stem
                    source_file = config.SOURCES.joinpath(f"chunk-{graph.stem}-{chunk_size}")
                    shutil.copyfile(source_file, facts_path / "source.facts")

                    binary = f"{facts_path}/eval"

                    compile_cmd = init_datalog_compilation(grammar, facts_path, binary)
                    status = subprocess.run(compile_cmd, capture_output=True, text=True, shell=True)

                    if status.returncode != 0:
                        sys.stderr.write(status.stderr)
                        sys.stdout.write(status.stdout)
                    
                    start = time()
                    status = subprocess.run(f"{binary}", capture_output=True, text=True, shell=True)
                    finish = time()

                    if status.returncode != 0:
                        sys.stderr.write(status.stderr)
                        sys.stdout.write(status.stdout)

                    os.remove(facts_path / "source.facts")
                    num_reachable = sum(1 for _ in open("path.csv", 'rb'))

                    result_csv_writer.writerow([graph.stem, f"{grammar.parent.stem}-{grammar.stem}", chunk_size, finish - start, num_reachable])