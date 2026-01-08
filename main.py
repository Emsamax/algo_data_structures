import data_loader
from trie import prefix_trie
from array import suffix_array
import argparse
import cProfile
import pstats
from io import StringIO


def run_suffix_array_benchmark(words, random_words, start, stop, args):
    """Run suffix array operations"""
    struct = suffix_array()

    # insert
    for word in words:
        struct.insert(word)
    # visualize
    if args.graph:
        struct.visualize(
            "graphs/",
            f"suffix_array_dataset_{args.dataset}",
            f"Suffix Array visualization - Dataset {args.dataset}",
        )

    # range search
    result = struct.range_search(start, stop)

    # search suffixes
    suffixes = data_loader.get_random_suffixes(words)
    for suffix in suffixes:
        result = struct.search(suffix)

    # remove
    for word in random_words:
        struct.remove(word)

    # search again after removal
    for suffix in suffixes:
        result = struct.search(suffix)

    return struct


def run_prefix_trie_benchmark(words, random_words, start, stop, args):
    """Run prefix trie operations"""
    struct = prefix_trie()

    # insert
    for word in words:
        struct.insert(word=word)
    # visualize
    if args.graph:
        struct.visualize(
            "graphs/",
            f"prefix_trie_dataset_{args.dataset}",
            f"Prefix trie made with dataset n°{args.dataset}",
            True,
        )

    # range search
    struct.range_search(start, stop, current=None, current_word="", result=None)

    # search
    for word in random_words:
        struct.search(word=word)

    # remove
    for word in random_words:
        struct.remove(word=word, verbose=False)

    # search again
    for word in random_words:
        struct.search(word=word)

    return struct


def print_profile_results(profiler, output_file=None):
    """Print and optionally save profiling results"""
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)

    # Sort by cumulative time
    stats.sort_stats("cumulative")
    stats.print_stats(20)  # Top 20 functions

    result = s.getvalue()
    print("\n" + "=" * 80)
    print("PROFILING RESULTS - Top 20 functions by cumulative time")
    print("=" * 80)
    print(result)

    if output_file:
        with open(output_file, "w") as f:
            f.write(result)
        print(f"\nProfiling results saved to: {output_file}")


if __name__ == "__main__":

    datasets = {
        1: "datasets/dataset_1.txt",
        2: "datasets/dataset_2.txt",
        3: "datasets/dataset_3.txt",
    }

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Script that runs prefix_trie or suffix array algorithms for benchmarking

Both algorithms are tested on the same scenario:
  - First insert all the words
  - Select 2 random words then proceed to do a range search
  - Search for random words in this trie or array (1/10 of original dataset)
  - Remove those words
  - Search for them again
""",
    )

    # Algorithm arguments
    algo_group = parser.add_mutually_exclusive_group(required=True)
    algo_group.add_argument("--trie", action="store_true", help="prefix trie algorithm")
    algo_group.add_argument(
        "--array", action="store_true", help="suffix array algorithm"
    )

    # Dataset
    parser.add_argument(
        "--dataset",
        "-d",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="choose a dataset: 1 (100 words), 2 (1000 words), 3 (10000 words)",
    )

    parser.add_argument(
        "--invert", "-i", action="store_true", help="invert all words before insertion"
    )

    parser.add_argument(
        "--graph",
        "-g",
        action="store_true",
        help="generate a graph (not recommended for datasets 2 and 3)",
    )

    parser.add_argument(
        "--profile",
        "-p",
        action="store_true",
        help="enable cProfile profiling and save results",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="print detailed output during operations",
    )

    args = parser.parse_args()

    # Load data
    words = data_loader.load_data(datasets[args.dataset])

    if args.invert:
        words = data_loader.inverse(words)

    random_words = data_loader.get_slice(words, pair=False)
    range_pair = data_loader.get_slice(words, pair=True)
    start = range_pair[0]
    stop = range_pair[1]

    # Create profiler if requested
    profiler = cProfile.Profile() if args.profile else None

    # Run benchmark
    if args.profile:
        profiler.enable()

    if args.array:
        algo_name = "suffix_array"
        if args.verbose:
            print(f"\n{'='*60}")
            print(f"Running SUFFIX ARRAY on dataset {args.dataset}")
            print(f"Words: {len(words)}, Range: [{start}, {stop}]")
            print(f"{'='*60}\n")

        struct = run_suffix_array_benchmark(words, random_words, start, stop, args)

    else:  # trie
        algo_name = "prefix_trie"
        if args.verbose:
            print(f"\n{'='*60}")
            print(f"Running PREFIX TRIE on dataset {args.dataset}")
            print(f"Words: {len(words)}, Range: [{start}, {stop}]")
            print(f"Inverted: {args.invert}")
            print(f"{'='*60}\n")

        struct = run_prefix_trie_benchmark(words, random_words, start, stop, args)

    if args.profile:
        profiler.disable()

        # Create profiling directory
        import os

        os.makedirs("profiling", exist_ok=True)

        # Save profile data
        profile_filename = f"profiling/{algo_name}_dataset{args.dataset}"
        if args.invert:
            profile_filename += "_inverted"

        # Save .prof file for visualization tools
        profiler.dump_stats(f"{profile_filename}.prof")
        print(f"\nProfile data saved to: {profile_filename}.prof")

        # Print and save text results
        print_profile_results(profiler, f"{profile_filename}.txt")

        print("\n" + "=" * 80)
        print("To visualize with snakeviz: snakeviz " + profile_filename + ".prof")
        print("=" * 80)
