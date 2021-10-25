"""test.py

Create LIF files from the Science Parse output. Testing the code on a directpory
with ScienceParse output files.

Usage:

$ python3 test.py JSON_DIR LIF_DIR TXT_DIR

The first directory is the one with JSON files created by science parse, the
second the target for LIF files and the third the target for text files. All
directories are assumed to exist.

"""


import os
import sys
import json

from converter import Converter
from lif import Container


def create_lif_files(science_parse_dir, lif_dir, txt_dir, test=False):
    for fname in os.listdir(science_parse_dir):
        create_lif_file(os.path.join(science_parse_dir, fname),
                        os.path.join(lif_dir, fname[:-5] + '.lif'),
                        os.path.join(txt_dir, fname[:-5] + '.txt'),
                        test)


def create_lif_file(json_file, lif_file, txt_file, test=False):
    print("Creating {}".format(lif_file))
    with open(json_file, encoding='utf8') as fh_in, \
         open(lif_file, 'w', encoding='utf8') as fh_out_lif, \
         open(txt_file, 'w', encoding='utf8') as fh_out_txt:
        c = Converter(fh_in.read())
        fh_out_lif.write(c.as_json_string())
        fh_out_txt.write(c.text_value())
    if test:
        test_lif_file(lif_file)

        
def test_lif_file(lif_file):
    """Just print the text of all headers, should give an indication of whether all
    the offsets are correct."""
    lif = Container(json_file=lif_file).payload
    text = lif.text.value
    view = lif.views[0]
    for anno in view.annotations:
        if anno.type.endswith('Header'):
            print("[{}]".format(text[anno.start:anno.end]))
    print('')


if __name__ == '__main__':

    science_parse_dir = sys.argv[1]
    lif_dir = sys.argv[2]
    txt_dir = sys.argv[3]
    create_lif_files(science_parse_dir, lif_dir, txt_dir, test=False)


    
