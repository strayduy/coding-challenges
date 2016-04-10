#!python2.7

# Standard libs
import argparse
import itertools
import math
import sys

# Config
PRIMES_FILE = 'primes.txt' # Text file containing first 50k primes

# Constants
DIGITS = '0123456789'
FIRST_PRIMES = set()
LARGEST_KNOWN_PRIME = 5

def generate_jamcoins(length):
    for i in itertools.count(0):
        # Step 1: Construct potential jamcoin
        binary = '{number:0{width}b}'.format(number=i, width=length - 2)
        binary = '1' + binary + '1'

        if len(binary) != length:
            continue

        # Step 2: Look for divisors for each base
        divisors = []

        for base in xrange(2, 11):
            n = convertToBase10(binary, base)
            for divisor in divisorGenerator(n):
                if divisor == 1 or divisor == n:
                    continue
                divisors.append(str(divisor))
                break

        # If we find all nine divisors, we're good to go
        if len(divisors) != 9:
            continue

        yield binary, divisors

# http://codereview.stackexchange.com/q/78514
def convertToBase10(n, base):
    number = []

    for i in n:
        number.append(int(i))

    number = number[::-1]
    for i in range(len(number)):
        number[i] = number[i] * (base ** i)

    return sum(number)

# http://stackoverflow.com/a/171779
def divisorGenerator(n):
    large_divisors = []
    for i in itertools.count(1):
        # Give up looking for divisors once we reach numbers larger than our
        # largest known prime. This will result in false negatives, but we'll
        # avoid spending lots of time looking for "difficult" jamcoins.
        if i >= int(math.sqrt(n) + 1) or i > LARGEST_KNOWN_PRIME:
            break
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('jamcoin_length', type=int)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()

    global LARGEST_KNOWN_PRIME
    with open(PRIMES_FILE, 'r') as f:
        for line in f:
            prime = int(line.strip())
            FIRST_PRIMES.add(prime)
            LARGEST_KNOWN_PRIME = prime

    for i, (jamcoin, divisors) in enumerate(generate_jamcoins(args.jamcoin_length), start=1):
        print jamcoin, ' '.join(divisors)
        sys.stdout.flush()

        if i >= args.limit:
            break

if __name__ == "__main__":
    main()

