#!/usr/bin/env python3.6

import sys

from src.markov import Markov

def main(filename, textsToLearn=[]):
    mark = Markov(filename, 300)
    for text in textsToLearn:
        mark.learnFromFile(text)

    mark.cleanDirty()

    texto = mark.generateText()

    with open("test/texto.txt", 'w', encoding='utf-8') as f:
        f.write(texto)
        f.close()

    #mark.jsonSave(indent=4)
    

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2:])
    else:
        main(sys.argv[1])
