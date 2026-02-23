import random
import time
import matplotlib.pyplot as plt

SWAP_COUNT = 0

# To heapify a subtree rooted with node i
def heapify(arr, n, i):

    # Initialize largest as root
    largest = i

    # left index = 2*i + 1
    l = 2 * i + 1

    # right index = 2*i + 2
    r = 2 * i + 2

    # If left child is larger than root
    if l < n and arr[l] > arr[largest]:
        largest = l

    # If right child is larger than largest so far
    if r < n and arr[r] > arr[largest]:
        largest = r

    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]

        # Recursively heapify the affected sub-tree
        heapify(arr, n, largest)

# Main function to do heap sort
def heapSort(arr):
    n = len(arr)

    # Build heap (rearrange vector)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract an element from heap
    for i in range(n - 1, 0, -1):

        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]

        # Call max heapify on the reduced heap
        heapify(arr, i, 0)

def performance():
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3

    times = []
    swaps = []

    header = "n     " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "   avg(ms)"
    print(header)
    print("-" * len(header))

    for n in test_sizes:
        run_times = []
        swap_for_n = 0

        for _ in range(repeats):
            global SWAP_COUNT
            SWAP_COUNT = 0

            arr = [random.randint(0, 100000) for _ in range(n)]

            start = time.perf_counter()
            heapSort(arr)
            end = time.perf_counter()

            run_times.append((end - start) * 1000)
            swap_for_n = SWAP_COUNT

        avg_time = sum(run_times) / repeats

        row = f"{n:<5} " + "  ".join(f"{t:>10.3f}" for t in run_times) + f"  {avg_time:>10.3f}"
        print(row)

        times.append(avg_time)
        swaps.append(swap_for_n)

    # 🔹 Graphs
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(test_sizes, times, marker="o", linestyle="-", label="Heap Sort Time")
    axes[0].set_title("Heap Sort Execution Time")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Time (ms)")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(test_sizes, swaps, marker="o", linestyle="-", label="Heap Sort Swaps")
    axes[1].set_title("Heap Sort Swap Count")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Number of Swaps")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    performance()