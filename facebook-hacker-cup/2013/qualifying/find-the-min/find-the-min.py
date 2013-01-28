#!/usr/bin/env python2.7

# Standard libs
import collections
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

        # Generate the m array for each test case
        # Compute the nth element of each m array
        for test_case_number in range(1, num_test_cases + 1):
            first_line = input_file.readline().strip()
            second_line = input_file.readline().strip()

            n, k = map(int, first_line.split(" "))
            a, b, c, r = map(int, second_line.split(" "))

            m = generate_m(k, a, b, c, r)
            nth_element = get_nth_element_of_m(m, n)
            print "Case #%d: %d" % (test_case_number, nth_element)

# Generator that spits out successive values for an m array
def next_min(initial_values):
    # sliding_window keeps track of the previous k elements.
    # deque has constant time appending and removal of elements from the ends
    # of the list.
    sliding_window = collections.deque(initial_values)

    # occurrences keeps track of how many times each value appears in the list
    # Counter has constant time "contains" lookup
    occurrences = collections.Counter(initial_values)

    next_value = popped_value = 0

    while True:
        # Determine the minimum possible value that could appear next
        next_value = min(next_value, popped_value)

        # Increment upwards from that minimum until we find a value that
        # doesn't already appear in our list
        while next_value in occurrences:
            next_value += 1
        yield next_value

        # Pop off the leftmost value from the list
        # Update our counter accordingly
        popped_value = sliding_window.popleft()
        occurrences[popped_value] -= 1
        if occurrences[popped_value] <= 0:
            del occurrences[popped_value]

        # Append the new value to the end (right) of the list
        # Update our counter accordingly
        sliding_window.append(next_value)
        occurrences[next_value] += 1

def get_nth_element_of_m(m, n):
    limit = n - len(m) - 1

    # Iterate through our generator until we get to the nth element
    for i, value in enumerate(next_min(m)):
        if i >= limit:
            break

    return value

def generate_m(k, a, b, c, r):
    m = [a]
    for i in range(1, k):
        m.append((b * m[i - 1] + c) % r)
    return m

if __name__ == "__main__":
    main(sys.argv)
