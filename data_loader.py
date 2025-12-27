# for sequential memory data structure
import numpy as np


def load_data(filepath: str) -> np.array:
    """
    Load all examples from a dataset in memory with an array
    :param str filepath
    """
    file = open(filepath, "r", encoding="utf-8")
    content = file.read()

    # clean file and remove specaol chars '[' && ']'
    content = content.strip()
    content = content.replace("[", "").replace("]", "")

    # using regular array because because can't add from a loop
    arr = []
    for word in content.split(","):
        # clean once more
        word = word.strip().strip('"').strip("'")
        # add if word
        if word:
            arr.append(word)
    # convert array to ndattay
    result = np.array(arr)
    return result


def inverse(words: np.array) -> np.array:
    """
    inverse all words present in the given array
    :param array
    """
    return np.array([word[::-1] for word in words])


def get_slice(dataset: np.array, pair: bool) -> np.array:
    """
    Return an array with len of 1/10 of the original dataset
    filled with random words

    :param self: self
    :param dataset: list of words
    :type dataset: np.array
    :param pair if true return a pair of sorted random words (useful for range search)
    :return: the randoms words form the given dataset
    :rtype: np.array
    """
    if pair:
        size = 2
        # sorted alphabetically
        selected = np.random.choice(dataset, size=size, replace=False)
        return sorted([str(word) for word in selected])

    else:
        size = len(dataset) // 10
        return np.random.choice(dataset, size=size, replace=False)


def get_random_suffixes(words: np.array) -> np.array:
    """
    generate random suffixes for all words given
    :param words: Description
    :type words: np.array
    :return: Description
    :rtype: Any
    """
    suffixes = []

    for word in words:
        if len(word) > 2:
            start_pos = np.random.randint(0, len(word) - 1)
            suffix = word[start_pos:]
            suffixes.append(suffix)
        else:
            suffixes.append(word)

    return np.array(suffixes)
