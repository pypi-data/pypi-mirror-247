from pyodm.utils.search.dfs import DFS
import pyodm.model.definition as Model


class ODMDfs(DFS):

    def pruning_strategy(self, node) -> bool:
        return True

    def __init__(self, data, cached=False):
        super().__init__(data, cached)

    def neighbor_node(self, node):
        __neighbor = []
        for element in vars(node).values():
            if isinstance(element, Model.OneElement):
                __neighbor.append(element)
            elif isinstance(element, Model.ManyElements):
                for i in element.array:
                    __neighbor.append(i)
        return __neighbor
