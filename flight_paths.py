"""
flight paths related functionality module
"""

import json
from flight import Flight, get_timestamps_diff, timestamp2string

class FlightPaths(object):
    """
    flight paths
    """
    def __init__(self):
        self._flights = []
        self._flight_connections = {}
        self._paths = []

    def _add_flight_connection(self, flight1, flight2):
        """add connection between flights (flight2 is connection flight of flight1)
        :param flight_connections dict of flight connections
        :param flight1 first flight
        :param flight2 second flight
        """
        if flight1 not in self._flight_connections:
            self._flight_connections[flight1] = []

        self._flight_connections[flight1].append(flight2)

    def import_flights(self, input_):
        """
        import flights from input
        :param input input
        """
        for line in input_:
            line = line.rstrip('\n')

            new_flight = Flight()
            err = new_flight.parse_from_string(string=line)
            if err:
                continue

            # check flight connection with previously imported flights
            for f in self._flights:
                if new_flight.is_connecting_of(f):
                    self._add_flight_connection(f, new_flight)
                if f.is_connecting_of(new_flight):
                    self._add_flight_connection(new_flight, f)

            # add new flight
            self._flights.append(new_flight)

        self._explore_paths()

    def _explore_paths(self):
        for src in self._flight_connections:
            path = [src]
            self._add_connections_to_paths(path=path)

    def _add_connections_to_paths(self, path):
        src_flight = path[-1]
        if src_flight not in self._flight_connections:
            return

        paths = [path + [dest] for dest in self._flight_connections[src_flight]]
        for path in paths:
            if len(path) > 0:
                if path[0].source != path[-1].destination:
                    self._paths.append(path)

                self._add_connections_to_paths(path=path)

    def _path_to_string(self, path):
        """
        get human readable string of path
        """
        bags_allowed = min([f.bags_allowed for f in path])
        full_price = ''
        for bags_count in range(bags_allowed+1):
            full_price += 'bags:{bags_count},price:{price}. '.format(
                bags_count=bags_count,
                price=sum([f.get_full_price(bags_count) for f in path]))

        output = '''
Source: {source} {departure}
Destination {destination} {arrival}
Duration: {duration}
Bags allowed: {bags_allowed}
Price: {full_price}
Number of flights: {flights_count}
'''.format(

    source=path[0].source,
    destination=path[-1].destination,
    departure=timestamp2string(path[0].departure),
    arrival=timestamp2string(path[-1].arrival),
    duration=get_timestamps_diff(start=path[0].departure, end=path[-1].arrival),
    full_price=full_price,
    bags_allowed=bags_allowed,
    flights_count=len(path))

        i = 0
        while i < len(path):
            if i != 0:
                output += '  Delay between flights: {}\n'.format(
                    get_timestamps_diff(start=path[i-1].arrival, end=path[i].departure))

            output += "  Flight {flight_number}: {flight_info}\n".format(
                flight_number=i+1, flight_info=path[i].to_string())
            i += 1

        return output

    def _path_to_json(self, path, ):
        """
        get json object from path
        """
        bags_allowed = min([f.bags_allowed for f in path])
        full_price = []
        for bags_count in range(bags_allowed+1):
            full_price.append(dict(
                bags_count=bags_count,
                price=sum([f.get_full_price(bags_count) for f in path])))

        return dict(
            source=path[0].source,
            destination=path[-1].destination,
            departure=path[0].departure,
            arrival=path[-1].arrival,
            duration=path[-1].arrival - path[0].departure,
            full_price=full_price,
            bags_allowed=bags_allowed,
            flights=[f.to_json() for f in path]
        )

    def to_string(self):
        """
        get human readable string of all paths
        """
        if not self._paths:
            return 'No paths found. Number of imported flights: {}. Number of found flight connections: {}.'.format(
                len(self._flights), len(self._flight_connections)
            )

        output = ''
        for path in self._paths:
            output += self._path_to_string(path=path) + '\n'

        return output

    def to_json(self):
        """
        get json object from all paths
        """
        output = []
        for path in self._paths:
            output.append(self._path_to_json(path=path))

        return json.dumps(output)
