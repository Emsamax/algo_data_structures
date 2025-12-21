import data_loader, prefix_trie, suffix_array

datasets = {
    "DATASET_1": "datasets/dataset_1.txt",
    "DATASET_2": "datasets/dataset_2.txt",
    "DATASET_3": "datasets/dataset_3.txt",
}


if __name__ == "__main__":

    dataset_1 = data_loader.load_data(datasets["DATASET_1"]);
    print(dataset_1)
    print(data_loader.inverse(dataset_1))
