#!python2.7

# Standard libs
import itertools
import math
import Queue
import random
import sys
import threading
import time
import unittest

# Constants
RAND_INT_LOWER_BOUND = 1          # Inclusive
RAND_INT_UPPER_BOUND = sys.maxint # Inclusive
FIRST_PRIMES = [2, 3, 5, 7, 11]
FIRST_100_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

# Pseudo-abstract base class for a lazy stream
class Stream(object):
    def __init__(self, stream_generator=None):
        # Subclasses are expected to bind a generator function to stream_generator
        self.stream_generator = stream_generator

    # Return the next element of the stream, if any
    # Otherwise, return None
    def popNext(self):
        if not self.stream_generator:
            raise NotImplementedError("Stream class must implement stream_generator generator object")

        try:
            next_element = self.stream_generator.next()
        except StopIteration:
            next_element = None

        return next_element

    # Return the next num elements of the stream, if any
    # Otherwise, return None
    def popN(self, num, multiThread=False):
        if multiThread:
            return self._popN_multiThread(num)
        return self._popN_singleThread(num)

    def _popN_singleThread(self, num):
        values_to_return = [value for value in itertools.islice(self.stream_generator, num)]

        # If we get an empty list back,
        # return None instead of an empty list to be consistent with the popNext method
        if not values_to_return:
            return None

        # Otherwise, bundle the values into a tuple and return
        return tuple(values_to_return)

    def _popN_multiThread(self, num, num_threads=10):
        work_queue = Queue.Queue()
        generator_lock = threading.Lock()
        output_values = []

        # Start the pop threads
        pop_threads = []
        for i in xrange(num_threads):
            pop_threads.append(PopThread(self, work_queue, generator_lock, output_values))
            pop_threads[i].daemon = True
            pop_threads[i].start()

        # Populate the work queue
        for i in xrange(num):
            work_queue.put(i)

        # Wait for the queue to empty
        work_queue.join()

        # Aggregate all the returned values
        values_to_return = [v[1] for v in sorted(output_values, key=lambda v: v[0]) if v[1]]
        return tuple(values_to_return)

    # Returns a stream where fn has been applied to each element
    @classmethod
    def map(cls, fn, stream):
        assert(hasattr(fn, '__call__'))
        assert(isinstance(stream, Stream))

        def generateMappedStream(fn, stream):
            elements = stream.stream_generator
            for element in elements:
                yield fn(element)

        return Stream(generateMappedStream(fn, stream))

    # Returns a stream containing only the elements of the stream for which fn returns True
    @classmethod
    def filter(cls, fn, stream):
        assert(hasattr(fn, '__call__'))
        assert(isinstance(stream, Stream))

        def generateFilteredStream(fn, stream):
            elements = stream.stream_generator
            for element in elements:
                if fn(element):
                    yield element

        return Stream(generateFilteredStream(fn, stream))

    # Applies a given binary function pairwise to the elements of two given streams
    @classmethod
    def zipWith(cls, fn, streamA, streamB):
        assert(hasattr(fn, '__call__'))
        assert(isinstance(streamA, Stream))
        assert(isinstance(streamB, Stream))

        def generateZippedStream(fn, streamA, streamB):
            elementsA = streamA.stream_generator
            elementsB = streamB.stream_generator
            for a, b in itertools.izip(elementsA, elementsB):
                yield fn(a, b)

        return Stream(generateZippedStream(fn, streamA, streamB))

    # Where fn(x, y) is a function to perform a reduction across the stream,
    # returns a stream where the nth element is the result of combining the first n elements of the input stream using fn
    @classmethod
    def prefixReduce(cls, fn, stream, init):
        assert(hasattr(fn, '__call__'))
        assert(isinstance(stream, Stream))
        
        def generatePrefixReducedStream(fn, stream, init):
            reduction = init
            elements = stream.stream_generator
            for element in elements:
                yield element
                reduction = fn(reduction, element)

            yield reduction

        return Stream(generatePrefixReducedStream(fn, stream, init))

# Create a thread to perform each pop
class PopThread(threading.Thread):
    def __init__(self, stream, work_queue, generator_lock, output_values):
        threading.Thread.__init__(self)
        self.stream = stream
        self.work_queue = work_queue
        self.generator_lock = generator_lock
        self.output_values = output_values

    def run(self):
        while True:
            with self.generator_lock:
                self.index = self.work_queue.get()
                self.value = self.stream.popNext()
                self.output_values.append((self.index, self.value))
                self.work_queue.task_done()

# Stream of unique random positive integers
# This implementation is O(n) in space and approaches O(n) in time as you pop off more values
class Randoms(Stream):
    def __init__(self, lower_bound=RAND_INT_LOWER_BOUND, upper_bound=RAND_INT_UPPER_BOUND):
        # Sanity check
        assert(lower_bound > 0)
        assert(lower_bound <= upper_bound)

        # Stream generator function
        def generateRandoms(lower_bound, upper_bound):
            used_values = set()

            while len(used_values) < upper_bound - lower_bound + 1:
                # Pick a random integer within the bounds
                next_rand_int = random.randint(lower_bound, upper_bound)

                # If we've already used the number we just picked,
                # increment it until we find an unused value
                if next_rand_int in used_values:
                    while next_rand_int in used_values and next_rand_int <= upper_bound:
                        next_rand_int += 1

                # If we've incremented past the upper bound,
                # that means we didn't find an unused value in the upper part of the range
                if next_rand_int > upper_bound:
                    # Wrap back around to the lower end of the range and try again
                    next_rand_int = lower_bound
                    while next_rand_int in used_values and next_rand_int <= upper_bound:
                        next_rand_int += 1

                # Record this value as "used" and yield
                used_values.add(next_rand_int)
                yield next_rand_int

        self.stream_generator = generateRandoms(lower_bound, upper_bound)

