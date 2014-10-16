"""
Artifcial Intelligence and Decision Systems Assignment 1, Labyrinth
Authors: Simon Bilgeri, Rui Lopes
Year: 2014
Contact: Simon.Bilgeri@tum.de
"""
import sys
import itertools
import time

def read_labyrinth(filename):
    # This function reads the labyrinth into a list
    # input: filename of labyrinth file
    # output: labyrinth  matrix
    # Open input labyrinth
    input_file = open(filename)
    # read first line and get L and C of matrix
    L, C = [int(x) for x in input_file.readline().split()]  # split strings in line to numbers, convert strings to int
    labyrinth = [[int(x) for x in input_file.readline().split()] for l in input_file]  # read the matrix
    # remove empty lines
    labyrinth = [x for x in labyrinth if x]
    return labyrinth

def print_labyrinth(labyrinth,elements):
    # This function converts the labyrinth numbers into symbols and prints it
    # input: labyrinth matrix, conversion dictionary
    # output: labyrinth matrix in symbols
    labyrinth_symb=[];
    for x in range(0,len(labyrinth)):
        labyrinth_symb.append([elements[change] for change in labyrinth[x]])
        print(''.join(labyrinth_symb[x]))
    return

def create_graph(labyrinth):
    # This function creates a graph out of the labyrinth. (domain dependent)
    # input: labyrinth in matrix form
    # output: graph (dictionary), start node, goal nodes
    graph={}
    goal=[]
    # hardcopy labyrinth for processing
    labyrinth_orig=[]
    start_semaphore=0 # set to one if start node is found once
    for x in labyrinth: # hardcopy labyrinth
        labyrinth_orig.append(list(x))      
    switches=[x for y in range(len(labyrinth)) for x in labyrinth[y] if x<200 and x>3]
    possible_sw_comb=[] # all possible combinations of pushing switches
    for i in range(0, len(switches)+1):
        for subset in itertools.combinations(switches, i):
            possible_sw_comb.append(subset)
    for x in possible_sw_comb:
        labyrinth=[]
        for z in labyrinth_orig:
            labyrinth.append(list(z)) # get original labyrinth    
        # switch doorsstate according to possible_sw_comb
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
        for z in range(len(labyrinth)):
            for y in range(len(labyrinth[z])):
                if labyrinth[z][y]!=0:
                    graph[(z,y,door_state)]=[]
                    if labyrinth[z][y]==2 and start_semaphore==0: # start cell
                        start=(z,y,door_state)
                        start_semaphore=1
                    if labyrinth[z][y]==3: # goal cell
                        goal.append((z,y,door_state))
                    if labyrinth[z][y] in switches: # if a switch, connect to branch with different doorstate
                           door_state_temp=list(door_state)
                           for n,i in enumerate(door_state_temp):
                               if i-200==labyrinth[z][y]-100: # closed door
                                   door_state_temp[n]+=100
                               if i-300==labyrinth[z][y]-100: # open door
                                   door_state_temp[n]-=100
                           graph[(z,y,door_state)].append((z,y,tuple(door_state_temp)))
                    if labyrinth[z][y-1]!=0 and (labyrinth[z][y-1]>=300 or labyrinth[z][y-1]<200): # left
                        graph[(z,y,door_state)].append((z,y-1,door_state))
                    if labyrinth[z][y+1]!=0 and (labyrinth[z][y+1]>=300 or labyrinth[z][y+1]<200): # right
                        graph[(z,y,door_state)].append((z,y+1,door_state))  
                    if labyrinth[z+1][y]!=0 and (labyrinth[z+1][y]>=300 or labyrinth[z+1][y]<200) : # down
                        graph[(z,y,door_state)].append((z+1,y,door_state))
                    if labyrinth[z-1][y]!=0 and (labyrinth[z-1][y]>=300 or labyrinth[z-1][y]<200): # up
                        graph[(z,y,door_state)].append((z-1,y,door_state))
    return graph,start,goal

                                    
