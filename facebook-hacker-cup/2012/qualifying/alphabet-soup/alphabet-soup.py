#!/usr/bin/python

import sys

def count_hackercups(sentence):
    letter_counts = {
      "h" : 0,
      "a" : 0,
      "c" : 0,
      "k" : 0,
      "e" : 0,
      "r" : 0,
      #c (appeared already)
      "u" : 0,
      "p" : 0 
    }

    # Iterate through each char in the sentence
    for char in sentence.lower():
        # Count the number of occurences of each letter
        if char in letter_counts:
            letter_counts[char] += 1
        else:
            letter_counts[char] = 1

    # Divide the number of occcurences of c by 2 (round down)
    letter_counts["c"] /= 2

    # Find the minimum number of occurences of the letters:
    # h a c k e r u p (with c's occurences divided by 2)
    count = min([letter_counts["h"],
                 letter_counts["a"],
                 letter_counts["c"],
                 letter_counts["k"],
                 letter_counts["e"],
                 letter_counts["r"],
                               #c
                 letter_counts["u"],
                 letter_counts["p"]])

    return count

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_FILE" % (sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [l.strip() for l in f.readlines()]
    num_cases = int(lines[0])
    for i,case in enumerate(lines[1:num_cases+1]):
        print "Case #%d: %d" % (i+1, count_hackercups(case))

