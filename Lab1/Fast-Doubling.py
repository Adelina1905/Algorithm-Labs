import time
import matplotlib.pyplot as plt
# (Public) Returns F(n).
def fibonacci(n):
	if n < 0:
		raise ValueError("Negative arguments not implemented")
	return _fib(n)[0]


# (Private) Returns the tuple (F(n), F(n+1)).
def _fib(n):
	if n == 0:
		return (0, 1)
	else:
		a, b = _fib(n // 2)
		c = a * (b * 2 - a)
		d = a * a + b * b
		if n % 2 == 0:
			return (c, d)
		else:
			return (d, c + d)

def performance_fast_doubling():
    # fast doubling is O(log n), so use BIG n
    test_numbers = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
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
            value = fibonacci(n)
            end = time.perf_counter()
            execs.append((end - start) * 1000)

        avg = sum(execs) / repeats
        times_ms.append(avg)

        print(
            f"{n:<12} "
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
