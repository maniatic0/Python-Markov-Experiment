
import os
import json
from base64 import b64decode

from src.markovNode import MarkovNode, NodeType
from src.markovNodeSet import MarkovNodeSet

class Markov ():
    VERSION = 1
    VERSION_JSON_STRING = "version"
    SPECIAL_NODES_JSON_STRING = "specialNodes"
    NODES_JSON_STRING = "nodes"

    def __init__(self, filename=None, predictionMax=50):
        self.filename = filename
        self.predictionMax = predictionMax

        self.markovSet = MarkovNodeSet()

        self.startNode = MarkovNode("", self.markovSet, NodeType.START_NODE)
        self.endNode = MarkovNode(" ", self.markovSet, NodeType.END_NODE)
        self.newLineNode = MarkovNode("\n", self.markovSet, NodeType.NEWLINE_NODE)        

        if self.filename is not None and os.path.isfile(self.filename):
            self.jsonLoad(self.filename)

    
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
            
            if lenLines > 1 and lineNumber < lenLines - 1 and len(words) != 0:
                self.startNode.addTransition(prevWord)
                prevWord.addTransition(self.newLineNode)
                prevWord = self.newLineNode

            lineNumber += 1

        if lenLines != 0:
            prevWord.addTransition(self.endNode)
        
    
    def learnFromFile(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.learnFromText(f.read())
            f.close()

    def cleanDirty(self):
        self.markovSet.cleanDirty()

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

    def jsonDict(self):
        specialNodes = {}

        specialNodes["{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, NodeType.START_NODE)] \
            = self.startNode.jsonDict()

        specialNodes["{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, NodeType.END_NODE)] \
            = self.endNode.jsonDict()

        specialNodes["{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, NodeType.NEWLINE_NODE)] \
                = self.newLineNode.jsonDict()
        

        resp = {
            Markov.VERSION_JSON_STRING : Markov.VERSION,
            Markov.SPECIAL_NODES_JSON_STRING : specialNodes, 
            Markov.NODES_JSON_STRING : self.markovSet.jsonDict()
            }
        return resp

    def jsonDump(self, indent=0):
        return json.dumps(self.jsonDict(), indent=indent)

    def jsonSave(self, indent=0):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.jsonDump(indent=indent))
            f.close()

    def jsonLoad(self, filename):
        jsonDump = None
        with open(filename) as f:
            jsonDump = json.loads(f.read())
            f.close()

        specialNodes = jsonDump[Markov.SPECIAL_NODES_JSON_STRING]
        transitions = jsonDump[Markov.NODES_JSON_STRING]

        startNodeStr = "{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, NodeType.START_NODE)
        endNodeStr = "{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, NodeType.END_NODE)
        newlineNodeStr = "{0!s}{1!s}".format(MarkovNode.NODE_TYPE_SEPARATOR, NodeType.NEWLINE_NODE)

        for node in specialNodes[startNodeStr].items():
            name = b64decode(node[0].encode('utf-8')).decode('utf-8')
            loadedNode = self.markovSet.getOrCreateNode(name)
            self.startNode.addTransition(loadedNode, weight=int(node[1]))

        for node in specialNodes[newlineNodeStr].items():
            if node[0] == endNodeStr:
                self.newLineNode.addTransition(self.endNode, weight=int(node[1]))
            else:
                name = b64decode(node[0].encode('utf-8')).decode('utf-8')
                loadedNode = self.markovSet.getOrCreateNode(name)
                self.newLineNode.addTransition(loadedNode, weight=int(node[1]))
            

        for node in transitions.items():
            name = b64decode(node[0].encode('utf-8')).decode('utf-8')
            loadedNode = self.markovSet.getOrCreateNode(name)
            loadedTransitions = node[1]
            for transition in loadedTransitions.items():
                if transition[0] == newlineNodeStr:
                    loadedNode.addTransition(self.newLineNode, weight=int(transition[1]))
                elif transition[0] == endNodeStr:
                    loadedNode.addTransition(self.endNode, weight=int(transition[1]))
                else:
                    decodedTransition = b64decode(transition[0].encode('utf-8')).decode('utf-8')
                    transitionNode = self.markovSet.getOrCreateNode(decodedTransition)
                    loadedNode.addTransition(transitionNode, weight=int(transition[1]))


        #print(jsonDump)

        


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
