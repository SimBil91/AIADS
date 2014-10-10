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
    goal=[]
    # hardcopy labyrinth for processing
    labyrinth_orig=[]
    start_semaphore=0 # set to one if start node is found once
    for x in labyrinth:
        labyrinth_orig.append(list(x))      
    switches=[x for y in range(len(labyrinth)) for x in labyrinth[y] if x<200 and x>3]
    possible_sw_comb=[] # all possible combinations of pushing switches
    for i in range(0, len(switches)+1):
        for subset in itertools.combinations(switches, i):
            possible_sw_comb.append(subset)
    for x in possible_sw_comb:
        labyrinth=[]
        for z in labyrinth_orig:
            labyrinth.append(list(z))     
        # switch doors
        door_state=[]
        for y in range(len(labyrinth)):
            for z in range(len(labyrinth[y])):
                if labyrinth[y][z]>=200:
                    if labyrinth[y][z]<300 and (labyrinth[y][z]-100) in x: # open closed doors
                       labyrinth[y][z]=labyrinth[y][z]+100
                    elif labyrinth[y][z]>=300 and (labyrinth[y][z]-200) in x: # close openend doors
                       labyrinth[y][z]=labyrinth[y][z]-100
                    door_state.append(labyrinth[y][z])
        door_state=tuple(door_state)
        # create graph
        for x in range(len(labyrinth)):
            for y in range(len(labyrinth[x])):
                if labyrinth[x][y]!=0:
                    graph[(x,y,door_state)]=[]
                    if labyrinth[x][y]==2 and start_semaphore==0: # start cell
                        start=(x,y,door_state)
                        start_semaphore=1
                    if labyrinth[x][y]==3: # goal cell
                        goal.append((x,y,door_state))
                    # labyrinth[x][y]>=100 and labyrinth[x][y]<200: # switch cell
                    if labyrinth[x][y-1]!=0 and (labyrinth[x][y-1]>=300 or labyrinth[x][y-1]<200): # left
                        graph[(x,y,door_state)].append((x,y-1,door_state))
                        if labyrinth[x][y] in switches: # if a switch change doorstate
                            door_state_temp=list(door_state)
                            for n,i in enumerate(door_state_temp):
                                if i-200==labyrinth[x][y]-100: # closed door
                                    door_state_temp[n]+=100
                                if i-300==labyrinth[x][y]-100: # open door
                                    door_state_temp[n]-=100
                            graph[(x,y,door_state)].append((x,y-1,tuple(door_state_temp)))
                    if labyrinth[x][y+1]!=0 and (labyrinth[x][y+1]>=300 or labyrinth[x][y+1]<200): # right
                        graph[(x,y,door_state)].append((x,y+1,door_state))
                        if labyrinth[x][y] in switches: # if a switch change doorstate
                            door_state_temp=list(door_state)
                            for n,i in enumerate(door_state_temp):
                                if i-200==labyrinth[x][y]-100: # closed door
                                    door_state_temp[n]+=100
                                if i-300==labyrinth[x][y]-100: # open door
                                    door_state_temp[n]-=100
                            graph[(x,y,door_state)].append((x,y+1,tuple(door_state_temp)))
                    if labyrinth[x+1][y]!=0 and (labyrinth[x+1][y]>=300 or labyrinth[x+1][y]<300) : # down
                        graph[(x,y,door_state)].append((x+1,y,door_state))
                        if labyrinth[x][y] in switches: # if a switch change doorstate
                            door_state_temp=list(door_state)
                            for n,i in enumerate(door_state_temp):
                                if i-200==labyrinth[x][y]-100: # closed door
                                    door_state_temp[n]+=100
                                if i-300==labyrinth[x][y]-100: # open door
                                    door_state_temp[n]-=100
                            graph[(x,y,door_state)].append((x+1,y,tuple(door_state_temp)))
                    if labyrinth[x-1][y]!=0 and (labyrinth[x-1][y]>=300 or labyrinth[x-1][y]<200): # up
                        graph[(x,y,door_state)].append((x-1,y,door_state))
                        if labyrinth[x][y] in switches: # if a switch change doorstate
                            door_state_temp=list(door_state)
                            for n,i in enumerate(door_state_temp):
                                if i-200==labyrinth[x][y]-100: # closed door
                                    door_state_temp[n]+=100
                                if i-300==labyrinth[x][y]-100: # open door
                                    door_state_temp[n]-=100
                            graph[(x,y,door_state)].append((x-1,y,tuple(door_state_temp)))
    return graph,start,goal

def translate_output(path,num_nodes):
    sequence=''
    num_actions=num_nodes
    translation={(0,1): 'R', (0,-1): 'L', (-1,0): 'U', (1,0): 'D'}
    for x in range(len(path)-1): #until last element
        direction=(path[x+1][0]-path[x][0],path[x+1][1]-path[x][1])
        if path[x][2]!=path[x+1][2]:
            num_actions+=1
            sequence+='P'
        sequence+=translation[direction]            
    return num_actions,sequence

def BFS(adj_list,start,goal):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed and the parent field
    # 0=white, 1=in list, 2=visited
    # More than one goal possible!
    field_state,queue = dict.fromkeys(adj_list,[0,0,0]), [start]
    goal_found=0
    while queue:
        field = queue.pop(0) # FIFO, get element from queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2]] # mark node as visited -> 2
        if field in goal: # if goal reached end the while loop
            goal_found=field
            print('Solution found!')
            break;
        for x in adj_list[field]: # for all sucessors of the parent
            if field_state[x][0]==0: # if not added to list before
                field_state[x]=[1,field_state[parent][1]+1,parent] # mark node as added, raise node counter and save its parent
                queue.append(x) # add node to queue
    if goal_found!=0:
        # print the path to the goal and return it
        x=goal_found
        path=[]
        while x != 0:
            path.insert(0,x)
            x=field_state[x][2]
        return field_state[goal_found][1],path
    else:
        return 'No solution found',[]

def DFS(adj_list,start,goal):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed and the parent field
    # 0=white, 1=in list, 2=visited
    # More than one goal possible!
    field_state,queue = dict.fromkeys(adj_list,[0,0,0]), [start]
    goal_found=0
    while queue:
        field = queue.pop() # LIFO, get element from queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2]] # mark node as visited -> 2
        if field in goal: # if goal reached end the while loop
            goal_found=field
            print('Solution found!')
            break;
        for x in adj_list[field]: # for all sucessors of the parent
            if field_state[x][0]==0: # if not added to list before
                field_state[x]=[1,field_state[parent][1]+1,parent] # mark node as added, raise node counter and save its parent
                queue.append(x) # add node to queue
    if goal_found!=0:
        # print the path to the goal and return it
        x=goal_found
        path=[]
        while x != 0:
            path.insert(0,x)
            x=field_state[x][2]
        return field_state[goal_found][1],path
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

# read labyrinth from file
labyrinth = read_labyrinth('labyrinth')
# print it to screen with symbols
print_labyrinth(labyrinth,elements)
# domain dependent: create graph out of labyrinth
graph,start,goal=create_graph(labyrinth)
# domain independent: perform desired search algorithm given the graph
num_nodes,actions=BFS(graph,start,goal)
# domain dependent: translate node path into (UDLR) movements
num_actions,actions=translate_output(actions,num_nodes)
# print result
print(num_actions)
print(actions)
# write to file
f = open('BFS','w')
f.write(str(num_actions)+'\n'+actions)
f.close()
