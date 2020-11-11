import argparse
import sys
import os.path as ops
import json

sys.path.insert(1,'../src/hw3')
from ponyCode import *

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('csv_path', help="provide the path to the csv file")
    parser.add_argument('-o', '--output', help="Output file name", default='stdout')
    args=parser.parse_args()

    csv_path=args.csv_path

    dict_path=ops.join('..','data','words_alpha.txt')

    parseCSV(csv_path, dict_path)

    if args.output is not None:
        write_to_file(output_to_set(),args.output)
    else:
        json.dump(output_to_set(), sys.stdout)

if __name__=='__main__':
    main()



