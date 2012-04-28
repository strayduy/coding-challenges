import sys

def get_sequence_time(sequence_str):
    sequence = []

    s = sequence_str.strip().split(" ", 1)[1].split()

    for (bot, button) in zip(s[0::2], s[1::2]):
        sequence.append((bot, int(button)))

    other = { "O" : "B", "B" : "O" }
    position = { "O" : 1, "B" : 1 }
    individual_time = { "O" : 0, "B" : 0 }
    total_time = 0
    prev_action = None

    for action in sequence:
        bot        = action[0]
        button_pos = action[1]
        time       = abs(button_pos - position[bot]) + 1
        if prev_action is not None and prev_action[0] != bot:
            time = max(time - individual_time[other[bot]], 1)
            individual_time[bot] = 0
        total_time += time
        position[bot] = button_pos
        individual_time[bot] += time
        prev_action = action

    return total_time

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_FILE" % (sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [l.strip() for l in f.readlines()]
    num_cases = int(lines[0])
    for i,case in enumerate(lines[1:num_cases+1]):
        print "Case #%d: %d" % (i+1, get_sequence_time(case))

