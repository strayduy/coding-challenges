#!/usr/bin/python2.6

# Standard libs
import math
import sys

NUM_JUDGES = 3

def get_max_number_of_scores_above_threshold(num_googlers,
                                             num_surprising_scores,
                                             score_threshold,
                                             total_scores):
    if score_threshold == 0:
        return num_googlers

    num_scores_above_threshold   = 0
    surprising_results_remaining = num_surprising_scores

    # Sort scores in descending order.
    # We want to iterate over the highest scores first in order to
    # maximize the number of scores above the threshold.
    total_scores.sort(reverse=True)

    for total_score in total_scores:
        mean_score                 = total_score / float(NUM_JUDGES)
        best_non_surprising_result = min(total_score, int(math.ceil(mean_score)))

        # If the remainder of the total score / the number of judges != 1,
        # we'll be able to "boost" the best non-surprising result by 1
        if total_score % NUM_JUDGES != 1:
            best_surprising_result = min(total_score, best_non_surprising_result + 1)
        else:
            best_surprising_result = best_non_surprising_result

        if best_non_surprising_result >= score_threshold:
            num_scores_above_threshold += 1
        # Think of the number of surprising results as the number of times we
        # can "boost" a score above the threshold.
        # We'll only boost scores that are below the threshold.
        elif best_surprising_result >= score_threshold and \
             surprising_results_remaining > 0:
            num_scores_above_threshold += 1
            # Deduct from the number of surprising results each time we boost
            surprising_results_remaining -= 1

    return num_scores_above_threshold

def process_line(input_line):
    split_line  = [int(i) for i in input_line.split()]
    num_googlers = split_line.pop(0)
    num_surprising_scores = split_line.pop(0)
    score_threshold = split_line.pop(0)
    return str(get_max_number_of_scores_above_threshold(num_googlers,
                                                        num_surprising_scores,
                                                        score_threshold,
                                                        split_line))

def main(argv):
    if len(argv) != 2:
        print "Usage: python %s INPUT_FILE" % (sys.argv[0])
        return 1

    input_filepath = argv[1]

    with open(input_filepath, "r") as input_file:
        print "\n".join([
            "Case #%d: %s" % (i + 1, process_line(line.strip()))
            for i, line
            in enumerate(input_file.readlines()[1:])
        ])

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

