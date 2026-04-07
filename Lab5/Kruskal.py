class UnionFind:
    """Union-Find (Disjoint Set Union) with path compression and union by rank."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(edges, n):
    """
    Kruskal's Algorithm for Minimum Spanning Tree.

    Parameters:
        edges : list of (weight, u, v) tuples representing all graph edges
        n     : number of vertices

    Returns:
        mst_edges   : list of (u, v, weight) tuples in the MST
        total_weight: total weight of the MST
    """
    sorted_edges = sorted(edges, key=lambda e: e[0])
    uf = UnionFind(n)
    mst_edges = []
    total_weight = 0

    for w, u, v in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == n - 1:
                break   # MST complete

    return mst_edges, total_weight