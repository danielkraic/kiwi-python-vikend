"""
find combinations of flights
https://gist.github.com/martin-kokos/7fb98650c66bd8d93767da6627affffa
"""

from __future__ import print_function
import argparse
import sys
from flight_paths import FlightPaths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find flights paths from flights data")
    parser.add_argument('--json', action='store_true', help='print output in json format')
    parser.add_argument('--summary', action='store_true', help='print output in summary format')

    args = parser.parse_args()

    fp = FlightPaths()
    fp.import_flights(input_=sys.stdin)

    if args.json:
        print(fp.to_json())
    elif args.summary:
        print(fp.get_summary())
    else:
        print(fp.to_string())
