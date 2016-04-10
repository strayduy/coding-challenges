#!python2.7

# Standard libs
import argparse
import math

# Config
PRIMES_FILE = 'primes.txt'

# Constants
DIGITS = '0123456789'
FIRST_PRIMES = set()

def generate_jamcoins(length):
    limit = 2**length

    for i in xrange(3, limit):
        # Step 1: Determine whether i is a jamcoin
        binary = '{number:0{width}b}'.format(number=i, width=length)

        if binary[0] != '1' or binary[-1] != '1':
            continue

        is_jamcoin = True

        for base in xrange(2, 11):
            n = convertToBase10(binary, base)

            if isPrime(n):
                is_jamcoin = False
                break

        # If it's not a jamcoin, move on to the next number
        if not is_jamcoin:
            continue

        # Step 2: If i is a jamcoin, find a divisor in each base
        divisors = []

        for base in xrange(2, 11):
            n = convertToBase10(binary, base)
            for divisor in divisorGenerator(n):
                if divisor == 1 or divisor == n:
                    continue
                divisors.append(str(divisor))
                break

        if not divisors:
            continue

        yield binary, divisors

def isPrime(n):
    # Shortcut: Check whether n is one of the smaller primes
    if n in FIRST_PRIMES:
        return True

    # Shortcut: Check whether n is divisible by the smaller primes
    for prime in FIRST_PRIMES:
        if n % prime == 0:
            return False

    # Iterate through the odd numbers up to sqrt(n)
    # If n is divisible by any of those, it's a composite number
    for i in xrange(3, int(math.ceil(math.sqrt(n))) + 1, 2):
        if n % i == 0:
            return False

    # If we've reached this point, then the number must be prime
    return True

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
    for i in xrange(1, int(math.sqrt(n) + 1)):
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

    with open(PRIMES_FILE, 'r') as f:
        for line in f:
            prime = int(line.strip())
            FIRST_PRIMES.add(prime)

    for i, (jamcoin, divisors) in enumerate(generate_jamcoins(args.jamcoin_length), start=1):
        print jamcoin, ' '.join(divisors)

        if i >= args.limit:
            break

if __name__ == "__main__":
    main()

