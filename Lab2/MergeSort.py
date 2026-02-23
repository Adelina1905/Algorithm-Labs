import random
import time
import matplotlib.pyplot as plt

MERGE_COUNT = 0
def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    # Create temp arrays
    L = [0] * n1
    R = [0] * n2

    # Copy data to temp arrays L[] and R[]
    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]
        
    i = 0  
    j = 0  
    k = left  

    # Merge the temp arrays back
    # into arr[left..right]
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copy the remaining elements of L[],
    # if there are any
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copy the remaining elements of R[], 
    # if there are any
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

def mergeSortWrapper(arr, left, right):
    if left < right:
        mid = (left + right) // 2

        mergeSortWrapper(arr, left, mid)
        mergeSortWrapper(arr, mid + 1, right)
        merge(arr, left, mid, right)

def mergeSort(arr):
    mergeSortWrapper(arr, 0, len(arr) - 1)


# 🔹 Performance test
def performance():
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3

    times = []
    merges = []

    header = "n     " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "   avg(ms)"
    print(header)
    print("-" * len(header))

    for n in test_sizes:
        run_times = []
        merge_for_n = 0

        for _ in range(repeats):
            global MERGE_COUNT
            MERGE_COUNT = 0

            arr = [random.randint(0, 100000) for _ in range(n)]

            start = time.perf_counter()
            mergeSort(arr)
            end = time.perf_counter()

            run_times.append((end - start) * 1000)
            merge_for_n = MERGE_COUNT

        avg_time = sum(run_times) / repeats

        row = f"{n:<5} " + "  ".join(f"{t:>10.3f}" for t in run_times) + f"  {avg_time:>10.3f}"
        print(row)

        times.append(avg_time)
        merges.append(merge_for_n)

    # 🔹 Graphs
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(test_sizes, times, marker="o", linestyle="-", label="Merge Sort Time")
    axes[0].set_title("Merge Sort Execution Time")
    axes[0].set_xlabel("Array Size (n)")
    axes[0].set_ylabel("Time (ms)")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(test_sizes, merges, marker="o", linestyle="-", label="Merge Operations")
    axes[1].set_title("Merge Sort Merge Count")
    axes[1].set_xlabel("Array Size (n)")
    axes[1].set_ylabel("Number of Merges")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    performance()