#!/usr/bin/env python3

import argparse
import datalad.api
from shutil import copyfile
import os.path
from os import listdir

parser = argparse.ArgumentParser(description='install datalad procedures')
parser.add_argument('--destination', help = 'destination')

args = parser.parse_args()

destination = None
if args.destination:
    destination = args.destination
else:
    procedures = datalad.api.run_procedure(discover = True)
    
    for procedure in procedures:
        if procedure['procedure_name'] == 'cfg_yoda':
            destination = os.path.dirname(procedure['path'])
            break

if destination is None:
    raise Exception('could not find a suitable destination for the procedures. please select one with --destination')

for script in os.listdir('procedures'):
    input = os.path.join('procedures', script)
    output = os.path.join(destination, script)
    copyfile(input, output)
    print("copied {} to {}".format(input, output))