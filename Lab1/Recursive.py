import time
import matplotlib.pyplot as plt

def nth_fibonacci(n):
    if n <= 1:
        return n
    
    return nth_fibonacci(n-1) + nth_fibonacci(n-2)

def performance():
    test_numbers = [5, 10, 15, 20, 25, 30]
    repeats = 3
    naive_times = []
    naive_calls = []
    memo_times = []

    header = "n  " + "  ".join(f"run{i + 1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print(header)
    print("-" * len(header))

    for number in test_numbers:
        naive_execs = []
        memo_execs = []
        calls_for_n = 0

        for _ in range(repeats):
            global CALL_COUNT
            CALL_COUNT = 0
            start = time.perf_counter()
            nth_fibonacci(number)
            end = time.perf_counter()
            naive_execs.append((end - start) * 1000)
            calls_for_n = CALL_COUNT

        avg_time = sum(naive_execs) / repeats
        row = f"{number:<2} " + "  ".join(f"{t:>8.3f}" for t in naive_execs) + f"  {avg_time:>8.3f}"
        print(row)

        naive_times.append(avg_time)
        naive_calls.append(calls_for_n)
        memo_times.append(sum(memo_execs) / repeats)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(test_numbers, naive_times, marker="o", linestyle="-", label="Naïve Recursion")
    axes[0].set_title("Execution Time (Average of runs)")
    axes[0].set_xlabel("Fibonacci Number Index")
    axes[0].set_ylabel("Execution Time (ms)")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(test_numbers, naive_calls, marker="o", linestyle="-", label="Naïve Recursion Calls")
    axes[1].set_title("Naïve Recursion Call Count")
    axes[1].set_xlabel("Fibonacci Number Index")
    axes[1].set_ylabel("Function Calls")
    axes[1].grid(True)
    axes[1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance()