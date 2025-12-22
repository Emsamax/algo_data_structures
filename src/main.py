import data_loader
from trie import prefix_trie

datasets = {
    "DATASET_1": "datasets/dataset_1.txt",
    "DATASET_2": "datasets/dataset_2.txt",
    "DATASET_3": "datasets/dataset_3.txt",
}


if __name__ == "__main__":

    dataset_1 = data_loader.load_data(datasets["DATASET_1"])
    print(dataset_1)

    trie = prefix_trie()
    # init trie
    for word in dataset_1:
        trie.insert(word=word)

    # search for "ignorance"
    print(trie.search("ignorance"))
    trie.visualize("graphs/", "dataset_1", "prefix trie made with dataset n°1", True)

    little = dataset_1[::10]
    print(little)
    little_trie = prefix_trie()
    for word in little:
        little_trie.insert(word=word)
    print(little_trie.search("branchia"))
    little_trie.visualize(
        "graphs/", "little_before", "prefix trie before removing word branchia", True
    )
    little_trie.remove("branchia")
    little_trie.visualize(
        "graphs/", "little_after", "prefix trie after removing word branchia", True
    )
    print(little_trie.search("branchia"))
