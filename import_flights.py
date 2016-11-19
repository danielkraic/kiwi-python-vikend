"""
flight import related functionality
"""

from flight import Flight

def add_flight_connection(flight_connections, flight1, flight2):
    """add connection between flights (flight2 is connection flight of flight1)
    :param flight_connections dict of flight connections
    :param flight1 first flight
    :param flight2 second flight
    """
    if flight1 not in flight_connections:
        flight_connections[flight1] = []

    flight_connections[flight1].append(flight2)

def import_flights(input):
    """
    import flights from input
    :param input input
    :return tuple of flights lists and flights connections dict
    """
    flights = []
    flight_connections = {}

    for line in input:
        line = line.rstrip('\n')

        new_flight = Flight()
        err = new_flight.parse_from_string(string=line)
        if not err:
            # check flight connection with previously imported flights
            for f in flights:
                if new_flight.is_connecting_of(f):
                    add_flight_connection(flight_connections, f.flight_id, new_flight.flight_id)
                if f.is_connecting_of(new_flight):
                    add_flight_connection(flight_connections, new_flight.flight_id, f.flight_id)

            # add new flight
            flights.append(new_flight)

    return (flights, flight_connections)
