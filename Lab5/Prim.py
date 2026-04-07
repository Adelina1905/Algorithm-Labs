import heapq

INF = float('inf')


def prim(adj, n):
    """
    Prim's Algorithm for Minimum Spanning Tree.

    Parameters:
        adj : adjacency list — list of lists of (neighbor, weight) tuples
        n   : number of vertices

    Returns:
        mst_edges : list of (u, v, weight) tuples in the MST
        total_weight : total weight of the MST
    """
    visited = [False] * n
    min_heap = [(0, 0, -1)]   # (weight, vertex, parent)
    mst_edges = []
    total_weight = 0

    while min_heap:
        w, u, parent = heapq.heappop(min_heap)

        if visited[u]:
            continue

        visited[u] = True
        total_weight += w

        if parent != -1:
            mst_edges.append((parent, u, w))

        for v, edge_w in adj[u]:
            if not visited[v]:
                heapq.heappush(min_heap, (edge_w, v, u))

    return mst_edges, total_weight