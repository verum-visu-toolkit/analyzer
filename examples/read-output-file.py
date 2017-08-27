import sys
from vvanalyzer import file
from pprint import pprint

with open(sys.argv[1], 'rb') as f:
    parsed_data = file.read_output_file(f)
    pprint(parsed_data, depth=3)
