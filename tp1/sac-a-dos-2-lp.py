#!/usr/bin/python3
# coding: utf-8
import sys
import argparse

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input-file',
    dest='input_file')
parser.add_argument('-o', '--output-file',
    dest='output_file',
    help='if no output file is specified, then the output is produced on stdout')
args = parser.parse_args()

if args.input_file == None:
    parser.error('specify an input file')

input_file = open(args.input_file,'r')

if args.output_file == None:
    output_file = sys.stdout
else:
    output_file = open(args.output_file, 'w')

objects = []
capacity = None

for line in input_file:
    toks = line.split()

    if len(toks) == 0 or toks[0] == '#':
        continue

    if capacity == None:
        if len(toks) != 1:
            raise Exception(
                'Error while parsing capacity: expected one token, got ' + str(len(toks)))

        capacity = toks[0]
    else:
        if len(toks) != 3:
            raise Exception(
                'Error while parsing object: expected 3 tokens, got ' + str(len(toks)))

        objects.append({'id': toks[0], 'weight': toks[1], 'value': toks[2]})

input_file.close()

output_file.write('Maximize\n')
output_file.write(
    '    ' + \
    ' + '.join(map(lambda obj: obj['value'] + ' x' + obj['id'], objects)))
output_file.write('\nSubject to\n')
output_file.write(
    '    c: ' \
    + ' + '.join(map(lambda obj: obj['weight'] + ' x' + obj['id'], objects)) \
    + ' <= ' + capacity)
output_file.write('\nBinary\n')
output_file.write(
    '    ' + \
    '\n    '.join(map(lambda obj: ' x' + obj['id'], objects)))
output_file.write('\nEnd')
output_file.close()