def translate_output(path,num_nodes):
    # This function translates the output path to the domain dependent representation
    # input: path list, number of nodes traversed
    # output: number of actions (with push), the sequence
    sequence=''
    num_actions=num_nodes
    translation={(0,1): 'R', (0,-1): 'L', (-1,0): 'U', (1,0): 'D', (0,0): 'P'} # Difference 0 --> PUSH!
    for x in range(len(path)-1): #until last element
        direction=(path[x+1][0]-path[x][0],path[x+1][1]-path[x][1])
        sequence+=translation[direction]            
    return num_actions,sequence

def BFS(adj_list,start,goal):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed and the parent field
    # 0=white, 1=in list, 2=visited
    # More than one goal possible!
    # input: adj_list(graph dictionary), start node, goal nodes
    # output: # of nodes traversed, path
    field_state,queue = dict.fromkeys(adj_list,[0,0,0]), [start]
    goal_found=0
    while queue:
        field = queue.pop(0) # FIFO, get element from queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2]] # mark node as visited -> 2
        if field in goal: # if goal reached end the while loop
            goal_found=field
            print('Solution found using Breadth First Search!')
            break
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
    # input: adj_list(graph dictionary), start node, goal nodes
    # output: # of nodes traversed, path
    field_state,queue = dict.fromkeys(adj_list,[0,0,0]), [start]
    goal_found=0
    while queue:
        field = queue.pop() # LIFO, get element from queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2]] # mark node as visited -> 2
        if field in goal: # if goal reached end the while loop
            goal_found=field
            print('Solution found using Depth First Search!')
            break
        for x in adj_list[field]: # for all sucessors of the parent
            if field_state[x][0]!=2: # if not added to list before
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

def IdDFS(adj_list,start,goal,limit):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed in path and the parent field
    # 0=white, 1=in list, 2=visited
    # More than one goal possible!
    # Depth of search is limited by "limit'
    # input: adj_list(graph dictionary), start node, goal nodes, limit
    # output: # of nodes traversed, path
    goal_found=0
    depth_iter=1
    while depth_iter<limit and goal_found==0:
        field_state,queue = dict.fromkeys(adj_list,[0,0,0]), [start]
        while queue:
            field = queue.pop() # LIFO, get element from queue
            parent=field # save parent node
            field_state[field]=[2,field_state[field][1],field_state[field][2]] # mark node as visited -> 2
            if field in goal: # if goal reached end the while loop
                goal_found=field
                print('Solution found using Iterative deepening Depth First Search with L=%d!' %limit)
                break
            if field_state[field][1]<=depth_iter: # when current field is in highest depth dont add any nodes anymore
                for x in adj_list[field]: # for all sucessors of the parent
                    if field_state[x][0]==0: # if not added to list before and it is within the limit
                        field_state[x]=[1,field_state[parent][1]+1,parent] # mark node as added, raise node counter and save its parent
                        queue.append(x) # add node to queue
                    if field_state[x][0]==2 and field_state[field][1]+1<field_state[x][1]: # if other path shorter put node in queue again 
                        field_state[x]=[1,field_state[parent][1]+1,parent] # mark node as added, raise node counter and save its parent
                        queue.append(x) # add node to queue
        depth_iter+=1 # raise highest iteration after one try
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

def Greedy(adj_list,start,goal,heu_func):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed, the parent field and the heuristic value
    # 0=white, 1=in list, 2=visited
    # The heuristic function is given with h_func
    # input: adj_list(graph dictionary), start node, goal nodes, heuristic function
    # output: # of nodes traversed, path
    field_state,queue = dict.fromkeys(adj_list,[0,0,0,0]), [start]
    goal_found=0
    while queue:
        # sort queue according to their h-value
        test=queue[:]
        queue=sorted(queue, key=lambda x:field_state[x][3])
        field = queue.pop(0) # get first element of queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2],field_state[field][3]] # mark node as visited -> 2
        if field in goal: # if goal reached end the while loop
            goal_found=field
            print('Solution found using Greedy Best First Search!')
            break
        for x in adj_list[field]: # for all sucessors of the parent
            if field_state[x][0]==0: # if not added to list before
                field_state[x]=[1,field_state[parent][1]+1,parent,heu_func(x,goal)] # mark node as added, raise node counter and save its parent
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

