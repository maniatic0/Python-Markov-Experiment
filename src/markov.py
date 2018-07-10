
import os

from markovNode import MarkovNode

class Markov ():
    startNode = MarkovNode("")
    endNode = MarkovNode(" ")
    newLineNode = MarkovNode("\n")

    @staticmethod
    def init(filename):
        pass
    
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
    