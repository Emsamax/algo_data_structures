import numpy as np
from graphviz import Digraph
from queue import Queue


class trie_node:
    def __init__(self, text="") -> None:
        self.text = text
        self.children = dict()
        self.is_end = False


class prefix_trie:

    def __init__(self):
        self.root = trie_node()

    def __checkword(self, word: str, start: str, stop: str) -> bool:
        return start <= word <= stop

    def insert(self, word: str) -> None:
        """
        :param word to insert in the trie
        """
        current = self.root
        for char in word:
            # if char not in child create a new child with it
            if char not in current.children:
                current.children[char] = trie_node(char)

            # set current node to children
            current = current.children[char]
        current.is_end = True

    def remove(self, word: str, verbose: bool = False) -> None:
        """
        :param word to remove from the trie
        """
        current = self.root
        # branch that represent the word to delete
        trie_branch = [current]
        # get nodes
        for char in word:
            current = current.children.get(char)
            # word does not exist
            if current is None:
                return
            trie_branch.append(current)
        # set last node.isEnd to false
        current.is_end = False
        # loop from last to root node
        # len(trie_branch) to start at the second last node to check last node children
        for current_id in range(len(trie_branch) - 2, -1, -1):
            current = trie_branch[current_id]
            child_id = current_id + 1
            # find the char of the child to delete
            child_char = None
            for char, node in current.children.items():
                if node == trie_branch[child_id]:
                    child_char = char
                    break
            if verbose:
                print("{", end="")
                for node in trie_branch:
                    print(node.text, end=",")
                print("}", end="")
                print("\ncurrent ", current.text)
                print("child char", child_char)

            # another word from this prefix
            if len(current.children) > 1:
                # del current char
                del trie_branch[current_id].children[child_char]
                # break to stop deleting
                break

            # current have childrends -> del childrens
            if trie_branch[current_id].children:
                del trie_branch[current_id].children[child_char]

    def search(self, word: str) -> bool:
        """
        :param word to search
        """
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end

    def range_search(
        self,
        start: str,
        stop: str,
        current: trie_node = None,
        current_word: str = "",
        result: list = None,
    ) -> np.array:
        """
        return all words inside the range (it's a dfs with range)
        :param start of the range
        :param stop of the range
        """
        if current is None:
            current = self.root
        if result is None:
            result = []

        # check if range in trie
        if not (self.search(start) | self.search(stop)):
            print("invalid range, not in the trie ", start, " ", stop)
            return

        if current.is_end:
            if self.__checkword(current_word, start, stop):
                result.append(current_word)
            elif current_word > stop:
                return np.array(result)

        # get all childrens alphabetically sorted
        sort_childs = sorted(current.children.keys())
        for char in sort_childs:
            # update word and child
            child = current.children[char]
            new_word = current_word + char
            # dont expolore if new word outside of the range
            if new_word > stop:
                break
            # recursif call
            self.range_search(start, stop, child, new_word, result)

        # return array only at root level
        if current == self.root:
            return np.array(result)
        return None

    
        current = self.root
        diagram = Digraph(name=filename, comment=comment, directory=directory)
        node_id = 0
        diagram.node(str(node_id), self.root.text)
        q = Queue()
        q.put((self.root, node_id))
        while not q.empty():
            current, parent_index = q.get()
            for char, child_node in current.children.items():
                node_id += 1
                # put value in node
                if child_node.is_end:
                    diagram.node(
                        str(node_id),
                        char,
                        fillcolor="darkgreen",
                        shape="circle",
                        style="filled",
                    )
                diagram.node(str(node_id), char, shape="circle")
                # draw edges
                diagram.edge(str(parent_index), str(node_id))
                q.put((child_node, node_id))

        o = open(directory + filename + ".gv", "w")
        o.write(diagram.source)
        if render:
            diagram.render(filename + ".gv", view=False, overwrite_source=True)
        o.close()
