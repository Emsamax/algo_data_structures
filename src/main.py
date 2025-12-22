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
    trie.visualize("graphs/dataset_1", "prefix trie made with dataset n°1", True)
