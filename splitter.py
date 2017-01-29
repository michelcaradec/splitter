#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import re


def try_parse_float(text):
    """
    Try to parse a string to a float.
    """
    try:
        return float(text)
    except ValueError:
        return None


def cnv_bytes(text):
    """
    Convert a string to a value in bytes.
    """
    value = try_parse_float(text)
    if value:
        return int(value)

    pattern = r"(\d+)([\.]{0,1})([\d]*)([\s]*)([\w]*)"
    matches = re.match(pattern, text, re.IGNORECASE)
    if matches and len(matches.groups()) == 5:
        value = try_parse_float("".join(matches.groups()[0:4]).strip())
        if value:
            unit = matches.groups()[4].strip().lower()
            if unit == "kb":
                factor = 1024
            elif unit == "mb":
                factor = 1024 ** 2
            elif unit == "gb":
                factor = 1024 ** 3
            elif unit == "tb":
                factor = 1024 ** 4
            else:
                factor = 1

            return int(value * factor)

    return None


def split(input_stream,
          batch_count=None, \
          batch_size=None, \
          output_file="output", \
          reject_file=None, \
          skip_line=None,
          skip_insert=False):
    """
    Split function.
    """
    if not batch_count and not batch_size:
        batch_size = 1024 ** 2 # Default batch size = 1Mb

    skipped_lines = []
    # Rejected lines
    if skip_line and skip_line > 0:
        f_reject = open(reject_file, "w") if reject_file else None
        for num, line in enumerate(input_stream, 1):
            if f_reject:
                f_reject.write(line)
            if skip_insert:
                skipped_lines.append(line)
            if num >= skip_line:
                break

        if f_reject:
            f_reject.close()
            f_reject = None

    # Lines to partition
    f_output = None
    batch_num = 0
    size = 0
    for idx, line in enumerate(input_stream):
        close_output = False

        if batch_size:
            line_len = len(line)
            size += line_len
            if size >= batch_size:
                close_output = True
                size = line_len
        elif batch_count:
            if idx and idx % batch_count == 0:
                close_output = True

        if close_output and f_output:
            f_output.close()
            f_output = None

        if not f_output:
            batch_num += 1
            f_output = open("%s.part%05d" % (output_file, batch_num), "w")
            # Insert skipped lines at beginning of file
            for skipped_line in skipped_lines:
                f_output.write(skipped_line)

        f_output.write(line)

    if f_output:
        f_output.close()
        f_output = None


def main(args):
    """
    Main function.
    """
    batch_count = None # Batch size in number of lines
    batch_size = None # Batch size if bytes
    output_file = "output"
    reject_file = None
    skip_line = None # Number of lines to skip
    skip_insert = False # Insert skipped lines at begin of each file segment

    for arg in args:
        if arg.startswith("-batchcount:"):
            value = int(arg[12:])
            batch_count = value if value > 0 else None
        if arg.startswith("-batchsize:"):
            value = cnv_bytes(arg[11:])
            batch_size = value if value > 0 else None
        elif arg.startswith("-output:"):
            value = arg[8:]
            if value:
                output_file = value
        elif arg.startswith("-skip:"):
            skip_line = int(arg[6:])
        elif arg.startswith("-skipreject:"):
            reject_file = arg[12:]
        elif arg.startswith("-skipinsert"):
            skip_insert = True

    split(sys.stdin, batch_count, batch_size, output_file, reject_file, skip_line, skip_insert)


if __name__ == "__main__":
    """
    [input] | python splitter.py -batchcount:3 -output:output -skipreject:header.txt -skip:1
    """
    main(sys.argv[1:])
