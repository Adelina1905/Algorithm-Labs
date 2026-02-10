import math
import time
import matplotlib.pyplot as plt
def fibonacci(n):
    
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2

    return round((math.pow(phi, n) - math.pow(psi, n)) / math.sqrt(5))


def performance_binet():
    # you can change these, but keep in mind float precision breaks for large n
    test_numbers = [0, 5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
    repeats = 5

    times_ms = []
    values = []

    header = "n       F(n)                 " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print(header)
    print("-" * len(header))

    for n in test_numbers:
        execs = []

        for _ in range(repeats):
            start = time.perf_counter()
            val = fibonacci(n)
            end = time.perf_counter()
            execs.append((end - start) * 1000)

        avg = sum(execs) / repeats
        values.append(val)
        times_ms.append(avg)

        print(
            f"{n:<7} {val:<20} "
            + "  ".join(f"{t:>10.6f}" for t in execs)
            + f"  {avg:>10.6f}"
        )

    # plot time
    plt.figure(figsize=(8, 4))
    plt.plot(test_numbers, times_ms, marker="o", linestyle="-", label="Binet / Golden Ratio")
    plt.title("Binet Fibonacci Execution Time (Average of runs)")
    plt.xlabel("Fibonacci Number Index (n)")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    performance_binet()