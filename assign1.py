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

