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
    try:
        sentences = [eval(l.strip()) for l in input_file]  # read the sentences
    except:
        print('Input format of sentences wrong! \n')
        return -1
   # remove empty lines
    sentences = [x for x in sentences if x]
    return sentences

def print_sentences(sentences):
    # This function prints all sentences given from a file
    print('\n')
    for i in range(0,len(sentences)):
        print('(',i,') ', show_nice_format(sentences[i]));
    return 1

def is_atom(sentence):
    # checks if sentence is atom (string)
    if type(sentence)==str:
        return 1
    else:
        return 0

def is_negation(sentence):
    # checks if sentence is a negation (only 2 arguments
    if len(sentence)==2:
        if sentence[0]=='not':
            return 1
        else:
            print('Input file contains errors!')
            exit(-1)
    else:
        return 0
    
def is_conjunction(sentence):
    # checks if sentence is conjunction
    if len(sentence)==3:
        if sentence[0]=='and':
            return 1
        else:
            return 0
    else:
        return 0

def is_disjunction(sentence):
    # checks if sentence is disjunction
    if len(sentence)==3:
        if sentence[0]=='or':
            return 1
        else:
            return 0
    else:
        return 0

def is_implication(sentence):
    #checks if sentence is implication
    if len(sentence)==3:
        if sentence[0]=='=>':
            return 1
        else:
            return 0
    else:
        return 0

def is_equivalence(sentence):
    # checks if sentence is equivalence
    if len(sentence)==3:
        if sentence[0]=='<=>':
            return 1
        else:
            return 0
    else:
         return 0

def is_literal(sentence):
    # checks if sentence is a literal
    if is_atom(sentence):
        return 1
    elif is_negation(sentence)&is_atom(sentence[1]):
        return 1
    else:
        return 0
def show_nice_format(sentence):
    # Converts sentence in nice output format
    if is_atom(sentence):
        return sentence
    else:
        if is_equivalence(sentence):
            return '('+show_nice_format(sentence[1])+'<=>'+show_nice_format(sentence[2])+')'
        elif is_implication(sentence):
            return '('+show_nice_format(sentence[1])+'=>'+show_nice_format(sentence[2])+')'
        elif is_negation(sentence):
            return chr(172)+show_nice_format(sentence[1])
        elif is_conjunction(sentence):
            return '('+show_nice_format(sentence[1])+'&'+show_nice_format(sentence[2])+')'
        elif is_disjunction(sentence):
            return '('+show_nice_format(sentence[1])+'|'+show_nice_format(sentence[2])+')'
        
def elim_equivalence(sentence):
    # This function eliminates all equivalence in a sentence
    if is_literal(sentence):
        return sentence
    else:
        if is_equivalence(sentence):
            # split equivalence into to implications
            conversion=('and', ('=>', sentence[1], sentence[2]), ('=>', sentence[2], sentence[1]))
            if DEBUG:
                print(show_nice_format(sentence),'is an equivalence!')
                print('Splitting it into two implications:')
                print(show_nice_format(conversion))
            # perform conversion
            return elim_equivalence(conversion)
        else:
            if is_negation(sentence): # if a negation only 1 argument
                return (sentence[0],elim_equivalence(sentence[1]))
            else: # else several arguments
                return (sentence[0],elim_equivalence(sentence[1]),elim_equivalence(sentence[2]))

def elim_implication(sentence):
    # This function eliminates all implications in a sentence
    if is_literal(sentence):
        return sentence
    else:
        if is_implication(sentence):
            # convert implication into notA or B
            conversion=('or', ('not', sentence[1]), sentence[2])
            if DEBUG:
                print(show_nice_format(sentence),'is an implication!')
                print('Transform it into '+chr(172)+'sentence1|sentence2:')
                print(show_nice_format(conversion))
            # perfrom conversion
            return elim_implication(conversion)
        else:
            if is_negation(sentence): # if a negation only 1 argument
                return (sentence[0],elim_implication(sentence[1]))
            else: # else several arguments
                return (sentence[0],elim_implication(sentence[1]),elim_implication(sentence[2]))

def propagate_negation(sentence):
    # This function propagates all negations in a sentence
    if is_literal(sentence):
        return sentence
    else:
        if is_negation(sentence):
            #if we have a negation but it is not a literal, apply de Morgan's rule
            if DEBUG:
                print(show_nice_format(sentence), 'is a negation!')
            if is_negation(sentence[1]):
                # eliminate negation
                conversion3=(sentence[1][1])
                if DEBUG:
                    print('Eliminate double negation:')
                    print(show_nice_format(conversion3))
                return propagate_negation(conversion3)
            elif is_disjunction(sentence[1]):
                conversion1=('and', ('not', sentence[1][1]), ('not', sentence[1][2]))
                if DEBUG:
                    print('Converting disjunction to conjunction applying De Morgan''s rule:')
                    print(show_nice_format(conversion1))
                # perform conversion
                return propagate_negation(conversion1)
            elif is_conjunction(sentence[1]):
                conversion2=('or', ('not', sentence[1][1]), ('not', sentence[1][2]))
                if DEBUG:
                    print('Converting conjunction to disjunction applying De Morgan''s rule:')
                    print(show_nice_format(conversion2))
                # perform conversion
                return propagate_negation(conversion2)
            else:
                print('Input sentence contains errors!')
        else:
            return (sentence[0],propagate_negation(sentence[1]),propagate_negation(sentence[2]))

def distribute_disjunction(sentence):
    # This function distributes all disjunctions in a sentence
    #print(sentence)
    if is_literal(sentence):
        return sentence
    else:
        if is_disjunction(sentence):
            # check if there is a conjunction inside
            if is_conjunction(sentence[1]): # if first argument or both
                conversion1=('and',('or', sentence[1][1], sentence[2]), ('or', sentence[1][2], sentence[2]))
                if DEBUG:
                    print(show_nice_format(sentence), 'Left or both side(s) is(are) conjunction, disjunction is distributed:')
                    print(show_nice_format(conversion1))
                return distribute_disjunction(conversion1)
            elif is_conjunction(sentence[2]): # second argument
                conversion2=('and',('or', sentence[1], sentence[2][1]), ('or', sentence[1], sentence[2][2]))
                if DEBUG:
                    print(show_nice_format(sentence), 'Right side is conjunction, disjunction is distributed:')
                    print(show_nice_format(conversion2))
                return distribute_disjunction(conversion2)
            else: # disjunction contains only literals or disjunctions --> return them in next call
                return (sentence[0],distribute_disjunction(sentence[1]),distribute_disjunction(sentence[2]))
        else:# conjunction
            return (sentence[0],distribute_disjunction(sentence[1]),distribute_disjunction(sentence[2]))

def prop2cnf(sentence):
    # This wrapper function only calls each transformation step for a sentence
    # 1. Eliminate Equivalences, 2. Eliminate Implications, 3. Propagate Negations, 4. Distribute Disjunctions
    # perform distribution of disjunction until no more changes
    prev_iteration=()
    current_iteration=distribute_disjunction(propagate_negation(elim_implication(elim_equivalence(sentence))))
    while(prev_iteration!=current_iteration):
        prev_iteration=current_iteration
        current_iteration=distribute_disjunction(prev_iteration)
    return current_iteration

def merge_disjunctions(sentence):
    # This function merges all disjunctions in a sentence (no 'or')
    if is_literal(sentence):
        return sentence
    else:
        if is_disjunction(sentence): # if a disjunction found append the list of lists
            CNF=[]
            CNF.append(merge_disjunctions(sentence[1]))
            CNF.append(merge_disjunctions(sentence[2]))
        return CNF

def flatten(lst):
    # This function flattens list of lists (for or's)
	return sum( ([x] if not isinstance(x, list) else flatten(x)
		     for x in lst), [] )
    
def extract_clauses(sentence):
    # This function converts the logical tree to CNF (list of list(clauses))
    change=1 # check if changes are made
    work_CNF=[sentence] # temporal CNF list
    CNF=[] # resulting list of lists
    while change: # iterate until no changes made anymore
        change=0
        work_CNF2=[] # empty work list 2
        for i in range(0,len(work_CNF)):
            if is_literal(work_CNF[i]): # if it's a literal push it to the CNF list
                CNF.append([work_CNF[i]])
                change=1
            elif is_conjunction(work_CNF[i]): # if it's a conjunction push both clauses to working list
                work_CNF2.append(work_CNF[i][1])
                work_CNF2.append(work_CNF[i][2])
                change=1
            elif is_disjunction(work_CNF[i]): # if it's a disjunction, merge it, flatten it and push it to the CNF list
                CNF.append(flatten(merge_disjunctions(work_CNF[i])))
        work_CNF[:]=work_CNF2[:]
    return CNF

