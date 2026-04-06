import heapq
# ─────────────────────────────────────────────
# Dijkstra's Algorithm
# ─────────────────────────────────────────────
INF = float('inf')

def dijkstra(adj, src):
    """
    Dijkstra's algorithm using a min-heap priority queue.
    adj: dict of {node: [(neighbor, weight), ...]}
    Returns: dist[] array of shortest distances from src.
    """
    n = len(adj)
    dist = [INF] * n
    dist[src] = 0
    heap = [(0, src)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist