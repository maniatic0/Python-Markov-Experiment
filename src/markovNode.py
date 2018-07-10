
from operator import itemgetter
from random import uniform
from base64 import b64encode, b64decode

from markovNodeSetAbstract import MarkovNodeSetAbstract

class MarkovNode ():
    # Instance Methods
    def __init__(self, name, markovSet):
        self.name = name
        self.dirty = False
        self.transitions = {}
        self.totalTransitions = 0
        self.nextList = []
        self.markovSet = markovSet

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

    def fixTransitions(self):
        if not self.dirty:
            return

        # Get transitions as a list
        self.nextList = list(self.transitions.items())

        floatTotalTransitions = float(self.totalTransitions)

        # Normalize weights
        for transition in self.nextList:
            transition[1] = float(transition[1]) / floatTotalTransitions

        # Sort by weight
        self.nextList.sort(key=itemgetter(1))

        self.dirty = False
        
    def getRandomNext(self):
        if self.dirty:
            self.fixTransitions()
        
        p = uniform(0.0, 1.0)

        for node in self.nextList:
            p -= node[1]
            if p <= 0.0:
                return node[0]

        raise ValueError('We went out of array')
