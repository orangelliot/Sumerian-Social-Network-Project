huckel = [[0,1,1,0,0,0],
          [1,0,1,0,0,0],
          [1,1,0,1,0,0],
          [0,0,1,0,1,1],
          [0,0,0,1,0,1],
          [0,0,0,1,1,0]]

N = len(huckel)
 
# variables to be used
# in both functions
graph = [[] for i in range(N)]
cycles = [[] for i in range(N)]
 
 
# Function to mark the vertex with
# different colors for different cycles
def dfs_cycle(u, p, color: list,
              par: list):
    global cyclenumber
 
    # already (completely) visited vertex.
    if color[u] == 2:
        return
 
    # seen vertex, but was not
    # completely visited -> cycle detected.
    # backtrack based on parents to
    # find the complete cycle.
    if color[u] == 1:
        v = []
        cur = p
        v.append(cur)
 
        # backtrack the vertex which are
        # in the current cycle thats found
        while cur != u:
            cur = par[cur]
            v.append(cur)
        cycles[cyclenumber] = v
        cyclenumber += 1
 
        return
 
    par[u] = p
 
    # partially visited.
    color[u] = 1
 
    # simple dfs on graph
    for v in graph[u]:
 
        # if it has not been visited previously
        if v == par[u]:
            continue
        dfs_cycle(v, u, color, par)
 
    # completely visited.
    color[u] = 2
 
# add the edges to the graph
def addEdge(u, v):
    graph[u].append(v)
    graph[v].append(u)
 
# Function to print the cycles
def printCycles():
 
    # print all the vertex with same cycle
    for i in range(0, cyclenumber):
 
        # Print the i-th cycle
        print("Cycle Number %d:" % (i+1), end = " ")
        for x in cycles[i]:
            print(x, end = " ")
        print()
 
# Driver Code
if __name__ == "__main__":
 
    for i in range(N):
        for j in range(i):
            if huckel[i][j] == 1:
                addEdge(i,j)
 
    # arrays required to color the
    # graph, store the parent of node
    color = [0] * N
    par = [0] * N
 
    # store the numbers of cycle
    cyclenumber = 0
 
    # call DFS to mark the cycles
    dfs_cycle(1, 0, color, par)
 
    # function to print the cycles
    printCycles()
