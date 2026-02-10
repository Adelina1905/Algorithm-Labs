import time
import matplotlib.pyplot as plt

def nthFibonacci(n):
  
    if n <= 1:
        return n

    dp = [0] * (n + 1)

    dp[0], dp[1] = 0, 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

def performance():
    test_numbers = [1000, 5000, 10000, 20000, 50000, 100000]
    repeats = 5

    dp_times = []

    header = "n      " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print(header)
    print("-" * len(header))

    for n in test_numbers:
        execs = []

        for _ in range(repeats):
            start = time.perf_counter()
            nthFibonacci(n)
            end = time.perf_counter()
            execs.append((end - start) * 1000)

        avg_time = sum(execs) / repeats
        print(f"{n:<6} " + "  ".join(f"{t:>10.3f}" for t in execs) + f"  {avg_time:>10.3f}")
        dp_times.append(avg_time)

    plt.figure(figsize=(7, 4))
    plt.plot(test_numbers, dp_times, marker="o", linestyle="-", label="DP (Bottom-Up)")
    plt.title("DP Execution Time (Average of runs)")
    plt.xlabel("Fibonacci Number Index (n)")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance()