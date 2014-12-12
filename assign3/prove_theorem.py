"""
Artifcial Intelligence and Decision Systems Assignment 3, Theorem Prover
Authors: Simon Bilgeri, Rui Lopes
Year: 2014
Contact: Simon.Bilgeri@tum.de
"""
import sys
import prop2cnf # module from assignment 2

DEBUG = 0


def read_clauses(filename):
    # This function reads a Knowledgbase in CNF or propositional logic from a file
    # input: filename of input file
    # output: Proof based on Resolution step by step
    # Open input file
    input_file = open(filename)
    KB=[]
    to_prove=[]
    try:
        read = [eval(l.strip()) for l in input_file]  # read the clauses/sentences
    except:
        print('Input format of sentences wrong! \n')
        return -1
    # remove empty lines
    read = [x for x in read if x]
    # Check if sentences already converted to CNF
    if type(read[0])==list:
        clauses=read;
        return clauses,KB,to_prove
    else: # convert KB to CNF and negate last sentence before
        KB=read[0:len(read)-1]
        to_prove=read[len(read)-1]
        clauses=[]
        # convert KB to CNF
        prop2cnf.DEBUG=0
        for i in range(0,len(KB)):
            # convert all sentences, extract clauses and simplify them
            CNF=prop2cnf.simplify_clause(prop2cnf.extract_clauses(prop2cnf.prop2cnf(KB[i]))) 
            for j in range(0,len(CNF)):
                clauses.append(CNF[j])
        # negate sentence to prove and convert it to CNF
        CNF=prop2cnf.simplify_clause(prop2cnf.extract_clauses(prop2cnf.prop2cnf(('not',to_prove))))
        for j in range(0,len(CNF)): # add clauses
            clauses.append(CNF[j])
        # simplify resulting clauses
        clauses=prop2cnf.simplify_clause(clauses) # simplify resulting KB
        return clauses,KB,to_prove
        
def print_sentences(KB,to_prove):
    # This function prints all sentences and clauses given from a file
    print('\n')
    if KB==[]:
        print('KB is not provided in propositional logic')
    else:
        print('KB in propositional Logic:')
        for i in range(0,len(KB)):
            print('(',i,') ', prop2cnf.show_nice_format(KB[i]))
        print('\nSentence to prove in propositional Logic:')
        print('(',i+1,') ',prop2cnf.show_nice_format(to_prove))
 
def print_clauses(clauses,write):
    # This function prints all sentences and clauses given from a file
    print('\nResulting clauses for resolution in CNF:\n')
    i=0
    for item in clauses:
        print('( c',i,')','%s' % item)
        if write:
            f.write('(c'+str(i)+')'+str(item)+'\n')
        i=i+1
    return 1     

def perform_resolution(clause1,clause2,clauses):
    new_clause=[]
    for k in range(0,len(clause1)):
        for l in range(0, len(clause2)):
            # if first clause literal is negation check for atom in second clause
            if clause1[k]==('not',clause2[l]) or clause2[l]==('not',clause1[k]):
                temp1=clause1[:]
                temp1.remove(clause1[k])
                temp2=clause2[:]
                temp2.remove(clause2[l])
                new_clause=temp1+temp2
                if new_clause==[]:
                    return new_clause
                # check for simplification. (multiple literals or tautology)
                prop2cnf.DEBUG=0
                if (prop2cnf.simplify_clause([new_clause])) not in clauses:
                    if (prop2cnf.simplify_clause([new_clause]))!=[]:
                        prop2cnf.DEBUG=1
                        new_clause=(prop2cnf.simplify_clause([new_clause]))[0]
                    else:
                        print('Resolving',clause1,'with',clause2,'yields a tautology...')

                        new_clause=0
                        clauses.append(temp1+temp2)
                return new_clause
    return 0
    
