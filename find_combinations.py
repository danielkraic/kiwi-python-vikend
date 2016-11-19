#!/usr/bin/env python3

"""
find combinations of flights
https://gist.github.com/martin-kokos/7fb98650c66bd8d93767da6627affffa
"""

from __future__ import print_function
import sys
from import_flights import import_flights
from connection_paths import get_all_paths

if __name__ == "__main__":
    (flights, flight_connections) = import_flights(input=sys.stdin)

    paths = get_all_paths(flight_connections=flight_connections)
    for p in paths:
        print(p)
