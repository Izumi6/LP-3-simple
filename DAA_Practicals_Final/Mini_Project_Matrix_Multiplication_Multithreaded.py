import random
import threading
import time


def normal_multiply(first, second):
    n = len(first)
    result = [[0 for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += first[i][k] * second[k][j]

    return result


def multiply_row(first, second, result, row):
    n = len(first)

    for j in range(n):
        for k in range(n):
            result[row][j] += first[row][k] * second[k][j]


def threaded_multiply(first, second):
    n = len(first)
    result = [[0 for j in range(n)] for i in range(n)]
    threads = []

    for i in range(n):
        thread = threading.Thread(target=multiply_row, args=(first, second, result, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result


def print_matrix(matrix):
    for row in matrix:
        print(row)


def main():
    n = int(input("Enter size of square matrices (recommended: 100 to 200): "))

    if n <= 0:
        print("Matrix size must be greater than zero.")
        return

    random.seed(42)
    first = [[random.randint(1, 9) for j in range(n)] for i in range(n)]
    second = [[random.randint(1, 9) for j in range(n)] for i in range(n)]

    start = time.perf_counter()
    normal_result = normal_multiply(first, second)
    normal_time = time.perf_counter() - start

    start = time.perf_counter()
    threaded_result = threaded_multiply(first, second)
    threaded_time = time.perf_counter() - start

    print("\nNormal Multiplication:")
    print("Execution time:", round(normal_time, 6), "seconds")

    print("\nMultithreaded Multiplication (one thread per row):")
    print("Execution time:", round(threaded_time, 6), "seconds")

    if n <= 5:
        print("\nResult Matrix:")
        print_matrix(normal_result)

    print("\nBoth results are same:", normal_result == threaded_result)

    if threaded_time > 0:
        speedup = normal_time / threaded_time
        print("Speed-up (normal time / threaded time):", round(speedup, 2), "x")

        if speedup > 1:
            print("The threaded method was faster for this run.")
        else:
            print("The normal method was faster for this run.")

    print("\nTime Complexity of both methods: O(n^3)")
    print("Note: Python threads may not speed up CPU-bound work because of the GIL and thread overhead.")


if __name__ == "__main__":
    main()


# SAMPLE OUTPUT:
# Enter size of square matrices (recommended: 100 to 200): 2
#
# Normal Multiplication:
# Execution time: varies seconds
#
# Multithreaded Multiplication (one thread per row):
# Execution time: varies seconds
#
# Result Matrix:
# [10, 15]
# [28, 51]
#
# Both results are same: True
# Speed-up (normal time / threaded time): varies x
# The normal method was faster for this run.
#
# Time Complexity of both methods: O(n^3)
# Note: Python threads may not speed up CPU-bound work because of the GIL and thread overhead.
