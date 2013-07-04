#!/usr/bin/env python2.7

# Standard libs
from collections import Counter
import sys

# Constants
USAGE = "python %s INPUT_FILE" % (sys.argv[0])
BOARD_SIZE = 4
PLAYER_SYMBOLS = ['X', 'O']
WILDCARD_SYMBOL = 'T'
EMPTY_SYMBOL = '.'

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

        # Determine the game state for each test case
        for test_case_number in range(1, num_test_cases + 1):
            rows = [input_file.readline().strip() for _ in xrange(BOARD_SIZE)]
            game_state = get_game_state(rows)
            print "Case #%d: %s" % (test_case_number, game_state)

            # Yield the extra newline after each test case
            input_file.readline()

def get_game_state(rows):
    # Given an N x N board, there are only 2*N+2 ways to line up N symbols:
    # 1. N horizontal rows
    # 2. N vertical columns
    # 3. 2 diagonals

    # Construct the columns and diagonals from the given rows
    cols = [''.join([row[i] for row in rows]) for i in xrange(BOARD_SIZE)]
    diagonals = [''.join([row[i] for i, row in enumerate(rows)]),
                 ''.join([row[BOARD_SIZE - i - 1] for i, row in enumerate(rows)])]

    has_empty_space = False

    # Iterate through the rows, columns, and diagonals and check if there's a
    # winner along any of them. Also check to see whether all the spaces on
    # board have been filled, so we can tell if the game is over.
    for line in rows + cols + diagonals:
        winner = get_winner(line)
        if winner:
            return '%s won' % (winner)

        # Stop checking for empty spaces after we've found at least one, in
        # order to avoid the repeated cost of the substring check.
        if not has_empty_space and EMPTY_SYMBOL in line:
            has_empty_space = True

    # If neither player has won, but there are still empty spaces on the
    # board, then the game's not over yet
    if has_empty_space:
        return 'Game has not completed'

    # If we've reached this point, then the board has been filled but neither
    # player has won
    return 'Draw'

# Given a line of four cells, returns the player symbol of the winner of that
# line, if there is a winner.
# Otherwise returns None.
def get_winner(line):
    counter = Counter(line)

    for symbol in PLAYER_SYMBOLS:
        # If a player has completed a line of length N with only their symbols
        # and wildcard symbols, then they've won
        if counter[symbol] + counter[WILDCARD_SYMBOL] >= BOARD_SIZE:
            return symbol

    return None

if __name__ == "__main__":
    main(sys.argv)
