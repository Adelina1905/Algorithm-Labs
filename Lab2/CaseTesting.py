import random
import time
import matplotlib.pyplot as plt
from QuickSort import quickSort
from MergeSort import mergeSort
from CountingSort import count_sort
from HeapSort import heapSort

# =========================================================
# 🔹 DATA GENERATORS
# =========================================================

def gen_random_integers(n):
    return [random.randint(0, 100000) for _ in range(n)]

def gen_sorted_ascending(n):
    return list(range(n))

def gen_sorted_descending(n):
    return list(range(n, 0, -1))

def gen_negative_numbers(n):
    return [random.randint(-10_000, -1) for _ in range(n)]

def gen_floating_point(n):
    return [random.uniform(-1000.0, 1000.0) for _ in range(n)]

def gen_complex_magnitudes(n):
    return [abs(complex(random.uniform(-100, 100), random.uniform(-100, 100)))
            for _ in range(n)]

def gen_nearly_sorted(n):
    arr = list(range(n))
    swaps = int(n * 0.05)  # 5% swapped
    for _ in range(swaps):
        i, j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def gen_many_duplicates(n):
    return [random.randint(0, 10) for _ in range(n)]


INPUT_TYPES = {
    "Random Integers":      gen_random_integers,
    "Sorted Ascending":     gen_sorted_ascending,
    "Sorted Descending":    gen_sorted_descending,
    "Negative Numbers":     gen_negative_numbers,
    "Floating Point":       gen_floating_point,
    "Complex (Magnitude)":  gen_complex_magnitudes,
    "Nearly Sorted":        gen_nearly_sorted,
    "Many Duplicates":      gen_many_duplicates,
}

# =========================================================
# 🔹 TIMER (AVERAGED)
# =========================================================

def measure_time_avg(sort_function, arr, runs=3):
    total = 0.0
    for _ in range(runs):
        data = arr.copy()
        start = time.perf_counter()
        sort_function(data)
        end = time.perf_counter()
        total += (end - start)
    return total / runs

# =========================================================
# 🔹 BENCHMARK RUNNER
# =========================================================

sizes = [1000, 5000, 10000, 20000, 50000]

SORTS = {
    "Quick Sort": quickSort,
    "Merge Sort": mergeSort,
    "Heap Sort": heapSort,
    "Count Sort": count_sort
}

def run_all_cases_subplots():
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()

    for idx, (case_name, generator) in enumerate(INPUT_TYPES.items()):
        print(f"\n=== CASE: {case_name} ===")

        results = {name: [] for name in SORTS.keys()}

        for n in sizes:
            print(f"Testing size {n}...")
            arr = generator(n)

            for sort_name, sort_func in SORTS.items():
                try:
                    t = measure_time_avg(sort_func, arr)
                except Exception as e:
                    t = None
                    print(f"{sort_name} failed on {case_name} with size {n}: {e}")
                results[sort_name].append(t)

        ax = axes[idx]

        for sort_name, times in results.items():
            if any(t is None for t in times):
                continue
            ax.plot(sizes, times, label=sort_name)

        ax.set_title(case_name)
        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel("Time (seconds)")
        ax.grid(True)
        ax.legend(fontsize=7)

    plt.suptitle("Sorting Performance Across Input Types", fontsize=16)
    plt.tight_layout()
    plt.show()

# =========================================================
# 🔹 MAIN
# =========================================================

if __name__ == "__main__":
    run_all_cases_subplots()