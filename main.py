import data_loader
from trie import prefix_trie
from array import suffix_array
import argparse

# TODO : visualize finction for array
# TODO : normalize console output (same format for trie/array algo)
# FIXME : range search isn't working
# TODO : benchmarking with hyperfind and cProfile
# TODO : write seminar


if __name__ == "__main__":

    datasets = {
        1: "datasets/dataset_1.txt",
        2: "datasets/dataset_2.txt",
        3: "datasets/dataset_3.txt",
    }
    parser = argparse.ArgumentParser(
        # preserve string format
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Script that runs prefix_trie or suffix array algorithms for benchmarking with hyperfine

Both algorithms are tested on the same scenario:
  - First insert all the words
  - Select 2 random words then proceed to do a range search
  - Search for random words in this trie or array (1/10 of original dataset)
  - Remove those words
  - Search for them again
 
""",
    )

    # algo arguments, mutually exclusive
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

    args = parser.parse_args()
    # load the specified dataset
    words = data_loader.load_data(datasets[args.dataset])

    if args.invert:
        # invert words before insertion if needed
        words = data_loader.inverse(words)

    random_words = data_loader.get_slice(words, pair=False)
    range = data_loader.get_slice(words, pair=True)
    start = range[0]
    stop = range[1]

    # print(random_words)
    # print(range)

    struct = None
    # scenarios

    print(range)

    if args.array:
        """
        ARRAY
        """
        struct = suffix_array()
        # insert words
        for word in words:
            struct.insert(word)

        if args.graph:
            struct.visualize(
                "graphs/", "array_dataset_1", "prefix trie made with dataset n°1", True
            )

        # 1 range search
        print("=" * 30)
        print("RANGE SEARCH")
        print("=" * 30)
        print(struct.range_search(start, stop))
        suffixes = data_loader.get_random_suffixes(words)

        # 2 search
        for suffix in suffixes:
            result = struct.search(suffix)
            print(f"Words with suffix '{suffix}': {result}")

        # 3 remove
        for word in words:
            print(f"remove word : '{word}'")
            struct.remove(word)
        # 4 search again
        for suffix in suffixes:
            result = struct.search(suffix)
            print(f"Words with suffix '{suffix}': {result}")

    else:
        """
        TRIE
        """
        # init trie
        struct = prefix_trie()
        for word in words:
            struct.insert(word=word)

        if args.graph:
            struct.visualize(
                "graphs/", "dataset_1", "prefix trie made with dataset n°1", True
            )

        print(
            struct.range_search(start, stop, current=None, current_word="", result=None)
        )
        # 2 search
        for word in random_words:
            print(word, " found  : ", struct.search(word=word))
        # 3 remove
        for word in random_words:
            struct.remove(word=word, verbose=False)
        # 4 search again
        for word in random_words:
            print(word, " found  : ", struct.search(word=word))