def Astar(adj_list,start,goal,heu_func,cost_func):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed, the parent field and the heuristic value
    # 0=white, 1=in list, 2=visited
    # The heuristic function is given with h_func
    # input: adj_list(graph dictionary), start node, goal nodes, heuristic and node cost function
    # output: # of nodes traversed, path
    field_state,queue = dict.fromkeys(adj_list,[0,0,0,0]), [start]
    goal_found=0
    while queue:
        # sort queue according to their f-value
        queue=sorted(queue, key=lambda x:field_state[x][3]+field_state[x][1])
        field = queue.pop(0) # get first element of queue
        parent=field # save parent node
        field_state[field]=[2,field_state[field][1],field_state[field][2],field_state[field][3]] # mark node as visited -> 2
        if field in goal: # if goal reached end the while loop
            goal_found=field
            print('Solution found using A* Search!')
            break
        for x in adj_list[field]: # for all sucessors of the parent
            if field_state[x][0]==0: # if not added to list before
                field_state[x]=[1,field_state[parent][1]+cost_func(x),parent,heu_func(x,goal)] # mark node as added, raise node counter and save its parent
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
    
def IDAstar(adj_list,start,goal,heu_func,cost_func):
    # A list reprentation of the graph is used, which is good for sparse graphs
    # This algorithm can be used with any kind of graph given in a dictionary representation.
    # field_state represents if the field was visited (0=no,1=yes), number of nodes traversed, the parent field and the heuristic value
    # 0=white, 1=in list, 2=visited
    # The heuristic function is given with h_func
    # input: adj_list(graph dictionary), start node, goal nodes, heuristic and cost function
    # output: # of nodes traversed, path
    goal_found=0
    cutoff=1
    while goal_found==0:
        newcutoff=float("inf")
        field_state,queue = dict.fromkeys(adj_list,[0,0,0,0]), [start]
        while queue:
            # sort queue according to their f-value
            queue=sorted(queue, key=lambda x:field_state[x][3]+field_state[x][1])
            field = queue.pop(0) # get first element of queue
            parent=field # save parent node
            field_state[field]=[2,field_state[field][1],field_state[field][2],field_state[field][3]] # mark node as visited -> 2
            if field in goal: # if goal reached end the while loop
                goal_found=field
                print('Solution found using Iterative Deepening A* Search!')
                break
            for x in adj_list[field]: # for all sucessors of the parent
                f=heu_func(x,goal)+field_state[parent][1]+cost_func(x)
                if field_state[x][0]==0 and f<=cutoff: # if not added to list before
                    field_state[x]=[1,field_state[parent][1]+cost_func(x),parent,heu_func(x,goal)] # mark node as added, raise node counter and save its parent
                    queue.append(x) # add node to queue
                if f>cutoff and f<newcutoff: # find closest higher value to current cutoff
                    newcutoff=f
        if newcutoff!=float('inf'):
           cutoff=newcutoff
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

def h_func(node,goal):
    # use l1 norm as heuristic function
    # input: current node, goal state
    # output: value of function
    value=abs(node[0]-goal[0][0])+abs(node[1]-goal[0][1])
    return value

def n_func(node):
    # input: current node
    # output: cost of node
    return 1


####### MAIN PART ########

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

# read command line path location
if len(sys.argv)>1:
    try:
        # read labyrinth from file
        labyrinth = read_labyrinth(sys.argv[1])
    except:
        print('file not found!')
        exit()
else: # load default labyrinth
    labyrinth = read_labyrinth('inputTest7.txt')
# domain dependent: create graph out of labyrinth
graph,start,goal=create_graph(labyrinth)
# Choose Algorithm to use:
print('Welcome to the Labyrinth Solver 1.0\n')
print('Written by Simon Bilgeri and Rui Lopes\n')
# print it to screen with symbols
print_labyrinth(labyrinth,elements)
number=0
while(number!='q'):
    print('\nPlease choose the desired search algorithm:')
    print('uninformed: BFS(1), DFS(2), IdDFS(3)')
    print('informed: Greedy(4), A*(5), IDA*(6)')
    print('Quit(q)')
    number=input('\nYour choice:')
    start_time = time.time()
    if (number=='1'):
        # domain independent: perform desired search algorithm given the graph
        num_nodes,actions=BFS(graph,start,goal)
        # domain dependent: translate node path into (UDLR) movements
        num_actions,actions=translate_output(actions,num_nodes)
        # print result
        print(num_actions)
        print(actions)
        current_time=time.time()
        print("Execution time in seconds: ", current_time - start_time)
        # write to file
        f = open('BFS.txt','w')
        f.write(str(num_actions)+'\n'+actions)
        f.close()
    elif (number=='2'):
        # domain independent: perform desired search algorithm given the graph
        num_nodes,actions=DFS(graph,start,goal)
        # domain dependent: translate node path into (UDLR) movements
        num_actions,actions=translate_output(actions,num_nodes)
        # print result
        print(num_actions)
        print(actions)
        current_time=time.time()
        print("Execution time in seconds: ", current_time - start_time)
        # write to file
        f = open('DFS.txt','w')
        f.write(str(num_actions)+'\n'+actions)
        f.close()
    elif (number=='3'):
        limit=input('Enter limit for maximum Depth of search:')
        start_time = time.time()
        # domain independent: perform desired search algorithm given the graph
        num_nodes,actions=IdDFS(graph,start,goal,int(limit))
        # domain dependent: translate node path into (UDLR) movements
        num_actions,actions=translate_output(actions,num_nodes)
        # print result
        print(num_actions)
        print(actions)
        current_time=time.time()
        print("Execution time in seconds: ", current_time - start_time)
        # write to file
        f = open('IdDFS.txt','w')
        f.write(str(num_actions)+'\n'+actions)
        f.close() 
    elif (number=='4'):
        # domain independent: perform desired search algorithm given the graph
        num_nodes,actions=Greedy(graph,start,goal,h_func)
        # domain dependent: translate node path into (UDLR) movements
        num_actions,actions=translate_output(actions,num_nodes)
        # print result
        print(num_actions)
        print(actions)
        current_time=time.time()
        print("Execution time in seconds: ", current_time - start_time)
        # write to file
        f = open('Greedy.txt','w')
        f.write(str(num_actions)+'\n'+actions)
        f.close()
    elif (number=='5'):
        # domain independent: perform desired search algorithm given the graph
        num_nodes,actions=Astar(graph,start,goal,h_func,n_func)
        # domain dependent: translate node path into (UDLR) movements
        num_actions,actions=translate_output(actions,num_nodes)
        # print result
        print(num_actions)
        print(actions)
        current_time=time.time()
        print("Execution time in seconds: ", current_time - start_time)
        # write to file
        f = open('Astar.txt','w')
        f.write(str(num_actions)+'\n'+actions)
        f.close()
    elif (number=='6'):
        # domain independent: perform desired search algorithm given the graph
        num_nodes,actions=IDAstar(graph,start,goal,h_func,n_func)
        # domain dependent: translate node path into (UDLR) movements
        num_actions,actions=translate_output(actions,num_nodes)
        # print result
        print(num_actions)
        print(actions)
        current_time=time.time()
        print("Execution time in seconds: ", current_time - start_time)
        # write to file
        f = open('IDAstar.txt','w')
        f.write(str(num_actions)+'\n'+actions)
        f.close()
    elif (number=='q'):
        print('Thank you for using Labyrinth Solver 1.0')
    else:
        print('Menu entry not recognized. Please try again...')
        
