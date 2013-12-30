import numpy as np


# Grid format: 1:occupied, 0:empty
grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]
grid=np.array(grid,dtype=int)
init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

def make_heuristic(grid, goal):
    H = [[0 for row in range(len(grid[0]))] 
            for col in range(len(grid))]
    for i in range(len(grid)):    
        for j in range(len(grid[0])):
            H[i][j] = abs(i - goal[0]) + abs(j - goal[1])
    return np.array(H,dtype=int)
    
heuristic = make_heuristic(grid, goal)

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def move(pos,direct):
    return [sum(i) for i in zip(pos, direct)]
    
def in_border(x,y):
    return 0<=x<len(grid) and 0<=y<len(grid[0])

def neighbor(pos, visited, more):
    for d in delta:
        newp = move(pos, d)
        x,y=newp
        if newp in more or not in_border(x,y) or grid[x,y] or visited[x,y]:
            continue
        visited[x,y]=1
        yield newp

def track(expand,start,end):
    pos=end
    m,n=expand.shape
    road=np.array([[' ',]*n]*m)
    road_grid=[]
    while True:
        for i,d in enumerate(delta):
            newp=move(pos,d)
            if not in_border(newp[0],newp[1]):
                continue
            if expand[newp[0],newp[1]]==expand[pos[0],pos[1]]-cost:
                road[pos[0],pos[1]]=delta_name[i]
                print pos
                road_grid.append(pos)
                pos=newp
                if pos == start:
                   return road, list(reversed(road_grid))
                else:
                   break 
    return road,road_grid

def f(g,x,y):
    return g+heuristic[x,y]

def search():
    start = [0, heuristic[init[0],init[1]]]  + init  #[steps,f,x,y]
    visited = np.zeros(grid.shape)
    visited[init[0],init[1]]=1
    expand=np.ones(grid.shape,dtype=int)*-1
    more = [start]
    while more:
        cur=more.pop(np.argmin(zip(*more)[0]))
        #cur = more.pop(0)
        x,y=cur[2:]
        expand[x,y]=cur[0]
        if cur[2:] == goal:
            return expand
        for newp in neighbor(cur[2:], visited, more):
            g=cur[0]+cost
            more.append([g, f(g, newp[0],newp[1])] + newp)        
    return None
    #return path # you should RETURN your result

if __name__=="__main__":
    expand=search()
    print expand
    road, path= track(expand,init,goal)
    print road
    import smooth_control
    newpath = smooth_control.smooth(path, 0.5, 0.1)
    smooth_control.visual(path, newpath)

