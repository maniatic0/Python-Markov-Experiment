
from operator import itemgetter
from random import uniform
from base64 import b64encode, b64decode
from enum import IntEnum, unique

from src.markovNodeSetAbstract import MarkovNodeSetAbstract

@unique
class NodeType (IntEnum):
    START_NODE = 0
    END_NODE = 1
    NEWLINE_NODE = 2
    NORMAL = 3

class MarkovNode ():
    NODE_TYPE_SEPARATOR = '&'
    # Instance Methods
    def __init__(self, name, markovSet, nodeType=NodeType.NORMAL):
        self.name = name
        self.nodeType = nodeType
        self.dirty = False
        self.transitions = {}
        self.totalTransitions = 0
        self.nextList = []
        self.markovSet = markovSet

    def getName(self):
        return self.name

    def getNameBase64(self):
        return b64encode(self.getName().encode('utf-8')).decode('utf-8')

    def addTransition(self, nextNode, weight=1):
        if nextNode is None:
            return

        if not self.dirty:
            self.markovSet.markAsDirty(self)
            self.dirty = True

        if nextNode in self.transitions:
            self.transitions[nextNode] += weight
        else:
            self.transitions[nextNode] = weight

        self.totalTransitions += weight

    def fixTransitionsNoUpdateSet(self):
        if not self.dirty:
            return

        # Get transitions as a list and normalize
        floatTotalTransitions = float(self.totalTransitions)

        self.nextList = [(transition[0], float(transition[1]) / floatTotalTransitions) \
                            for transition in self.transitions.items()]

        # Sort by weight
        self.nextList.sort(key=itemgetter(1))

        self.dirty = False

    def fixTransitions(self):
        self.fixTransitionsNoUpdateSet()
        self.markovSet.markAsClean(self)

    def getRandomNext(self):
        if self.dirty:
            self.fixTransitions()

        if self.totalTransitions == 0:
            return None

        p = uniform(0.0, 1.0)

        for node in self.nextList:
            p -= node[1]
            if p <= 0.0:
                return node[0]

        raise ValueError('We went out of array')

    def __repr__(self):
        representation = "markovNode(name={0!r}, transitions=[" \
            .format(self.getNameBase64())

        transitionLast = len(self.transitions.items())-1
        transitionIndex = 0

        for elem in self.transitions.items():
            representation += "({0!r}, {1!r})" \
                .format(elem[0].getNameBase64(), elem[1])
            if transitionIndex != transitionLast:
                representation += ', '
            transitionIndex += 1
        representation += "])"
        return representation

    def __str__(self):
        representation = "markovNode(name={0!s}, transitions=[".format(self.name)

        transitionLast = len(self.transitions.items())-1
        transitionIndex = 0

        for elem in self.transitions.items():
            representation += "({0!s}, {1!s})" \
                .format(elem[0].getName(), elem[1])
            if transitionIndex != transitionLast:
                representation += ', '
            transitionIndex += 1
        representation += "])"
        return representation

    def jsonDict(self):
        resp = {}
        for transition in self.transitions.items():
            if transition[0].nodeType == NodeType.NORMAL:
                resp[transition[0].getNameBase64()] = transition[1]
            else:
                resp[ \
                    "{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, transition[0].nodeType) \
                    ] = transition[1]

        return resp
