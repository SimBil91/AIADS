"""
Artifcial Intelligence and Decision Systems Assignment 1, Labyrinth
Authors: Simon Bilgeri, Rui Lopes
Year: 2014
Contact: Simon.Bilgeri@tum.de
"""

import itertools

def read_labyrinth(filename):
    # This function reads the labyrinth into a list
    # Open input labyrinth
    input_file = open(filename)
    # read first line and get L and C of matrix
    L, C = [int(x) for x in input_file.readline().split()]  # split strings in line to numbers, convert strings to int
    labyrinth = [[int(x) for x in input_file.readline().split()] for l in range(0, L)]  # read the matrix
    #print(labyrinth, L, C)
    return labyrinth

def print_labyrinth(labyrinth,elements):
    # This function converts the labyrinth numbers into symbols and prints it
    labyrinth_symb=[];
    for x in range(0,len(labyrinth)):
        labyrinth_symb.append([elements[change] for change in labyrinth[x]])
        print(''.join(labyrinth_symb[x]))
    return

def create_graph(labyrinth):
    graph={}
    # hardcopy labyrinth for processing
    labyrinth_orig=[]
    for x in labyrinth:
        labyrinth_orig.append(list(x))
        
    door_state=[x for y in range(len(labyrinth)) for x in labyrinth[y] if x>=200]
    switches=[x for y in range(len(labyrinth)) for x in labyrinth[y] if x<200 and x>3]
    possible_sw_comb=[] # all possible combinations of pushing switches
    for i in range(0, len(switches)+1):
        for subset in itertools.combinations(switches, i):
            possible_sw_comb.append(subset)
    for x in possible_sw_comb:
        for y in x:
            # open or close doors in labyrinth
            #for switch in y:
                  print('jiha')  
            # update door_state
    print(door_state,switches)
    for x in range(len(labyrinth)):
        for y in range(len(labyrinth[x])):
            if labyrinth[x][y]!=0:
                graph[(x,y)]=[]
                if labyrinth[x][y]==2: # start cell
                    start=(x,y)
                if labyrinth[x][y]==3: # goal cell
                    goal=(x,y)
                # labyrinth[x][y]>=100 and labyrinth[x][y]<200: # switch cell
                if labyrinth[x][y-1]!=0 and labyrinth[x][y-1]<300: # left
                    graph[(x,y)].append((x,y-1))
                if labyrinth[x][y+1]!=0 and labyrinth[x][y+1]<300: # right
                    graph[(x,y)].append((x,y+1))
                if labyrinth[x+1][y]!=0 and labyrinth[x+1][y]<300: # down
                    graph[(x,y)].append((x+1,y))
                if labyrinth[x-1][y]!=0 and labyrinth[x-1][y]<300: # up
                    graph[(x,y)].append((x-1,y))      
    return graph,start,goal

def translate_output(path):
    sequence=''
    translation={(0,1): 'R', (0,-1): 'L', (-1,0): 'U', (1,0): 'D'}
    for x in range(len(path)-1): #until last element
        direction=(path[x+1][0]-path[x][0],path[x+1][1]-path[x][1])
        sequence+=translation[direction]            
    return sequence

def BFS(adj_list,start,goal):
    # As the labyrinth is sparse, a list reprentation of the graph is used
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state saves if the field was visited (0=no,1=yes), number of nodes traversed and the parent field
    # 0=white, 1=in list, 2=visited
    field_state,queue = dict.fromkeys(adj_list,[0,0,0]), [start]
    goal_found=0
    while queue:
        field = queue.pop(0) # FIFO, get element from queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2]] # mark node as visited -> 2
        if field==goal: # if goal reached end the while loop
            goal_found=1
            break;
            print('Goal found!')
        for x in adj_list[field]: # for all sucessors of the parent
            if field_state[x][0]==0: # if not added to list before
                field_state[x]=[1,field_state[parent][1]+1,parent] # mark node as added, raise node counter and save its parent
                queue.append(x) # add node to queue
    if goal_found:
        # print the path to the goal and return it
        x=goal
        path=[]
        while x != 0:
            path.insert(0,x)
            x=field_state[x][2]
        return field_state[goal][1],path
    else:
        return 'No solution found',[]

"""graph = {(1,1): set([(1,2), (1,3)]),
         (1,2): set([(1,1), (1,4), (1,5)]),
         (1,3): set([(1,1), (1,6)]),
         (1,4): set([(1,2)]),
         (1,5): set([(1,2), (1,6)]),
         (1,6): set([(1,3), (1,5)])}

graph2 = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}"""

# MAIN PART
# Create a dictionary for visualisation
elements = {0:'####',1:'    ',2:' OO ',3:' G  '}
for x in range(100,109):
    elements[x]='SW'+str(x-100) + ' '
for x in range(110,199):
    elements[x]='SW'+str(x-100)
for x in range(200,209):
    elements[x]='CD'+str(x-200) + ' '
for x in range(210,299):
    elements[x]='CD'+str(x-200) 
for x in range(300,309):
    elements[x]='OD'+str(x-300) + ' '
for x in range(310,399):
    elements[x]='OD'+str(x-300) 

labyrinth = read_labyrinth('labyrinth')
print_labyrinth(labyrinth,elements)
#print(BFS(graph2,'A','F'))
graph,start,goal=create_graph(labyrinth)
num_actions,actions=BFS(graph,start,goal)
print(num_actions)
print(translate_output(actions))
