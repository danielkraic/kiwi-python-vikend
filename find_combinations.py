#!/usr/bin/env python3

from __future__ import print_function
import sys
from datetime import datetime, timedelta
import calendar
from itertools import count
import networkx as nx

class Flight(object):
    """flight info
    """
    _ids = count(0)

    def __init__(self):
        self.flight_id = next(self._ids) # next(get_next_id())
        self.source = None
        self.destination = None
        self.departure = None
        self.arrival = None
        self.flight_number = None
        self.price = None
        self.bags_allowed = None
        self.bag_price = None

    def parse_line(self, line):
        """parse Flight data from string
        :param lene line string data
        :return error message
        """
        (self.source,
         self.destination,
         departure_s,
         arrival_s,
         self.flight_number,
         price_s,
         bags_allowed_s,
         bag_price_s) = line.split(',')

        to_timestamp = lambda s: calendar.timegm(datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').utctimetuple())

        try:
            self.departure = to_timestamp(departure_s)
        except ValueError:
            return "Invalid departure date: {}".format(departure_s)

        try:
            self.arrival = to_timestamp(arrival_s)
        except ValueError:
            return "Invalid arrival date: {}".format(arrival_s)

        if not price_s.isdigit():
            return "price is not digit"
        if not bags_allowed_s.isdigit():
            return "bags_allowed is not digit"
        if not bag_price_s.isdigit():
            return "bag_price is not digit"

        self.price = int(price_s)
        self.bags_allowed = int(bags_allowed_s)
        self.bag_price = int(bag_price_s)

    def __str__(self):
        return '{fl}: {src} {st} ->  {dest} {end}'.format(
            fl=self.flight_number,
            src=self.source,
            dest=self.destination,
            st=self.departure,
            end=self.arrival)

    def is_connecting_of(self, other_flight):
        """check if current flight may be connecting flight of other_flight
        :param other_flight
        :return True if current flight may be connecting flight of other_flight
        """
        if self.source != other_flight.destination:
            return False

        if self.departure < other_flight.arrival:
            return False

        diff = self.departure - other_flight.arrival

        if diff > 4 * 60 * 60 or diff < 1 * 60 * 60:
            return False

        return True

def add_flight_connection(flight_connections, flight1, flight2):
    """add connection between flights (flight2 is connection flight of flight1)
    :param flight_connections dict of flight connections
    :param flight1 first flight
    :param flight2 second flight
    """
    if flight1 not in flight_connections:
        flight_connections[flight1] = []

    flight_connections[flight1].append(flight2)

def add_connections_to_paths(flight_connections, final_paths, current_path):
    src = current_path[-1]
    if src not in flight_connections:
        return

    paths = [current_path + [dest] for dest in flight_connections[src]]
    for p in paths:
        if len(p) == 0 or p[0] == p[-1]:
            continue

        final_paths.append(p)
        add_connections_to_paths(flight_connections, final_paths, p)

def get_all_paths(flight_connections):
    final_paths = []
    for src in flight_connections:
        p = [src]
        add_connections_to_paths(flight_connections, final_paths, p)

    return final_paths

if __name__ == "__main__":
    lines_count = 0
    flights = []
    flight_connections = {}

    for line in sys.stdin:
        lines_count += 1

        line = line.rstrip('\n')

        new_flight = Flight()
        err = new_flight.parse_line(line=line)
        if err:
            print("err{cnt}: {err}\n".format(cnt=lines_count, err=err))
        else:
            # check flight connection with previously imported flights
            for f in flights:
                if new_flight.is_connecting_of(f):
                    add_flight_connection(flight_connections, f.flight_id, new_flight.flight_id)
                if f.is_connecting_of(new_flight):
                    add_flight_connection(flight_connections, new_flight.flight_id, f.flight_id)

            # add new flight
            flights.append(new_flight)

    print("number of flights imported:", len(flights))

    paths = get_all_paths(flight_connections=flight_connections)
    print("paths: {}".format(len(paths)))
    for p in paths:
        print(p)
