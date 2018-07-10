
from markovNode import MarkovNode
from markovNodeSetAbstract import MarkovNodeSetAbstract

class MarkovNodeSet (MarkovNodeSetAbstract) :

    def __init__(self):
        self.nodes = {}
        self.dirtyNodes = set()

    def markAsDirty(self, node):
        self.dirtyNodes.add(node)

    def markAsClean(self, node):
        self.dirtyNodes.remove(node)

    def cleanDirty(self):
        for node in self.dirtyNodes:
            node.fixTransitions()
        self.dirtyNodes.clear()

    def getNode(self, name):
        node = self.nodes.get(name)
        return node

    def _createNode(self, name):
        self.nodes[name] = MarkovNode(name, self)
        return self.nodes[name]

    def createNode(self, name):
        possibleNode = self.getNode(name)

        if possibleNode is not None:
            return possibleNode
        else:
            return self._createNode(name)

    def getOrCreateNode(self, name):
        node = self.getNode(name)

        if node is None:
            return self._createNode(name)
        else:
            return node