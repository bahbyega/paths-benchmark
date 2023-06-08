# Paths benchmark

Benchmark suits for performance study of various regular path querying algorithms and their implementations

---

## Dataset description

| **Graph**  | **Vertices** | **Edges** | **Labels** | **Link**            |
|------------|--------------|-----------|-------------------|----------           |
| enzyme     | 48.8K        | 86.5K     | 14                |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/enzyme/enzyme.tar.gz)     |
| eclass     | 239.1K       | 360.2K    | 10                |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/eclass/eclass.tar.gz)     |
| go         | 582.9K       | 1.4M      | 47                |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/graph-go/go.tar.gz)     |
| geospecies | 450.6K       | 2.2M      | 158               |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/geospecies/geospecies.tar.gz)     |
| taxonomy   | 5.7M         | 14.9M     | 21                |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/taxonomy/taxonomy.tar.gz)     |
| advogato   | 6K           | 51.1K     | 3                 |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/advogato/advogato.tar.gz)     |
| youtube    | 15K          | 27.3M     | 5                 |     [.tar.gz](https://pathsbenchmark.blob.core.windows.net/youtube/youtube.tar.gz)     |

It is possible to [download](https://pathsbenchmark.blob.core.windows.net/ds-all/paths-benchmark-ds.tar.gz) all graphs from the dataset with a single archive.

## Installation
You can install everything within your local python interpreter or virtual environment.
1. Install dependencies.
```
pip3 install pygraphblas
```

2. Download the source code of this repository.
```
git clone https://github.com/bahbyega/paths-benchmark.git
```

3. Within the repo folder init git submodule to get the source code of all the dependencies. 
```
git sumbodule --init --recursive
```

## How to install tools for comparison
#### Tensor
Tensor algorithm is a part of CFPQ_PyAlgo algorithms collection and will run without additional configuration after you have performed previous [installation](#installation) step successfully.

#### Souffle
Follow [this page](https://souffle-lang.github.io/install) for `Soufflé` installation.

## How to download and prepare dataset
1. Download dataset containing all the graphs and extract it into [`data/Graphs`](./data/Graphs) folder. Note that `data/Graphs/txt` now contains all the graphs.
2. Run [`scripts/initialize.py`](./scripts/initialize.py) to prepare graphs and generate queries.
```
python3 scripts/initialize.py
```

## How to run benchmark

1. Run [`benchmark/run_benchmark.py`](./benchmark/run_benchmark.py) to run specific benchmark.
```
python3 benchmark/run_benchmark.py [--algo] [--data] [--result] [--scenario]
```

# License
This project is under the MIT License.