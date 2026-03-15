from collections import deque

# BFS for a single connected component
def bfsConnected(adj, src, visited, res):
    q = deque()
    visited[src] = True
    q.append(src)

    while q:
        curr = q.popleft()
        res.append(curr)

        # visit all the unvisited
        # neighbours of current node
        for x in adj[curr]:
            if not visited[x]:
                visited[x] = True
                q.append(x)

# BFS for all components (handles disconnected graphs)
def bfs(adj):
    V = len(adj)
    visited = [False] * V
    res = []

    for i in range(V):
        if not visited[i]:
            bfsConnected(adj, i, visited, res)
    return res
