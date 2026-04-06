import time
import random
import heapq

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

from Djikstra import dijkstra
from Floyd import floyd_warshall
# ─────────────────────────────────────────────
# Graph generation
# ─────────────────────────────────────────────

INF = float('inf')

def generate_graph_adjacency_list(n, density, weighted=True, max_weight=100):
    """Generate a random undirected weighted graph as adjacency list."""
    adj = {i: [] for i in range(n)}
    max_edges = n * (n - 1) // 2
    target_edges = int(max_edges * density)
    edges_added = 0
    edge_set = set()

    # Ensure connectivity with a spanning tree
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u, v = nodes[i-1], nodes[i]
        w = random.randint(1, max_weight)
        adj[u].append((v, w))
        adj[v].append((u, w))
        edge_set.add((min(u,v), max(u,v)))
        edges_added += 1

    # Add remaining edges
    attempts = 0
    while edges_added < target_edges and attempts < target_edges * 10:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v:
            key = (min(u,v), max(u,v))
            if key not in edge_set:
                w = random.randint(1, max_weight)
                adj[u].append((v, w))
                adj[v].append((u, w))
                edge_set.add(key)
                edges_added += 1
        attempts += 1
    return adj

def generate_graph_matrix(n, density, max_weight=100):
    """Generate a random undirected weighted graph as adjacency matrix."""
    mat = [[INF]*n for _ in range(n)]
    for i in range(n):
        mat[i][i] = 0

    max_edges = n * (n - 1) // 2
    target_edges = int(max_edges * density)
    edges_added = 0
    edge_set = set()

    # Spanning tree
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u, v = nodes[i-1], nodes[i]
        w = random.randint(1, 100)
        mat[u][v] = w
        mat[v][u] = w
        edge_set.add((min(u,v), max(u,v)))
        edges_added += 1

    attempts = 0
    while edges_added < target_edges and attempts < target_edges * 10:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v:
            key = (min(u,v), max(u,v))
            if key not in edge_set:
                w = random.randint(1, max_weight)
                mat[u][v] = w
                mat[v][u] = w
                edge_set.add(key)
                edges_added += 1
        attempts += 1
    return mat




# ─────────────────────────────────────────────
# Empirical Analysis
# ─────────────────────────────────────────────

VERTEX_COUNTS = [10, 50, 100, 200, 300, 500]
REPEATS = 5
DENSITIES = {'sparse': 0.2, 'dense': 0.8}

def measure_dijkstra(n, density):
    times = []
    for _ in range(REPEATS):
        adj = generate_graph_adjacency_list(n, density)
        src = random.randint(0, n-1)
        t0 = time.perf_counter()
        dijkstra(adj, src)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)

def measure_floyd(n, density):
    times = []
    for _ in range(REPEATS):
        mat = generate_graph_matrix(n, density)
        t0 = time.perf_counter()
        floyd_warshall(mat)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return sum(times) / len(times)

def run_experiments():
    results = {
        'dijkstra': {'sparse': [], 'dense': []},
        'floyd':    {'sparse': [], 'dense': []},
    }
    print(f"{'n':>6} | {'Dijk sparse':>14} | {'Dijk dense':>14} | {'Floyd sparse':>14} | {'Floyd dense':>14}")
    print("-" * 70)
    for n in VERTEX_COUNTS:
        row = {'n': n}
        for label, density in DENSITIES.items():
            d = measure_dijkstra(n, density)
            f = measure_floyd(n, density)
            results['dijkstra'][label].append(d)
            results['floyd'][label].append(f)
            row[f'dijk_{label}'] = d
            row[f'floyd_{label}'] = f
        print(f"{n:>6} | {row['dijk_sparse']*1000:>12.4f}ms | {row['dijk_dense']*1000:>12.4f}ms | "
              f"{row['floyd_sparse']*1000:>12.4f}ms | {row['floyd_dense']*1000:>12.4f}ms")
    return results

# ─────────────────────────────────────────────
# Plotting helpers
# ─────────────────────────────────────────────

COLORS = {'dijkstra_sparse': '#2196F3', 'dijkstra_dense': '#0D47A1',
          'floyd_sparse':    '#FF9800', 'floyd_dense':    '#E65100'}

def save_plot(path, title, x, datasets, ylabel='Execution Time (ms)', xlabel='Number of Vertices'):
    fig, ax = plt.subplots(figsize=(9, 5))
    for label, y_sec, color, marker in datasets:
        y_ms = [v * 1000 for v in y_sec]
        ax.plot(x, y_ms, marker=marker, label=label, color=color, linewidth=2, markersize=6)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")

