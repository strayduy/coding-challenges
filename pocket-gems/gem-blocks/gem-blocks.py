#!/usr/bin/env python2.7

"""
Solving the problem in one dimension
------------------------------------

Let's assume that all walls are of height 1.

For a wall of width 2, the possible walls are:
    _ _
1. |_|_|
    _ _
2. |_ _|

Width 3:
    _ _ _
1. |_|_|_|
    _ _ _
2. |_ _|_|
    _ _ _
3. |_|_ _|

Width 4:
    _ _ _ _
1. |_|_|_|_|
    _ _ _ _
2. |_ _|_|_|
    _ _ _ _
3. |_|_ _|_|
    _ _ _ _
4. |_ _|_|_|
    _ _ _ _
5. |_ _|_ _|

Width 5:
    _ _ _ _ _
1. |_|_|_|_|_|
    _ _ _ _ _
2. |_ _|_|_|_|
    _ _ _ _ _
3. |_|_ _|_|_|
    _ _ _ _ _
4. |_|_|_ _|_|
    _ _ _ _ _
5. |_|_|_|_ _|
    _ _ _ _ _
6. |_ _|_ _|_|
    _ _ _ _ _
7. |_ _|_|_ _|
    _ _ _ _ _
8. |_|_ _|_ _|

Hey, looks like a Fibonacci sequence. If we go with this conclusion, then for a
wall of width W and height 1, there are Fib(W+1) possible configurations, where
Fib(N) is the Nth Fibonacci number.

Fib(0) = 0
Fib(1) = 1
Fib(2) = 1
Fib(3) = 2
...
Fib(N) = Fib(N-1) + Fib(N-2)


Solving the problem with only 1x1 and 2x1 blocks
------------------------------------------------

Now, let's consider walls of height > 1, but we'll pretend that 1x2 blocks don't
exist.

This then becomes a combinatorial problem. If we have H rows of width W, and
there are P possible configurations for each row, then the number of wall
configurations is P^H.

We previously concluded that P = Fib(W+1).

So for this simplified case, the number of wall configurations is Fib(W+1)^H.


Solving the actual problem
--------------------------


"""

# Standard libs
import sys

# Constants
USAGE = "python %s INPUT_FILE" % (sys.argv[0])
WIDTH_BASE = 2
RESULT_MODULO = 1000000007

def main(argv):
    if len(argv) != 2:
        print "Usage: %s" % (USAGE)
        raise Exception("Invalid arguments")

    input_filename = argv[1]

    # Loop through each test case in the input file
    with open(input_filename, "r") as input_file:
        # Discard the first line, which contains the number of test cases
        input_file.readline()

        # Process the test cases in the rest of the lines
        for line in input_file:
            width_exponent, height = map(int, line.strip().split())
            width = WIDTH_BASE ** width_exponent
            num_wall_configurations = count_wall_configurations(width, height)
            print "%d" % (num_wall_configurations % RESULT_MODULO)

# Compute the number of possible wall configurations for a wall of the given
# width and height, using blocks of size 1x1, 2x1, and 1x2
def count_wall_configurations(width, height):
    return fib(width + 1) ** height

# A Fibonacci algorithm that's way more efficient than anything I could come
# up with on my own.
# Pulled from here:
# http://en.literateprograms.org/Fibonacci_numbers_%28Python%29
fibs = {0: 0, 1: 1}
def fib(n):
    if n in fibs: return fibs[n]
    if n % 2 == 0:
        fibs[n] = ((2 * fib((n / 2) - 1)) + fib(n / 2)) * fib(n / 2)
        return fibs[n]
    else:
        fibs[n] = (fib((n - 1) / 2) ** 2) + (fib((n+1) / 2) ** 2)
        return fibs[n]

if __name__ == "__main__":
    main(sys.argv)
