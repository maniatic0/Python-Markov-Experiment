#!/usr/bin/env python3.6

import sys

from src.markov import Markov

def main(filename, textsToLearn=[]):
    mark = Markov(filename, 200)
    for text in textsToLearn:
        mark.learnFromFile(text)

    print(mark.generateText())

    

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main(sys.argv[1], sys.argv[2:])
    else:
        main(sys.argv[1])
