import random
import time
import matplotlib.pyplot as plt
from bfs import bfs       # your bfs function from bfs.py
from dfs import dfs       # your dfs function from dfs.py
import sys
sys.setrecursionlimit(5000) 
# Generate a random undirected graph with V vertices and given density
def generate_graph(V, density=0.1):
    adj = [[] for _ in range(V)]
    max_edges = V * (V - 1) // 2
    num_edges = int(max_edges * density)
    
    edges = set()
    while len(edges) < num_edges:
        u = random.randint(0, V - 1)
        v = random.randint(0, V - 1)
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            adj[u].append(v)
            adj[v].append(u)
    return adj

# Parameters
vertex_sizes = [10, 50, 100, 500, 1000, 2000]
densities = [0.2, 0.8]  # sparse and dense
repeats = 5  # repeat each experiment to average

# Store results
results_bfs = {d: [] for d in densities}
results_dfs = {d: [] for d in densities}

for density in densities:
    for V in vertex_sizes:
        bfs_times = []
        dfs_times = []
        for _ in range(repeats):
            graph = generate_graph(V, density)
            
            # BFS timing
            start = time.perf_counter()
            bfs(graph)
            end = time.perf_counter()
            bfs_times.append(end - start)
            
            # DFS timing
            start = time.perf_counter()
            dfs(graph)
            end = time.perf_counter()
            dfs_times.append(end - start)
        
        # Average times
        avg_bfs = sum(bfs_times) / repeats
        avg_dfs = sum(dfs_times) / repeats
        results_bfs[density].append(avg_bfs)
        results_dfs[density].append(avg_dfs)

# Plot results
for density in densities:
    plt.figure(figsize=(10, 6))
    plt.plot(vertex_sizes, results_bfs[density], marker='o', label='BFS')
    plt.plot(vertex_sizes, results_dfs[density], marker='x', label='DFS')
    plt.xlabel("Number of vertices")
    plt.ylabel("Execution time (seconds)")
    plt.title(f"Empirical Analysis of BFS and DFS, Density = {density}")
    plt.legend()
    plt.grid(True)
    plt.show()