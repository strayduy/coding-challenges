#!/usr/bin/env python2.7

# Standard libs
from collections import defaultdict
import operator
import re
import sys

# Constants
USAGE = "python %s INPUT_FILE" % (sys.argv[0])
LETTER_REGEX = re.compile(r"""^[A-Za-z]$""");
MAX_CHAR_BEAUTY = 26

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

        # Evaluate the beauty of each test case
        for test_case_number in range(1, num_test_cases + 1):
            input_string = input_file.readline().strip()
            max_beauty = get_max_beauty(input_string)
            print "Case #%d: %d" % (test_case_number, max_beauty)

# To maximize the beauty of a string, we want to first count the number of
# occurrences of each letter. Then, we want to assign the highest beauty value
# to the most frequently occurring letter, and the second highest beauty value
# to the second-most frequently occurring letter, and so on.
def get_max_beauty(input_string,
                   valid_char_regex=LETTER_REGEX,
                   max_char_beauty=MAX_CHAR_BEAUTY):
    if not input_string:
        return 0

    # Dict for keeping track of the number of occurrences of each character in
    # the input string.
    # Default dict value = 0
    char_occurrences = defaultdict(int)

    # Normalize the input string
    normalized_input_string = normalize_input_string(input_string)

    # Count the occurrences of each valid character
    for char in normalized_input_string:
        if valid_char_regex.match(char):
            char_occurrences[char] += 1

    # Sort the dict by the number of occurrences for each character, in
    # descending order.
    # We don't actually care about the individual characters anymore, but we
    # still want to keep track of the number of occurrences AND the relative
    # order of these occurrences.
    # So we'll throw away the letter value but replace it with the index of
    # each item in the sorted list (via enumerate).
    # Reference:
    # http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
    sorted_occurrences = [(index, item[1])
                          for index, item
                          in enumerate(sorted(char_occurrences.iteritems(),
                                              key=operator.itemgetter(1),
                                              reverse=True))]

    # Compute the individual beauty contribution of each character by
    # multiplying the Nth highest beauty value by the number of occurrences
    # for that character.
    # Sum up the contribution of each letter to get the total max beauty.
    max_beauty = sum([(MAX_CHAR_BEAUTY - index) * num_occurrences
                      for index, num_occurrences
                      in sorted_occurrences])

    return max_beauty

# We just need to lowercase the string so the same lowercase and uppercase
# letters are counted together
def normalize_input_string(input_string):
    return input_string.lower()

if __name__ == "__main__":
    main(sys.argv)
