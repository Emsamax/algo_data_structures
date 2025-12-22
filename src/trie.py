import numpy as np
from graphviz import Digraph
from queue import Queue


class trie_node:
    def __init__(self, text=""):
        self.text = text
        self.children = dict()
        self.is_end = False


class prefix_trie:

    def __init__(self):
        self.root = trie_node()

    def insert(self, word) -> None:
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

    def remove(self, word) -> None:
        """
        :param word to remove from the trie
        """
        pass

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

    def range_search(self, start: str, stop: str) -> np.array:
        """
        return all words inside the range
        :param start of the range
        :param stop of the range
        """
        pass

    def visualize(self, filename: str, comment: str, render: bool) -> None:
        current = self.root
        diagram = Digraph(name=filename, comment=comment)
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

        o = open(filename + ".gv", "w")
        o.write(diagram.source)
        if render:
            diagram.render(filename + ".gv", view=False)
        o.close()
