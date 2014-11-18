"""
Artifcial Intelligence and Decision Systems Assignment 2, CNF converter
Authors: Simon Bilgeri, Rui Lopes
Year: 2014
Contact: Simon.Bilgeri@tum.de
"""
import sys

DEBUG = 1

def read_sentences(filename):
    # This function reads sentences in propositional logic from a file
    # input: filename of input file
    # output: List of tuples (sentences)
    # Open input file
    input_file = open(filename)
    # read first line and get L and C of matrix
    sentences = [eval(l.strip()) for l in input_file]  # read the sentences
    # remove empty lines
    sentences = [x for x in sentences if x]
    return sentences

def print_sentences(sentences):
    print('\n')
    for i in range(0,len(sentences)):
        print('(',i,') ', sentences[i]);
    return 1

def is_atom(sentence):
    if type(sentence)==str:
        return 1
    else:
        return 0

def is_negation(sentence):
    if len(sentence)==2:
        if sentence[0]=='not':
            return 1
        else:
            print('Input file contains errors!')
            exit(-1)
    else:
        return 0
    
def is_conjunction(sentence):
    if len(sentence)==3:
        if sentence[0]=='and':
            return 1
        else:
            return 0

def is_disjunction(sentence):
    if len(sentence)==3:
        if sentence[0]=='or':
            return 1
        else:
            return 0

def is_implication(sentence):
    if len(sentence)==3:
        if sentence[0]=='=>':
            return 1
        else:
            return 0

def is_equivalence(sentence):
    if len(sentence)==3:
        if sentence[0]=='<=>':
            return 1
        else:
            return 0

def is_literal(sentence):
    if is_atom(sentence):
        return 1
    elif is_negation(sentence)&is_atom(sentence[1]):
        return 1
    else:
        return 0

def prop2cnf(sentence):
    if is_literal(sentence)|(is_disjunction(sentence)&is_literal(sentence[1])&is_literal(sentence[2])):
        print (sentence)
    else:
        if is_equivalence(sentence):
            # split equivalence into to implications
            CNF.append(prop2cnf(('=>', sentence[1], sentence[2])))
            CNF.append(prop2cnf(('=>', sentence[2], sentence[1])))
            if DEBUG:
                print('Equivalence')
        if is_implication(sentence):
            # convert implication into notA or B
            conversion=('or', ('not', sentence[1]), sentence[2])
            #CNF.append(prop2cnf(conversion))
            if DEBUG:
                print(sentence,conversion)
        if is_negation(sentence)&~is_literal(sentence):
            if DEBUG:
                print('negation')
            # if we have a negation but it is not a literal, apply de Morgan
            #if is_disjunction(sentence[1]):
                #CNF.append(prop2cnf(('and', ('not', sentence[1][1]), ('not', sentence[1][2]))))
            #if is_conjunction(sentence[1]):
                #CNF.append(prop2cnf(('or', ('not', sentence[1][1]), ('not', sentence[1][2]))))
        
####### MAIN PART ########

# read command line path location
if len(sys.argv)>1:
    try:
        # read sentences from file
        sentences = read_sentences(sys.argv[1])
    except:
        print('file not found!')
        exit()
else: # load default file
    sentences = read_sentences('test1.txt')
# Choose task to perform:
print('Welcome to the Propositional logic to CNF converter 1.0\n')
print('Written by Simon Bilgeri and Rui Lopes\n')
number=0
while(number!='q'):
    print('\nChoose one of the following options:')
    print('List all sentences in propositional Logic (1)')
    print('Convert all sentences to CNF (2)')
    print('Quit(q)')
    number=input('\nYour choice:')
    if (number=='1'):
        print_sentences(sentences)
        # write to file
        f = open('CNF.txt','w')
        f.close()
    elif (number=='2'):
        CNF=prop2cnf(sentences[0])
        print(CNF)
    elif (number=='q'):
        print('Thank you for using Prop2CNF converter 1.0')
    else:
        print('Menu entry not recognized. Please try again...')
        
