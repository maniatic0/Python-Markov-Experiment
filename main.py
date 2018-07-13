#!/usr/bin/env python3.6

import argparse

from src.markov import Markov, markovMain
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser( \
        description='Control Markov Chain Text Generator by Christian Oliveros.')

    parser.add_argument('-mf', '--markovFile', metavar='filename', \
        help='Where is the JSON file to load and save the Markov Set', default=None)
    parser.add_argument('-t', '--textsToLearn', nargs='*', metavar='filename',\
        help='Texts to Learn', default=[])
    parser.add_argument('-mp', '--maxPredictions', metavar='N', \
        help='Maximum number of words in the generated text', default=100, type=int)
    parser.add_argument('-sm', '--saveMarkov', metavar='B', \
        help='If the Markov Set is to be save to the file ', default=True, type=bool)
    parser.add_argument('-ji', '--jsonIndent', metavar='N', \
        help='Indentation of the JSON file', default=4, type=int)
    parser.add_argument('-mo', '--markovOutput', metavar='filename', \
        help='Where to save the output. If none is provided the generated text is printed on terminal', \
        default=None)
    
    args = parser.parse_args()
    markovMain(args.markovFile, args.textsToLearn, args.maxPredictions, \
        args.saveMarkov, args.jsonIndent, args.markovOutput)
