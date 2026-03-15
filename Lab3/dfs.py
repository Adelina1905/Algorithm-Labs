from collections import defaultdict

def dfsRec(adj, visited, s, res):
    visited[s] = True
    res.append(s)

    # Recursively visit all adjacent 
    # vertices that are not visited yet
    for i in adj[s]:
        if not visited[i]:
            dfsRec(adj, visited, i, res)


def dfs(adj):
    visited = [False] * len(adj)
    res = []
    # Loop through all vertices to 
    # handle disconnected graph
    for i in range(len(adj)):
        if not visited[i]:
            dfsRec(adj, visited, i, res)
    return res

