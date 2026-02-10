import time
import math
import matplotlib.pyplot as plt

def fibonacci_naive(n):
    if n <= 1:
        return n
    
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)


def multiply(mat1, mat2):
    x = mat1[0][0] * mat2[0][0] + mat1[0][1] * mat2[1][0]
    y = mat1[0][0] * mat2[0][1] + mat1[0][1] * mat2[1][1]
    z = mat1[1][0] * mat2[0][0] + mat1[1][1] * mat2[1][0]
    w = mat1[1][0] * mat2[0][1] + mat1[1][1] * mat2[1][1]

    # Update matrix mat1 with the result
    mat1[0][0], mat1[0][1] = x, y
    mat1[1][0], mat1[1][1] = z, w

def matrixPower(mat1, n):
  
    # Base case for recursion
    if n == 0 or n == 1:
        return

    mat2 = [[1, 1], [1, 0]]

    matrixPower(mat1, n // 2)

    multiply(mat1, mat1)

    # If n is odd, multiply by the helper matrix mat2
    if n % 2 != 0:
        multiply(mat1, mat2)

def fib_matrix(n):
    if n <= 1:
        return n

    # Initialize the transformation matrix
    mat1 = [[1, 1], [1, 0]]

    matrixPower(mat1, n - 1)

    # The result is in the top-left cell of the matrix
    return mat1[0][0]


def fibonacci(n):
    
    phi = (1 + math.sqrt(5)) / 2
    psi = (1 - math.sqrt(5)) / 2

    return round((math.pow(phi, n) - math.pow(psi, n)) / math.sqrt(5))

def nthFibonacci(n):
  
    if n <= 1:
        return n

    dp = [0] * (n + 1)

    dp[0], dp[1] = 0, 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]



def fib_fast_doubling_mod(n):
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

def time_ms(func, n, repeats=5):
    """Return average time in ms over repeats."""
    total = 0.0
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(n)
        t1 = time.perf_counter()
        total += (t1 - t0) * 1000.0
    return total / repeats


def compare_all_methods_one_graph():
    # Use the SAME n list for all methods, but keep it safe for naive recursion.
    # If you push naive to 45+, it may take a long time.
    ns = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]

    repeats_fast = 50    # fast methods are super quick → more repeats = smoother
    repeats_slow = 3     # naive recursion is slow → fewer repeats

    series = {}

    # --- Naive recursion ---
    series["Naive Recursion"] = [
        time_ms(fibonacci_naive, n, repeats=repeats_slow) for n in ns
    ]

    # --- DP bottom-up ---
    series["DP (Bottom-Up)"] = [
        time_ms(nthFibonacci, n, repeats=repeats_fast) for n in ns
    ]

    # --- Matrix exponentiation ---
    series["Matrix Power"] = [
        time_ms(fib_matrix, n, repeats=repeats_fast) for n in ns
    ]

    # --- Binet / golden ratio ---
    series["Binet (Golden Ratio)"] = [
        time_ms(fibonacci, n, repeats=repeats_fast) for n in ns
    ]

    # --- Fast doubling (mod) ---
    series["Fast Doubling (mod)"] = [
        time_ms(fib_fast_doubling_mod, n, repeats=repeats_fast) for n in ns
    ]

    # ---------------- Plot ----------------
    plt.figure(figsize=(9, 5))
    for name, times in series.items():
        plt.plot(ns, times, marker="o", linestyle="-", label=name)

    plt.title("Fibonacci Methods: Execution Time Comparison")
    plt.xlabel("Fibonacci index (n)")
    plt.ylabel("Average execution time (ms)")
    plt.grid(True)
    plt.legend()

    # Big differences are hard to see on a normal scale → log scale helps a LOT
    plt.yscale("log")

    plt.tight_layout()
    plt.show()


# Run it
if __name__ == "__main__":
    compare_all_methods_one_graph()