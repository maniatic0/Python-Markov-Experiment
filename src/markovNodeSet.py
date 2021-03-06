
from base64 import b64encode

from src.markovNode import MarkovNode
from src.markovNodeSetAbstract import MarkovNodeSetAbstract

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

    def getNodesAmount(self):
        return len(self.nodes.items())

    def __repr__(self):
        representation = "MarkovNodeSet(size={0!r}, nodes=\n".format(self.getNodesAmount())
        for node in self.nodes.items():
            representation += "\t({0!r}, {1!r})\n".format(node[0], node[1])
        representation += ")"
        return representation

    def __str__(self):
        representation = "MarkovNodeSet(size={0!s}, nodes=\n".format(self.getNodesAmount())
        for node in self.nodes.items():
            representation += "\t({0!s}, {1!s})\n".format(node[0], node[1])
        representation += ")"
        return representation

    def jsonDict(self):
        resp = {}
        for node in self.nodes.items():
            resp[b64encode(node[0].encode('utf-8')).decode('utf-8')] = node[1].jsonDict()
        return resp