def save_table_image(path, title, headers, rows):
    """Render a results table as an image."""
    fig, ax = plt.subplots(figsize=(10, len(rows)*0.55 + 1.2))
    ax.axis('off')
    tbl = ax.table(cellText=rows, colLabels=headers, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor('#1565C0')
            cell.set_text_props(color='white', fontweight='bold')
        elif r % 2 == 0:
            cell.set_facecolor('#E3F2FD')
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved: {path}")

# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == '__main__':
    random.seed(42)
    os.makedirs('images', exist_ok=True)

    print("\n=== Running empirical analysis ===\n")
    results = run_experiments()

    x = VERTEX_COUNTS
    dijk_sp = results['dijkstra']['sparse']
    dijk_de = results['dijkstra']['dense']
    floyd_sp = results['floyd']['sparse']
    floyd_de = results['floyd']['dense']

    # 1. Dijkstra graph
    save_plot('images/Dijkstra_graph.png',
              "Dijkstra's Algorithm – Execution Time",
              x,
              [('Dijkstra Sparse (20%)', dijk_sp, COLORS['dijkstra_sparse'], 'o'),
               ('Dijkstra Dense (80%)',  dijk_de, COLORS['dijkstra_dense'],  's')])

    # 2. Floyd-Warshall graph
    save_plot('images/Floyd_graph.png',
              'Floyd-Warshall Algorithm – Execution Time',
              x,
              [('Floyd-Warshall Sparse (20%)', floyd_sp, COLORS['floyd_sparse'], 'o'),
               ('Floyd-Warshall Dense (80%)',  floyd_de, COLORS['floyd_dense'],  's')])

    # 3. Comparison sparse
    save_plot('images/Comparison_sparse.png',
              'BFS vs DFS on Sparse Graphs (density = 0.2)',
              x,
              [("Dijkstra Sparse",      dijk_sp,  COLORS['dijkstra_sparse'], 'o'),
               ("Floyd-Warshall Sparse", floyd_sp, COLORS['floyd_sparse'],    's')])

    # 4. Comparison dense
    save_plot('images/Comparison_dense.png',
              'Dijkstra vs Floyd-Warshall on Dense Graphs (density = 0.8)',
              x,
              [("Dijkstra Dense",      dijk_de,  COLORS['dijkstra_dense'], 'o'),
               ("Floyd-Warshall Dense", floyd_de, COLORS['floyd_dense'],   's')])

    # 5. Dijkstra results table image
    headers_d = ['n', 'Sparse (ms)', 'Dense (ms)']
    rows_d = [[str(n), f"{s*1000:.4f}", f"{d*1000:.4f}"]
              for n, s, d in zip(x, dijk_sp, dijk_de)]
    save_table_image('images/Dijkstra_results.png',
                     "Dijkstra's Algorithm – Results", headers_d, rows_d)

    # 6. Floyd results table image
    headers_f = ['n', 'Sparse (ms)', 'Dense (ms)']
    rows_f = [[str(n), f"{s*1000:.4f}", f"{d*1000:.4f}"]
              for n, s, d in zip(x, floyd_sp, floyd_de)]
    save_table_image('images/Floyd_results.png',
                     'Floyd-Warshall Algorithm – Results', headers_f, rows_f)

    # 7. Comparison sparse table
    headers_cs = ['n', 'Dijkstra (ms)', 'Floyd-Warshall (ms)']
    rows_cs = [[str(n), f"{d*1000:.4f}", f"{f*1000:.4f}"]
               for n, d, f in zip(x, dijk_sp, floyd_sp)]
    save_table_image('images/Table_comparison_sparse.png',
                     'Dijkstra vs Floyd-Warshall – Sparse Graphs', headers_cs, rows_cs)

    # 8. Comparison dense table
    headers_cd = ['n', 'Dijkstra (ms)', 'Floyd-Warshall (ms)']
    rows_cd = [[str(n), f"{d*1000:.4f}", f"{f*1000:.4f}"]
               for n, d, f in zip(x, dijk_de, floyd_de)]
    save_table_image('images/Table_comparison_dense.png',
                     'Dijkstra vs Floyd-Warshall – Dense Graphs', headers_cd, rows_cd)

    print("\n=== All images saved to images/ ===")
