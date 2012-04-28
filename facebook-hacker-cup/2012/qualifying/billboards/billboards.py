#!/usr/bin/python

import sys

def get_word_lengths(sentence):
    word_lengths = []
    prev_word_break_index = 0
    max_word_length = 0

    # Retrieve the length of each word in sentence
    for i,char in enumerate(sentence):
        if char == " ":
            word_length = i - prev_word_break_index
            word_lengths.append(word_length)
            if word_length > max_word_length:
                max_word_length = word_length
            prev_word_break_index = i + 1
    word_length = i - prev_word_break_index + 1
    word_lengths.append(word_length)
    if word_length > max_word_length:
        max_word_length = word_length

    return word_lengths, max_word_length

def get_number_of_lines(word_lengths, font_size, max_width):
    line_length = 0
    line_count  = 1

    for word_length in word_lengths:
        # First word of the line
        if line_length == 0:
            # Word by itself fills line
            if word_length * font_size >= max_width:
                line_count += 1
                line_length = 0
            else:
                line_length = word_length * font_size
        # Middle of line
        else:
            if line_length + (word_length + 1) * font_size >= max_width:
                line_count += 1
                line_length = word_length * font_size
            else:
                line_length += (word_length + 1) * font_size

    return line_count

def get_max_font_size(input_line):
    width, height, sentence = input_line.split(" ", 2)
    width  = int(width)
    height = int(height)

    word_lengths, max_word_length = get_word_lengths(sentence)

    # If the longest word can't fit with a 1" font, return 0
    if max_word_length > width:
        return 0

    # Find the max width that would fit the longest word on one line
    max_font_size = width / max_word_length

    for font_size in range(max_font_size, 0, -1):
        num_lines = get_number_of_lines(word_lengths, font_size, width)
        text_height = num_lines * font_size
        if text_height <= height:
            break

    return font_size

if len(sys.argv) != 2:
    print "Usage: python %s INPUT_FILE" % (sys.argv[0])
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = [l.strip() for l in f.readlines()]
    num_cases = int(lines[0])
    for i,case in enumerate(lines[1:num_cases+1]):
        print "Case #%d: %d" % (i+1, get_max_font_size(case))

