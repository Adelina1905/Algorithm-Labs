"""
CaseTesting.py
==============
Empirical analysis of Prim's and Kruskal's algorithms.
Measures average execution time across sparse and dense graphs
of increasing size, then plots the results.
"""
import os
import time
import random
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from Prim import prim
from Kruskal import kruskal

# ─────────────────────────── graph generators ──────────────────────────────

def generate_graph(n, density, seed=None):
    """
    Generate a random connected undirected weighted graph.

    Returns:
        adj  : adjacency list  (for Prim)
        edges: list of (w, u, v) (for Kruskal)
    """
    rng = random.Random(seed)
    adj = [[] for _ in range(n)]
    edge_set = set()

    # Guarantee connectivity via a random spanning tree
    vertices = list(range(n))
    rng.shuffle(vertices)
    for i in range(1, n):
        u, v = vertices[i - 1], vertices[i]
        w = rng.randint(1, 100)
        adj[u].append((v, w))
        adj[v].append((u, w))
        edge_set.add((min(u, v), max(u, v), w))

    # Add extra edges to match target density
    max_edges = n * (n - 1) // 2
    target = int(density * max_edges)

    # Build set of existing (u,v) pairs for fast lookup
    existing = {(e[0], e[1]) for e in edge_set}

    # Sample candidate pairs (all pairs shuffled, pick until target reached)
    all_pairs = [(u, v) for u in range(n) for v in range(u + 1, n)
                 if (u, v) not in existing]
    rng.shuffle(all_pairs)
    for u, v in all_pairs:
        if len(edge_set) >= target:
            break
        w = rng.randint(1, 100)
        adj[u].append((v, w))
        adj[v].append((u, w))
        edge_set.add((u, v, w))

    edges = [(w, u, v) for u, v, w in edge_set]
    return adj, edges


# ─────────────────────────── timing helpers ────────────────────────────────

RUNS = 3          # repetitions per configuration
ERROR_MS = 2.5    # experimental error margin (ms)


def time_prim(adj, n):
    t0 = time.perf_counter()
    prim(adj, n)
    return (time.perf_counter() - t0) * 1000


def time_kruskal(edges, n):
    t0 = time.perf_counter()
    kruskal(edges, n)
    return (time.perf_counter() - t0) * 1000


def avg_time(func, *args):
    times = [func(*args) for _ in range(RUNS)]
    return statistics.mean(times)


# ─────────────────────────── experiment ────────────────────────────────────

SIZES   = [10, 50, 100, 200, 300, 500]
DENSITY = {"sparse": 0.20, "dense": 0.80}

results = {
    "sparse": {"prim": [], "kruskal": []},
    "dense":  {"prim": [], "kruskal": []},
}

print(f"{'n':>6}  {'density':>8}  {'Prim (ms)':>12}  {'Kruskal (ms)':>14}")
print("-" * 50)

for label, d in DENSITY.items():
    for n in SIZES:
        adj, edges = generate_graph(n, d, seed=42)

        t_prim    = avg_time(time_prim,    adj, n)
        t_kruskal = avg_time(time_kruskal, edges, n)

        results[label]["prim"].append(t_prim)
        results[label]["kruskal"].append(t_kruskal)

        print(f"{n:>6}  {label:>8}  {t_prim:>12.4f}  {t_kruskal:>14.4f}")

# ─────────────────────────── table print ───────────────────────────────────

def print_table(label):
    d = results[label]
    print(f"\n{'─'*55}")
    print(f"  {label.upper()} GRAPHS  (density = {DENSITY[label]:.0%})")
    print(f"{'─'*55}")
    print(f"  {'n':>5}  {'Prim (ms)':>12}  {'Kruskal (ms)':>14}")
    print(f"  {'─'*5}  {'─'*12}  {'─'*14}")
    for i, n in enumerate(SIZES):
        print(f"  {n:>5}  {d['prim'][i]:>12.4f}  {d['kruskal'][i]:>14.4f}")

print_table("sparse")
print_table("dense")

# ─────────────────────────── plots ─────────────────────────────────────────

COLORS = {"prim": "#2563EB", "kruskal": "#DC2626"}


def make_comparison_plot(label, filename):
    fig, ax = plt.subplots(figsize=(9, 5))
    d = results[label]

    ax.plot(SIZES, d["prim"],    marker="o", linewidth=2.0,
            color=COLORS["prim"],    label="Prim")
    ax.plot(SIZES, d["kruskal"], marker="s", linewidth=2.0,
            color=COLORS["kruskal"], label="Kruskal")

    ax.fill_between(SIZES,
                    [v - ERROR_MS for v in d["prim"]],
                    [v + ERROR_MS for v in d["prim"]],
                    alpha=0.12, color=COLORS["prim"])
    ax.fill_between(SIZES,
                    [v - ERROR_MS for v in d["kruskal"]],
                    [v + ERROR_MS for v in d["kruskal"]],
                    alpha=0.12, color=COLORS["kruskal"])

    ax.set_title(f"Prim vs Kruskal — {label.capitalize()} Graphs (density = {DENSITY[label]:.0%})",
                 fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Number of Vertices (n)", fontsize=11)
    ax.set_ylabel("Execution Time (ms)", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_locator(mticker.FixedLocator(SIZES))
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {filename}")


def make_individual_plot(algo_name, filename):
    fig, ax = plt.subplots(figsize=(9, 5))
    color = COLORS[algo_name]

    for label, linestyle in [("sparse", "--"), ("dense", "-")]:
        d = results[label][algo_name]
        ax.plot(SIZES, d, marker="o", linewidth=2.0,
                linestyle=linestyle, color=color,
                label=f"{label.capitalize()} (density={DENSITY[label]:.0%})")
        ax.fill_between(SIZES,
                        [v - ERROR_MS for v in d],
                        [v + ERROR_MS for v in d],
                        alpha=0.10, color=color)

    title = "Prim's" if algo_name == "prim" else "Kruskal's"
    ax.set_title(f"{title} Algorithm — Sparse vs Dense", fontsize=13,
                 fontweight="bold", pad=12)
    ax.set_xlabel("Number of Vertices (n)", fontsize=11)
    ax.set_ylabel("Execution Time (ms)", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_locator(mticker.FixedLocator(SIZES))
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {filename}")
    
os.makedirs("images", exist_ok=True)

print("\nGenerating plots …")
make_comparison_plot("sparse", "images/Comparison_sparse.png")
make_comparison_plot("dense",  "images/Comparison_dense.png")
make_individual_plot("prim",    "images/Prim_graph.png")
make_individual_plot("kruskal", "images/Kruskal_graph.png")
print("Done.")