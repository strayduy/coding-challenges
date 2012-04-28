import sys

def xor(x, y):
    return x ^ y

def add(x, y):
    return x + y

def get_max_candy(candy_values_str):
    max_candy = 0
    candy_values = [int(value) for value in candy_values_str.split()]
    xor_sum = reduce(xor, candy_values)

    if xor_sum != 0:
        return "NO"

    # If the elements of the list XOR'd together == 0, then you can split
    # the list in two, and both sublists will always have the same XOR sum.
    # (Not sure why that works.)
    # So to maximize the value of an individual sublist, just take all the
    # elements in the list except for the smallest one.
    candy_values.sort()
    max_candy = reduce(add, candy_values[1:])

    return str(max_candy)

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_FILE" % (sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [l.strip() for l in f.readlines()]
    num_cases = int(lines.pop(0))
    case_num = 1
    while lines:
        num_candies = int(lines.pop(0))
        case = lines.pop(0)
        print "Case #%d: %s" % (case_num, get_max_candy(case))
        case_num += 1

