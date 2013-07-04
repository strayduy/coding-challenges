#!/usr/bin/env python2.7

# Standard libs
import itertools
import math
import sys

# Constants
USAGE = "python %s INPUT_FILE" % (sys.argv[0])
PRECOMPUTED_UPPER_BOUND = 10**14

def main(argv):
    if len(argv) != 2:
        raise Exception("Invalid arguments! Usage: %s" % (USAGE))

    input_filename = argv[1]

    # Pre-compute all fair-and-square numbers up to an absolute upper bound
    precomputed_fair_and_squares = get_fair_and_square_numbers(
                                       PRECOMPUTED_UPPER_BOUND)
    #print precomputed_fair_and_squares

    with open(input_filename, "r") as input_file:
        # Read in the number of test cases
        try:
            num_test_cases = int(input_file.readline().strip())
        except:
            raise Exception("Invalid input file")

        # Count the number of fair-and-square numbers for each test case
        for test_case_number in range(1, num_test_cases + 1):
            lower, upper = map(int, input_file.readline().strip().split())
            fair_and_square_count = count_fair_and_square_numbers(lower,
                                        upper, precomputed_fair_and_squares)
            print "Case #%d: %s" % (test_case_number, fair_and_square_count)

def count_fair_and_square_numbers(inclusive_lower_bound,
                                  inclusive_upper_bound,
                                  precomputed_fair_and_squares):
    def bounds(x):
        return x >= inclusive_lower_bound and x <= inclusive_upper_bound

    return len(filter(bounds, precomputed_fair_and_squares))

# Retrieve the set of fair-and-square numbers up to the upper bound
def get_fair_and_square_numbers(inclusive_upper_bound):
    fair_and_square_numbers = []

    for fair_and_square in fast_fair_and_squares():
        if fair_and_square > inclusive_upper_bound:
            break
        fair_and_square_numbers.append(fair_and_square)

    return fair_and_square_numbers

'''
The square roots of the first 39 fair and square numbers:
1
2
3
11
22
101
111
121
202
212
1001
1111
2002
10001
10101
10201
11011
11111
11211
20002
20102
100001
101101
110011
111111
200002
1000001
1001001
1002001
1010101
1011101
1012101
1100011
1101011
1102011
1110111
1111111
2000002
2001002
10000001

If you look at the values that are more than one digit, a pattern emerges!
All of the digits in the fair and square roots are either 0, 1, or 2. Also,
for each order of magnitude, there are only one or two fair and square roots
that start with the digit 2. Given this, we can try to construct palindromes
from just these three digits, instead of iterating through lots and lots of
numbers.
'''

# Generator for fair and square numbers that's quicker for larger numbers
def fast_fair_and_squares():
    yield 1
    yield 4
    yield 9

    #digit_set = ['0', '1', '2']
    digit_set = ['0', '1']
    num_digits = 2

    for palindrome in palindromes(digit_set):
        # Stick the palindrome between '1' digits
        palindrome = '1' + palindrome + '1'

        palindrome = int(palindrome)
        palindrome_squared = palindrome**2
        if is_palindrome(palindrome_squared):
            print palindrome
            yield palindrome_squared

# Generator for palindromes constructed from a given set of characters
def palindromes(char_set, min_palindrome_len=1):
    palindrome_len = min_palindrome_len

    while True:
        for chars in itertools.product(char_set, repeat=(palindrome_len / 2)):
            # Even number of characters
            if palindrome_len % 2 == 0:
                palindrome = ''.join(itertools.chain(chars, reversed(chars)))
                yield palindrome
            # Odd number of characters
            else:
                for middle_char in char_set:
                    palindrome = ''.join(itertools.chain(chars,
                                                         middle_char,
                                                         reversed(chars)))
                    yield palindrome

        palindrome_len += 1

# Generator for fair and square numbers
def fair_and_squares(start=1):
    i = int(math.ceil(math.sqrt(start)))

    while True:
        i_squared = i**2
        if is_palindrome(i) and is_palindrome(i_squared):
            yield i_squared
        i += 1

def is_palindrome(i):
    s = str(i)
    return s == ''.join(reversed(s))

if __name__ == "__main__":
    main(sys.argv)
