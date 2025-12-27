import numpy as np


class suffix_array:

    def __init__(self) -> None:
        # dict used to have suffixes for each words
        self.words: dict[str, np.ndarray] = dict()
        # global alphabetically sorted suffix array of tuple (suffix, word) to find words faster by suffixes
        # can have duplicates suffixes -> used for search
        self.suffixes_array: np.ndarray = np.array([], dtype=object)

    def insert(self, word: str) -> None:
        """
        insert a word and all it's suffixes
        :param self: Description
        :param str: Description
        :type str: str
        :param index: Description
        :type index: int
        """
        if word in self.words:
            return

        new_suffixes = []
        for i in range(len(word)):
            suffix = word[i:]
            new_suffixes.append(suffix)
        # alphabetically sorted suffix by words
        new_suffixes = sorted(new_suffixes)

        # new dict entry
        self.words[word] = np.array(new_suffixes, dtype=str)
        new_tuples = [(suffix, word) for suffix in new_suffixes]

        # for each suffixes find and add new one then sort global suffix array again

        # Convert to list, add new tuples, sort, convert back
        if len(self.suffixes_array) == 0:
            all_tuples = new_tuples
        else:
            all_tuples = list(self.suffixes_array) + new_tuples

        # Sort and convert to np.array
        self.suffixes_array = np.array(
            sorted(all_tuples, key=lambda x: x[0]), dtype=object
        )

    def remove(self, word: str) -> None:
        """
        remove a word and all it's suffix
        :param self: Description
        """
        if word in self.words:
            # delete from dictionnary
            del self.words[word]
            # del all tuples with origin if = word
            new_array = self.suffixes_array = [
                (suffix, origin)
                for suffix, origin in self.suffixes_array
                if origin != word
            ]
            self.suffixes_array = np.array(new_array, dtype=object)

    def _binary_search(self, target: str) -> int:
        """
        binary search to find the first element >= target in the suffix array
        because search a word or many words by suffixes

        :type str: targeted word
        :return: the indice of the first string after target
        :rtype: int
        """
        left = 0
        right = len(self.suffixes_array)
        while left < right:
            middle = (left + right) // 2  # integer division
            # check ledt part of array
            if target <= self.suffixes_array[middle][0]:
                right = middle
            else:
                left = middle + 1
        return left

    def search(self, suffix: str) -> np.array:
        """
        find the words that start with this suffix
        (= not reversed words that start with this prefix)

        :param self: Description
        :param pattern: Description
        :type pattern: str
        :return: Description
        :rtype: ndarray[_AnyShape, dtype[Any]]
        """
        results = set()
        left = self._binary_search(suffix)

        # start from the first suffix after the given suffix till the end of the array
        for i in range(left, len(self.suffixes_array)):
            suf, word = self.suffixes_array[i]
            if suf.startswith(suffix):
                results.add(word)
            else:
                # No more matches in sorted array
                break

        return np.array(list(results), dtype=str)

    def range_search(self, start: str, stop: str) -> np.ndarray:
        """
        find all the the words with a suffix inside the range(start,stop)
        (= not reversed words that start with these prefixes)

        :param self: Description
        :param start: Description
        :type start: str
        :param stop: Description
        :type stop: str
        :return: Description
        :rtype: ndarray[_AnyShape, dtype[Any]]
        """
        pass

    def visualize(
        self,
        directory: str,
        filename: str,
        comment: str,
        render: bool,
    ) -> None:
        pass
