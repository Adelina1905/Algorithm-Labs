import random
import time
import matplotlib.pyplot as plt

def count_sort(arr):
    if not arr:
        return []

    n = len(arr)
    maxval = max(arr)

    # create and initialize cntArr
    cntArr = [0] * (maxval + 1)

    # count frequency of each element
    for v in arr:
        cntArr[v] += 1

    # compute prefix sums
    for i in range(1, maxval + 1):
        cntArr[i] += cntArr[i - 1]

    # build output array
    ans = [0] * n
    # iterate in reverse to keep it stable
    for i in range(n - 1, -1, -1):
        v = arr[i]
        ans[cntArr[v] - 1] = v
        cntArr[v] -= 1

    return ans

def performance():
    test_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
    repeats = 3

    times = []

    header = "n     " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "   avg(ms)"
    print(header)
    print("-" * len(header))

    for n in test_sizes:
        run_times = []

        for _ in range(repeats):
            # IMPORTANT: keep value range reasonable for counting sort
            arr = [random.randint(0, 1000) for _ in range(n)]

            start = time.perf_counter()
            count_sort(arr)
            end = time.perf_counter()

            run_times.append((end - start) * 1000)

        avg_time = sum(run_times) / repeats

        row = f"{n:<5} " + "  ".join(f"{t:>10.3f}" for t in run_times) + f"  {avg_time:>10.3f}"
        print(row)

        times.append(avg_time)

    # 🔹 Time graph only
    plt.figure(figsize=(6, 5))
    plt.plot(test_sizes, times, marker="o", linestyle="-", label="Counting Sort Time")
    plt.title("Counting Sort Execution Time")
    plt.xlabel("Array Size (n)")
    plt.ylabel("Time (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    performance()
