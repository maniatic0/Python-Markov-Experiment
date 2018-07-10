
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
            node.fixTransitionsNoUpdateSet()
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

    def __repr__(self):
        representation = "MarkovNodeSet(size={0!r}, nodes=\n".format(len(self.nodes.items()))
        for node in self.nodes.items():
            representation += "\t({0!r}, {1!r})\n".format(node[0], node[1])
        representation += ")"
        return representation

    def __str__(self):
        representation = "MarkovNodeSet(size={0!s}, nodes=\n".format(len(self.nodes.items()))
        for node in self.nodes.items():
            representation += "\t({0!s}, {1!s})\n".format(node[0], node[1])
        representation += ")"
        return representation