#!python2.7

# Standard libs
import argparse

def get_min_flips(stack):
    if not stack or '-' not in stack:
        return 0

    # Truncate the happy bottom of the stack
    last_blank_index = stack.rindex('-')
    part_we_still_need_to_flip = stack[:last_blank_index + 1]

    # If the top of the stack is blank, we can make progress by flipping the
    # entire rest of the stack. The run of blanks at the top will become a
    # run of happy pancakes at the bottom.
    if part_we_still_need_to_flip[0] == '-':
        flipped = flip(part_we_still_need_to_flip)
        return 1 + get_min_flips(flipped)

    # Otherwise, we have a run of happy pancakes at the top. Flip those and
    # we'll recurse into the first case in the next cycle.
    first_blank_index = stack.index('-')
    half_to_flip = part_we_still_need_to_flip[:first_blank_index]
    half_to_not_flip = part_we_still_need_to_flip[first_blank_index:]
    return 1 + get_min_flips(flip(half_to_flip) + half_to_not_flip)

def flip(stack):
    return ''.join(['+' if p == '-' else '-' for p in stack[::-1]])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    with open(args.input_file) as f:
        num_cases = f.readline()
        for i, line in enumerate(f, start=1):
            stack = line.strip()
            print "Case #%d: %d" % (i, get_min_flips(stack))

if __name__ == "__main__":
    main()

