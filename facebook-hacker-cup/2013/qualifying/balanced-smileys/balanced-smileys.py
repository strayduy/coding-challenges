#!/usr/bin/env python2.7

# Standard libs
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

        # Check whether each test case has balanced parentheses
        for test_case_number in range(1, num_test_cases + 1):
            input_string = input_file.readline().strip()
            has_balanced_parentheses = check_balanced_parentheses(input_string)
            output = "YES" if has_balanced_parentheses else "NO"
            print "Case #%d: %s" % (test_case_number, output)

# Represents the parentheses balance state of a string, i.e. how many
# parentheses have been opened by this point.
#
# In our algorithm, we might want to evaluate parts of a string for
# parentheses balance, and it'll be helpful to be able to "jump" to the middle
# of a string.
class BalanceState:
    def __init__(self, input_string, open_parentheses=0):
        self.input_string = input_string
        self.open_parentheses = open_parentheses

    def __str__(self):
        return "<%s, %d>" % (self.input_string, self.open_parentheses)

    def __repr__(self):
        return str(self)

# Returns True if the input string has balanced parentheses
# Returns False otherwise
#
# Algorithm:
# We'll iterate through the string one char at a time, keeping track of the
# opening and closing of parentheses. If the number of opens and closes
# balance out, then we'll return True.
#
# Additionally, we'll keep track of different possible interpretaions of a
# parentheses in a queue. We'll see if the string balances out if we treat it
# like a regular parentheses, and if that doesn't work, we'll try to treat it
# as part of an emoticon.
#
# Only when we've exhausted all possible interpretations will we declare a
# string as unbalanced.
def check_balanced_parentheses(input_string):
    if not input_string:
        return True

    # Queue of possible strings to check
    # Each item in the queue will have an input string, and the current open
    # parentheses count for that string
    balance_states = [BalanceState(input_string)]

    while balance_states:
        balance_state = balance_states.pop(0)

        # The substring that we're checking for balanced parentheses
        input_string = balance_state.input_string

        # Number of parentheses that have been opened but not closed yet
        # We'll increment this count every time we open a parentheses, and
        # we'll decrement it when we close a parentheses.
        open_parentheses = balance_state.open_parentheses

        for i, char in enumerate(input_string):
            if char == "(":
                # If this parentheses could be part of an emoticon,
                # add the rest of the string to the queue of strings to check
                if i > 0 and input_string[i - 1] == ":":
                    balance_states.append(BalanceState(input_string[i + 1:], open_parentheses))

                # Increment the open_parentheses count every time we open one
                open_parentheses += 1
            elif char == ")":
                # If this parentheses could be part of an emoticon,
                # add the rest of the string to the queue of strings to check
                if i > 0 and input_string[i - 1] == ":":
                    balance_states.append(BalanceState(input_string[i + 1:], open_parentheses))

                # Decrement the open_parentheses every time we close one
                if open_parentheses > 0:
                    open_parentheses -= 1
                else:
                    # If we close a parentheses before opening one, then the
                    # string becomes immediately unbalanced
                    # Give up on this substring
                    open_parentheses = -1
                    break

        # If we get to the end of a string with a balanced parentheses count,
        # then we can stop here
        if open_parentheses == 0:
            return True

    # If execution reaches this point, we've tried all the possible
    # parentheses interpretations, and none of them balanced out.
    return False

if __name__ == "__main__":
    main(sys.argv)
