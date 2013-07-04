#!/usr/bin/env python2.7

# Standard libs
from decimal import Decimal, getcontext
import math
import sys

# Constants
USAGE = "python %s INPUT_FILE" % (sys.argv[0])

def main(argv):
    if len(argv) != 2:
        raise Exception("Invalid arguments! Usage: %s" % (USAGE))

    input_filename = argv[1]

    with open(input_filename, "r") as input_file:
        # Read in the number of test cases
        try:
            num_test_cases = int(input_file.readline().strip())
        except:
            raise Exception("Invalid input file")

        # Determine the maximum number of black rings around the bullseye for
        # each test case
        for test_case_number in range(1, num_test_cases + 1):
            initial_radius, paint_volume = map(int, input_file.readline().strip().split())
            max_black_rings = get_max_black_rings(initial_radius, paint_volume)
            print "Case #%d: %d" % (test_case_number, max_black_rings)

def get_max_black_rings(initial_radius, paint_volume):
    # The amount of paint that we need to use for each string is an arithmetic
    # sequence. For example, with an initial radius of 1, the amount of paint
    # required for each black ring is:
    # 3, 7, 11, 15, ...

    # The sum of an arithmetic sequence can be computed via:
    # Sn = (n * (a1 + an)) / 2
    # n:  number of terms in the sequence
    # a1: first term in the sequence
    # an: nth term in the sequence

    # The nth term in an arithmetic sequence can be computed via:
    # an = a1 + (n - 1) * d
    # d: common difference

    # If we combine the two formulae, we can turn it into a quadratic equation
    # and solve for n.
    # 0 = d * n^2 + (2a1 - d) * n - 2 * Sn
    # n = ((d - 2a1) +- sqrt((d - 2a1)^2 - 4 * d * (2 * Sn)) / (2 * d))

    # Source:
    # http://www.regentsprep.org/Regents/math/algtrig/ATP2/ArithSeq.htm

    paint_volume_for_first_ring = (initial_radius + 1)**2 - initial_radius**2

    # Ugh, having issues with floating point precision, so let's crank it up
    getcontext().prec = 1000

    # Have to convert everything to Decimal so we preserve floating point
    # precision
    a = Decimal(4)
    b = Decimal(2 * (paint_volume_for_first_ring) - 4)
    c = Decimal(-2 * paint_volume)
    n1 = (Decimal(-1) * b + Decimal(b**2 - 4 * a * c).sqrt()) / (Decimal(2) * a)
    n2 = (Decimal(-1) * b - Decimal(b**2 - 4 * a * c).sqrt()) / (Decimal(2) * a)

    # Round down to the nearest integer
    n1 = math.floor(n1)
    n2 = math.floor(n2)

    return max([n1, n2])

if __name__ == "__main__":
    main(sys.argv)