def simplify_clause(CNF):
    # This function applies 4 simplification rules.
    # Dublicates in clauses, Remove clauses with true and false literals,
    # remove identical clauses and check if clauses are subsets of others
    CNF_delete=[]
    for i in range(0,len(CNF)):
        # Remove dublicates of all clauses
        if len(CNF[i])!=len(set(CNF[i])):
           if DEBUG:
                print(CNF[i],'Remove duplicate elements:')
           CNF[i]=list(set(CNF[i]))
           if DEBUG:
                print(CNF[i])
        # Remove clauses with true and false literals
        for j in range(0,len(CNF[i])):
            for k in range(0,len(CNF[i])):
                if (is_negation(CNF[i][j])):
                    if(CNF[i][k]==CNF[i][j][1])&(i not in CNF_delete):
                        if DEBUG:
                            print(CNF[i][j],'is the negation of', CNF[i][k])
                            print('Removing clause...')
                        CNF_delete.append(i)
                        break;
    # Remove identical clauses:
    for i in range(0,len(CNF)):
        for j in range(i,len(CNF)):
            if (CNF[i]==CNF[j])&(i!=j)&(i not in CNF_delete):
                if DEBUG:
                    print(CNF[i],'is already in the KB!')
                    print('Removing clause...')
                CNF_delete.append(j)
    CNF_delete=list(set(CNF_delete))
    CNF_delete.sort()
    # Delete clauses
    for i in range(0,len(CNF_delete)):
        del CNF[CNF_delete[len(CNF_delete)-1-i]]
    # Check for subsets
    CNF_delete=[]
    for i in range(0,len(CNF)):
        for j in range(0,len(CNF)):
            if (set(CNF[i]) > set(CNF[j]))&(i!=j):
                if DEBUG:
                    print(CNF[j],'is a subset of', CNF[i])
                CNF_delete.append(i)
                if DEBUG:
                    print('Removing', CNF[i],'...')
    CNF_delete=list(set(CNF_delete))
    CNF_delete.sort()
    for i in range(0,len(CNF_delete)):
        del CNF[CNF_delete[len(CNF_delete)-1-i]]
    return CNF               
    

####### MAIN PART ########

# Read command line path location
if len(sys.argv)>1:
    try:
        # read sentences from file
        sentences = read_sentences(sys.argv[1])
    except:
        print('file not found!')
        exit()
else: # load default file
    sentences = read_sentences('test.txt')
if sentences==-1: # if an error occured --> Exit
    exit()

# MENU: Choose task to perform:
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
        # Choice 1: Print sentences
        print_sentences(sentences)
        print('\nChoose number of sentence to convert with explanations of each step')
        sentence_number=input('Number:')
        # Convert chosen sentence with DEBUG=1
        if int(sentence_number) in range(0,len(sentences)):
            print('\nConverting sentence',int(sentence_number),':\n')
            DEBUG=1 # Show each step
            CNF=prop2cnf(sentences[int(sentence_number)]) # call each sentence
            print('\nCNF:',show_nice_format(CNF)) # print the result in nice format
            CNF=extract_clauses(CNF)# extract clauses
            CNF=simplify_clause(CNF) # simplify them
            print('\nCNF:',CNF) # print resulting list of lists
        else:
            print('Sentence number not recognized')
    elif (number=='2'):
        # Convert all sentences and simplify them at the end again
        print('\n')
        print('In propositional Logic:')
        print_sentences(sentences) # print sentences
        print('\n')
        print('Converting all sentences to CNF...')
        DEBUG=0
        CNF_TOT=[]
        for i in range(0,len(sentences)):
            # convert all sentences, extract clauses and simplify them
            CNF=simplify_clause(extract_clauses(prop2cnf(sentences[i]))) 
            for j in range(0,len(CNF)):
                CNF_TOT.append(CNF[j])
            print('CNF',i,':',CNF)
        print('\nSimplification rules are applied concerning all clauses...')
        print('Resulting knowledgebase(KB) written to file:')
        # Write to file
        f = open('CNF.txt','w')
        CNF_TOT=simplify_clause(CNF_TOT) # simplify resulting KB
        print()
        for item in CNF_TOT:
          print("%s\n" % item)
          f.write("%s\n" % item) # Write KB to file
        f.close()
    elif (number=='q'):
        print('Thank you for using Prop2CNF converter 1.0')
    else:
        print('Menu entry not recognized. Please try again...')
        
