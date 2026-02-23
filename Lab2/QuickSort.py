import random
import time
import matplotlib.pyplot as plt

SWAP_COUNT = 0

# the QuickSort function implementation
def quick_sort(arr, low, high):
    if low < high:
        
        # pi is the partition return index of pivot
        pi = partition(arr, low, high)
        
        # recursion calls for smaller elements
        # and greater or equals elements
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
# partition function
def partition(arr, low, high):
    
    # choose the pivot
    pivot = arr[high]
    
    # index of smaller element and indicates 
    # the right position of pivot found so far
    i = low - 1
    
    # traverse arr[low..high] and move all smaller
    # elements to the left side. Elements from low to 
    # i are smaller after every iteration
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            swap(arr, i, j)
    
    # move pivot after smaller elements and
    # return its position
    swap(arr, i + 1, high)
    return i + 1

# swap function
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

def quickSort(arr):
    quick_sort(arr, 0, len(arr) - 1)

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
            quickSort(arr)
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

    axes[0].plot(test_sizes, times, marker="o", linestyle="-", label="Quick Sort Time")
    axes[0].set_title("Quick Sort Execution Time")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Time (ms)")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(test_sizes, swaps, marker="o", linestyle="-", label="Quick Sort Swaps")
    axes[1].set_title("Quick Sort Swap Count")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Number of Swaps")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    performance()