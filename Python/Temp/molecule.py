huckel = [[0,1,1,0,0,0],
          [1,0,1,0,0,0],
          [1,1,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0],
          [0,0,0,0,0,0]]

N = len(huckel)

graph = [[] for i in range(N)]
cycles = [[] for i in range(N)]

def dfs_cycle(u, p, color: list,
              par: list):
    global cyclenumber

    if color[u] == 2:
        return

    if color[u] == 1:
        v = []
        cur = p
        v.append(cur)

        while cur != u:
            cur = par[cur]
            v.append(cur)
        cycles[cyclenumber] = v
        cyclenumber += 1
 
        return
 
    par[u] = p

    color[u] = 1

    for v in graph[u]:

        if v == par[u]:
            continue
        dfs_cycle(v, u, color, par)

    color[u] = 2

def addEdge(u, v):
    graph[u].append(v)
    graph[v].append(u)

def printCycles():

    for i in range(0, cyclenumber):
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

    color = [0] * N
    par = [0] * N
    cyclenumber = 0
    dfs_cycle(1, 0, color, par)
    printCycles()
