"""run.py

Run the converter.

Usage:

$ cat SCIENCE_PARSE_FILE | python3 run.py
$ python3 run.py SCIENCE_PARSE_FILE
$ python3 run.py SCIENCE_PARSE_FILE LIF_FILE

In the first invocation the script takes standard input and writes to standard
output, in the second it reads a file and write to standard output and in the
third it reads a file and saves output in a file.

"""


import sys
import json

from converter import Converter


def parse(infile=None, outfile=None):
    fh_in = sys.stdin if infile is None else open(infile)
    fh_out = sys.stdout if outfile is None else open(outfile, 'w')
    data = fh_in.read()
    container = Converter(data)
    fh_out.write(container.as_json_string())


if __name__ == '__main__':

    infile = None
    outfile = None
    if len(sys.argv) > 1:
        infile = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    parse(infile, outfile)