# Stream of ordered prime numbers
class Primes(Stream):
    def __init__(self):
        # Stream generator function
        def generatePrimes():
            # Because 2 is the weird even prime
            yield 2

            # Now, let's start with the first odd prime
            i = 3

            # Iterate through odd numbers, checking whether they're prime
            while i <= sys.maxint:
                # Yield the prime numbers
                if isPrime(i):
                    yield i
                i += 2

        self.stream_generator = generatePrimes()

# Stream of prime factors for a given integer
class PrimeFactors(Stream):
    def __init__(self, int_to_be_factored):
        # Sanity check
        assert(int_to_be_factored > 0)

        # Stream generator function
        def generatePrimeFactors(n):
            primes = Primes().stream_generator

            # Iterate through the prime numbers up to n
            for prime in primes:
                if prime > n:
                    break
                # Yield the primes that are factors of n
                if n % prime == 0:
                    yield prime

        self.stream_generator = generatePrimeFactors(int_to_be_factored)

# Return True if n is prime
# Return False otherwise
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

def multiplyBy2(x):
    return x * 2

def isDivisibleBy2(x):
    return x % 2 == 0

def add(x, y):
    return x + y

class StreamUnitTests(unittest.TestCase):
    def test_isPrime(self):
        for prime in FIRST_100_PRIMES:
            self.assertTrue(isPrime(prime))

        for composite in [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]:
            self.assertFalse(isPrime(composite))

    def test_Randoms(self):
        random_stream = Randoms(1, 10)
        sorted_values = sorted([random_stream.popNext() for _ in xrange(1, 11)])
        self.assertEquals(sorted_values, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEquals(random_stream.popNext(), None)

        random_stream = Randoms(1, 10)
        sorted_values = sorted(list(random_stream.popN(20)))
        self.assertEquals(sorted_values, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEquals(random_stream.popNext(), None)

    def test_Primes(self):
        prime_stream = Primes()
        primes = [prime_stream.popNext() for _ in xrange(100)]
        self.assertEquals(primes, FIRST_100_PRIMES)

        prime_stream = Primes()
        primes = list(prime_stream.popN(100))
        self.assertEquals(primes, FIRST_100_PRIMES)

    def test_PrimeFactors(self):
        for n, expected_output in zip([4, 5, 6, 78, 910], [(2,), (5,), (2, 3), (2, 3, 13), (2, 5, 7, 13)]):
            prime_factors_stream = PrimeFactors(n)
            prime_factors = prime_factors_stream.popN(20)
            self.assertEquals(prime_factors, expected_output)

    def test_map(self):
        prime_factors_stream = PrimeFactors(910)
        mapped_stream = Stream.map(multiplyBy2, prime_factors_stream)
        doubled_prime_factors = mapped_stream.popN(20)
        self.assertEquals(doubled_prime_factors, (4, 10, 14, 26))

    def test_filter(self):
        random_stream = Randoms()
        filtered_stream = Stream.filter(isDivisibleBy2, random_stream)
        for _ in xrange(100):
            self.assertTrue(isDivisibleBy2(filtered_stream.popNext()))

    def test_zipWith(self):
        prime_streamA = Primes()
        prime_streamB = Primes()
        prime_streamB.popNext()

        zippedStream = Stream.zipWith(add, prime_streamA, prime_streamB)
        pairwise_sums = [zippedStream.popNext() for _ in xrange(10)]

        # A:   2, 3,  5,  7, 11, 13, 17, 19, 23, 29
        # B:   3, 5,  7, 11, 13, 17, 19, 23, 29, 31
        # Sum: 5, 8, 12, 18, 24, 30, 36, 42, 52, 60

        self.assertEquals(pairwise_sums, [5, 8, 12, 18, 24, 30, 36, 42, 52, 60])

    def test_prefixReduce(self):
        for init in xrange(10):
            prime_factors_stream = PrimeFactors(910)
            reduced_stream = Stream.prefixReduce(add, prime_factors_stream, init)
            reduced_values = reduced_stream.popN(20)
            self.assertEquals(reduced_values, (2, 5, 7, 13, (2 + 5 + 7 + 13 + init)))

    def test_popN(self):
        random_stream = Randoms()
        reduced_stream = Stream.prefixReduce(add, random_stream, 0)
        start_time = time.time()
        reduced_values = reduced_stream.popN(10000)
        end_time = time.time()

        random_stream = Randoms()
        reduced_stream = Stream.prefixReduce(add, random_stream, 0)
        start_time = time.time()
        reduced_values = reduced_stream.popN(10000, multiThread=True)
        end_time = time.time()

def main(argv):
    unittest.main()

if __name__ == "__main__":
    main(sys.argv)
