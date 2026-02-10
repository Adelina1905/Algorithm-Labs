import time
import matplotlib.pyplot as plt

MOD = 1000000007

def FastDoubling(n, res):
    if n == 0:
        res[0] = 0
        res[1] = 1
        return

    FastDoubling(n // 2, res)

    a = res[0]  # F(k)
    b = res[1]  # F(k+1)

    c = (2 * b - a) % MOD              # (2F(k+1) - F(k)) mod
    c = (a * c) % MOD                  # F(2k)
    d = (a * a + b * b) % MOD          # F(2k+1)

    if n % 2 == 0:
        res[0] = c
        res[1] = d
    else:
        res[0] = d
        res[1] = (c + d) % MOD         # IMPORTANT: mod here

def fib_fast_doubling_mod(n: int) -> int:
    res = [0, 0]
    FastDoubling(n, res)
    return res[0]

def performance_fast_doubling():
    # fast doubling is O(log n), so use BIG n
    test_numbers = [0, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    repeats = 10

    times_ms = []

    header = "n           F(n) mod 1e9+7   " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print(header)
    print("-" * len(header))

    for n in test_numbers:
        execs = []
        value = None

        for _ in range(repeats):
            start = time.perf_counter()
            value = fib_fast_doubling_mod(n)
            end = time.perf_counter()
            execs.append((end - start) * 1000)

        avg = sum(execs) / repeats
        times_ms.append(avg)

        print(
            f"{n:<12} {value:<16} "
            + "  ".join(f"{t:>10.6f}" for t in execs)
            + f"  {avg:>10.6f}"
        )

    plt.figure(figsize=(8, 4))
    plt.plot(test_numbers, times_ms, marker="o", linestyle="-", label="Fast Doubling (mod)")
    plt.title("Fast Doubling Fibonacci Execution Time (Average of runs)")
    plt.xlabel("Fibonacci Number Index (n)")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance_fast_doubling()
