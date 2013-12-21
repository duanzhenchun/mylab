# ----------
# User Instructions:
# 
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

heuristic = [[9, 8, 7, 6, 5, 4],
            [8, 7, 6, 5, 4, 3],
            [7, 6, 5, 4, 3, 2],
            [6, 5, 4, 3, 2, 1],
            [5, 4, 3, 2, 1, 0]]
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def move(pos,direct):
    return [sum(i) for i in zip(pos, direct)]
    
def in_border(pos):
    return 0<=pos[0]<len(grid) and 0<=pos[1]<len(grid[0])

def neighbor(pos, visited):
    for d in delta:
        newp = move(pos, d)
        if not in_border(newp) or grid[newp[0]][newp[1]] or visited[newp[0]][newp[1]]:
            continue
        yield newp

def f(g,x,y):
    return g+heuristic[x][y]

def search():
    start = [0] + init  #[steps,x,y]
    visited = []
    for i in range(len(grid)):
        visited.append([0,]*len(grid[0]))
    more = [start]
    while more:
        cur = more.pop(0)
        x,y=cur[1:]
        visited[x][y]=1
        for newp in neighbor(cur[1:], visited):
            if newp in more:
                continue
            more.append([cur[0]+cost] + newp)        
            if more[-1][1:] == goal:
                return more[-1]
    return None
    #return path # you should RETURN your result

print search()

