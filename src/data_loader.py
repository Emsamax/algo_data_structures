# for sequential memory data structure
import numpy as np


"""
Load all examples from a dataset in memory with an array
:param str filepath 
"""


def load_data(filepath: str) -> np.ndarray:
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


"""
inverse all words present in the given array
:param array 
"""


def inverse(words: np.ndarray) -> np.ndarray:
    return np.array([word[::-1] for word in words])
