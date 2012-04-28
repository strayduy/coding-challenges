import sys

def get_possibleness(games_today_upper_bound, win_percent_today, win_percent_lifetime):
    #print games_today_upper_bound, win_percent_today, win_percent_lifetime

    if win_percent_lifetime >= 100 and win_percent_today < 100:
        return "Broken"
    if win_percent_lifetime <= 0 and win_percent_today > 0:
        return "Broken"

    #for i in range(1, games_today_upper_bound + 1):
    i = 1
    while i <= games_today_upper_bound:
        if i * win_percent_today % 100 == 0:
            #games_today = i * win_percent_today
            #print "today = %f/%d" % ((i * win_percent_today / 100.0), i)
            for j in range(i, 101):
                if j * win_percent_lifetime % 100 == 0:
                    #games_lifetime = j * win_percent_lifetime
                    #print "lifetime = %f/%d" % (j * games_lifetime / 100.0, j)
                    return "Possible"
        i += 1

    return "Broken"

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_FILE" % (sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [l.strip() for l in f.readlines()]
    num_cases = int(lines.pop(0))
    case_num = 1
    while lines:
        case = [int(i) for i in lines.pop(0).split()]
        print "Case #%d: %s" % (case_num, get_possibleness(case[0], case[1], case[2]))
        case_num += 1