def perform_proof(clauses):
    # see page 280/311
    # Uses unit preference strategy (try resolution with unit clauses first)
    # Set of clauses is ordered with respect to the number of literals
    clauses_res=clauses[:]
    clauses_list=clauses[:]
    clauses_res.sort(key=len)
    clauses_total=clauses[:]
    print_clauses(clauses_list,1)
    f.write('\n')
    print('\nsorting clauses with respect to the number of literals...')
    l=[];
    for x in range(0,len(clauses_res)):
        l.append(clauses_list.index(clauses_res[x]))
    print('queue:', l)

    # repeat until empty clause or no new clause is found
    empty_clause=0
    set_update=1
    while empty_clause==0 and set_update==1:
        # for all clauses, check if resolution is possible
        set_update=0
        for i in range(0,len(clauses_res)):
            for j in range(i+1,len(clauses_res)):
                # check if clauses contain negate literals
                new_clause=perform_resolution(clauses_res[i],clauses_res[j],clauses_total)
                if new_clause==[]:
                    empty_clause=1
                    print('( c',len(clauses_res),')','%s' % new_clause,'( c',clauses_list.index(clauses_res[i]),',','c',clauses_list.index(clauses_res[j]),')')
                    f.write('(c'+str(len(clauses_res))+')'+str(new_clause)+' (c'+str(clauses_list.index(clauses_res[i]))+','+'c'+str(clauses_list.index(clauses_res[j]))+')\n') 
                    print('empty clause found')
                    return 1
                elif new_clause!=0: # check if clause is already in the set
                    if new_clause not in clauses_res:
                      # add clause to list
                      clauses_res.append(new_clause)
                      clauses_list.append(new_clause)
                      clauses_total.append(new_clause)
                      set_update=1
                      print('new clause added!')
                      print('( c',len(clauses_res)-1,')','%s' % new_clause,'( c',clauses_list.index(clauses_res[i]),',','c',clauses_list.index(clauses_res[j]),')')
                      f.write('(c'+str(len(clauses_res)-1)+')'+str(new_clause)+' (c'+str(clauses_list.index(clauses_res[i]))+','+'c'+str(clauses_list.index(clauses_res[j]))+')\n') 
                      break

            if set_update==1: # start again from the beginning and sort the clauses again
                clauses_res.sort(key=len) # unit preference rule extended
                print('sorting clauses with respect to the number of literals...')
                l=[];
                for x in range(0,len(clauses_res)):
                    l.append(clauses_list.index(clauses_res[x]))
                print('queue:', l)
                break
            
        
    print('No new clauses can be found...')
    return 0 # if no changes anymore
                                

####### MAIN PART ########

# Read command line path location
if len(sys.argv)>1:
    try:
        # read sentences from file
        clauses,KB,to_prove = read_clauses(sys.argv[1])
    except:
        print('file not found!')
        exit()
else: # load default file
    clauses,KB,to_prove = read_clauses('test4.txt')
if KB==-1: # if an error occured --> Exit
    exit()

# MENU: Choose task to perform:
print('Welcome to the theorem prover based on Resulution v1.0\n')
print('Written by Simon Bilgeri and Rui Lopes\n')
number=0
while(number!='q'):
    print('\nChoose one of the following options:')
    print('List all sentences in propositional Logic (1)')
    print('List all clauses in CNF (2)')
    print('Prove if KB infers alpha using Resolution (3)')
    print('Quit(q)')
    number=input('\nYour choice:')
    if (number=='1'):
        # Choice 1: Print sentences
        print_sentences(KB,to_prove)
    elif (number=='2'):
        print_clauses(clauses,0)
    elif (number=='3'):
        # Apply resolution to prove the theorem
        f = open('Proof.txt','w')
        print('\n')
        print('Starting proof based on Resolution:')
        if to_prove!=[]:
            print('Trying to proof: KB -|',prop2cnf.show_nice_format(to_prove))
            print('Negate sentence for resolution:',prop2cnf.show_nice_format(('not',to_prove)))
        result=perform_proof(clauses)
        if to_prove!=[]:
            if result==0:
                print('\nKB not -|',prop2cnf.show_nice_format(to_prove))
                f.write('FALSE')
            else:
                print('\nKB -|',prop2cnf.show_nice_format(to_prove))
                f.write('TRUE')
        else:
            if result!=0:
                print('\nThe theorem could be proved successfully')
                f.write('FALSE')
            else:
                print('\nThe theorem could not be proved')
                f.write('TRUE')
        f.close()
    elif (number=='q'):
        print('Thank you for using proof_theroem 1.0')
    else:
        print('Menu entry not recognized. Please try again...')
        
