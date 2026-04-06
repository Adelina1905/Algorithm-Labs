
# ─────────────────────────────────────────────
# Floyd-Warshall Algorithm
# ─────────────────────────────────────────────
INF = float('inf')

def floyd_warshall(mat):
    """
    Floyd-Warshall all-pairs shortest path algorithm.
    mat: n x n adjacency matrix (INF for no edge, 0 on diagonal).
    Returns: dist[][] n x n shortest distance matrix.
    """
    n = len(mat)
    dist = [row[:] for row in mat]  # deep copy

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
