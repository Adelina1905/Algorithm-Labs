import time
import matplotlib.pyplot as plt
import random
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

def nthFibonacci(n):
    if n <= 1:
        return n

    # Initialize the transformation matrix
    mat1 = [[1, 1], [1, 0]]

    matrixPower(mat1, n - 1)

    # The result is in the top-left cell of the matrix
    return mat1[0][0]


def performance():
    # use the same values as in your plot (edit if needed)
    test_numbers = [0, 500, 1000, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000]

    repeats = 5          # average makes it smoother; set to 1 for spikier
    warmup_runs = 1      # warmup helps reduce first-run weird spikes
    shuffle_order = False  # True if you want to reduce “always increasing” bias

    xs = test_numbers[:]
    if shuffle_order:
        random.shuffle(xs)

    # warmup
    for _ in range(warmup_runs):
        nthFibonacci(1000)

    times_ms = []

    header = "n       " + "  ".join(f"run{i+1}(ms)" for i in range(repeats)) + "  avg(ms)"
    print(header)
    print("-" * len(header))

    for n in xs:
        execs = []

        for _ in range(repeats):
            start = time.perf_counter()
            nthFibonacci(n)
            end = time.perf_counter()
            execs.append((end - start) * 1000)

        avg = sum(execs) / repeats
        print(f"{n:<7} " + "  ".join(f"{t:>10.3f}" for t in execs) + f"  {avg:>10.3f}")
        times_ms.append(avg)

    # plot in the original x-order
    if shuffle_order:
        paired = sorted(zip(xs, times_ms), key=lambda p: p[0])
        xs, times_ms = zip(*paired)

    plt.figure(figsize=(8, 4))
    plt.plot(xs, times_ms, marker="o", linestyle="-", label="Matrix Power")
    plt.title("Matrix Power Fibonacci Execution Time (Average of runs)")
    plt.xlabel("Fibonacci Number Index (n)")
    plt.ylabel("Execution Time (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    performance()