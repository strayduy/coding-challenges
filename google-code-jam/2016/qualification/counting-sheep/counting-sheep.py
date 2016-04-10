#!python2.7

# Standard libs
import argparse

def get_last_number(N):
    if N == 0:
        return 'INSOMNIA'

    digits = set(map(str, range(10)))

    for i in xrange(1, 999999):
        n = str(i * N)
        digits = digits - set(map(str, n))

        if not digits:
            break
    else:
        return 'INSOMNIA'

    return n

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    args = parser.parse_args()

    with open(args.input_file) as f:
        num_cases = f.readline()
        for i, line in enumerate(f, start=1):
            N = int(line.strip())
            print "Case #%d: %s" % (i, get_last_number(N))

if __name__ == "__main__":
    main()

