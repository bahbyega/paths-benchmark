import argparse
from pathlib import Path

import scripts.config as cfg
import scripts.dataset as ds
from bench_scenario import benchmark

if __name__ == "__name__":
    parser = argparse.ArgumentParser(description="Run benchmark in certain scenario.")
    parser.add_argument("-a", "--algo", help=f"Specify algo to be used: {ds.ALGO_NAMES}")
    parser.add_argument("-d", "--data", help="Specify data folder")
    parser.add_argument("-r", "--result", help="Specify result folder")
    parser.add_argument("-s", "--scenario", choices=cfg.DEFAULT_CHUNK_SIZES, nargs="+",
                        help="Specify specific scenarios (start vertices count).")

    args = parser.parse_args()

    data_dir = cfg.DATA
    if args.data is not None:
        data_dir = Path(args.data)

    result_dir = Path("result")
    if args.result is not None:
        result_dir = Path(args.result)

    if args.senario is not None:
        chunk_sizes = [int(x) for x in args.scenario]

    assert args.algo in ds.ALGO_NAMES 
    benchmark((ds.ALGO_NAMES[args.algo], args.algo), data_dir, result_dir)