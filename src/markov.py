
from operator import itemgetter

from random import uniform

class MarkovNode ():
    nodes = {}
    dirtyCount = 0

    # Instance Methods
    def __init__(self, name):
        self.name = name
        self.dirty = False
        self.transitions = {}
        self.totalTransitions = 0
        self.nextList = []
        MarkovNode.nodes[name] = self

    def addTransition(self, nextNode):
        if nextNode is None:
            return
        self.dirty = True
        MarkovNode.dirtyCount += 1

        if nextNode in self.transitions:
            self.transitions[nextNode] += 1
        else:
            self.transitions[nextNode] = 1

        self.totalTransitions += 1

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
        MarkovNode.dirtyCount -= 1
        
    def getRandomNext(self):
        if self.dirty:
            self.fixTransitions()
        
        p = uniform(0.0, 1.0)

        for node in self.nextList:
            p -= node[1]
            if p <= 0.0:
                return node[0]

        raise ValueError('We went out of array')

    # Static class methods

    @staticmethod
    def getNode(name):
        node = MarkovNode.nodes.get(name)
        return node

    @staticmethod
    def getOrCreateNode(name):
        node = MarkovNode.getNode(name)

        if node is None:
            return MarkovNode(name)
        else:
            return node


class Markov ():
    startNode = MarkovNode("")
    endNode = MarkovNode(" ")
    newLineNode = MarkovNode("\n")
    
    @staticmethod
    def processText(text):
        lines = text.splitlines()
        lenLines = len(lines)

        lineNumber = 0
        prevWord = Markov.startNode
        for line in lines:
            words = line.split()
            for word in words:
                nextWord = MarkovNode.getOrCreateNode(word)
                prevWord.addTransition(nextWord)
                prevWord = nextWord
            
            if lenLines > 1 and lineNumber < lenLines - 1:
                prevWord.addTransition(Markov.newLineNode)
                prevWord = Markov.newLineNode

            lineNumber += 1
    