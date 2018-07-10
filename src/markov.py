
import os

from src.markovNode import MarkovNode
from src.markovNodeSet import MarkovNodeSet

class Markov ():

    def __init__(self, filename, predictionMax=50):
        self.filename = filename
        self.predictionMax = predictionMax
        self.markovSet = MarkovNodeSet()
        self.startNode = MarkovNode("", self.markovSet)
        self.endNode = MarkovNode(" ", self.markovSet)
        self.newLineNode = MarkovNode("\n", self.markovSet)

    
    def learnFromText(self, text):
        lines = text.splitlines()
        lenLines = len(lines)

        lineNumber = 0
        prevWord = self.startNode
        for line in lines:
            words = line.split()
            for word in words:
                nextWord = self.markovSet.getOrCreateNode(word)
                prevWord.addTransition(nextWord)
                prevWord = nextWord
            
            if lenLines > 1 and lineNumber < lenLines - 1:
                self.startNode.addTransition(prevWord)
                prevWord.addTransition(self.newLineNode)
                prevWord = self.newLineNode

            lineNumber += 1

        prevWord.addTransition(self.endNode)
        self.markovSet.cleanDirty()
    
    def learnFromFile(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.learnFromText(f.read())
            f.close()

    def generateText(self):
        # if there is nothing to generate
        if self.markovSet.getNodesAmount() == 0:
            return ""

        currentNode = self.startNode
        steps = 0
        generated = ""
        while steps <= self.predictionMax and currentNode != self.endNode:
            generated += " " + currentNode.getName()
            currentNode = currentNode.getRandomNext()
            steps += 1
        
        return generated

    def __repr__(self):
        representation = "Markov(filename={0!r}, predictionMax={1!r}, markovSet={2!r}\n" \
                            .format(self.filename, self.predictionMax, self.markovSet)
        return representation + ")"

    def __str__(self):
        representation = "Markov(filename={0!s}, predictionMax={1!s}, markovSet={2!s}\n" \
                            .format(self.filename, self.predictionMax, self.markovSet)
        return representation + ")"
        


def main():
    mark = Markov("")
    print("Markov: {0!r}".format(mark))
    print("Empty: " + mark.generateText())
    print("")
    
    aprender = "Hola me llamo pedro"
    print("Aprendiendo: {0!s}".format(aprender))
    mark.learnFromText(aprender)
    print("Markov: {0!r}".format(mark))
    print("First Try: " + mark.generateText())
    print("Second Try: " + mark.generateText())
    print("")

    aprender = "Hola me llamo juan"
    print("Aprendiendo: {0!s}".format(aprender))
    mark.learnFromText(aprender)
    print("Markov: {0!s}".format(mark))
    print("First Try: " + mark.generateText())
    print("Second Try: " + mark.generateText())
    print("Third Try: " + mark.generateText())
    print("")

    aprender = "Primera Linea \n Segunda Linea \n Tercera Linea \n me llamo miguel"
    print("Aprendiendo: {0!s}".format(aprender))
    mark.learnFromText(aprender)
    print("Markov: {0!s}".format(mark))
    print("First Try: " + mark.generateText())
    print("Second Try: " + mark.generateText())
    print("Third Try: " + mark.generateText())
    print("")

if __name__ == '__main__':
    main()
