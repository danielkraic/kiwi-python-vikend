"""
flights connection paths related functionality
"""

def get_flight(flight_id, flights):
    for f in flights:
        if f.flight_id == flight_id:
            return f

    raise ValueError("Invalid flight_id: {}".format(flight_id))

def add_connections_to_paths(flight_connections, flights, final_paths, current_path):
    """
    add current path with its connections to final list of paths
    :param flight_connections dict of flight connactions
    :param final_paths list of all final connection paths
    """
    src_flight = current_path[-1]
    if src_flight.flight_id not in flight_connections:
        return

    paths = [current_path + [get_flight(flights=flights, flight_id=dest)] for dest in flight_connections[src_flight.flight_id]]
    for path in paths:
        if len(path) > 0:
            if path[0].source != path[-1].destination:
                final_paths.append(path)

            add_connections_to_paths(flight_connections=flight_connections, flights=flights, final_paths=final_paths, current_path=path)

def get_all_paths(flights, flight_connections):
    """
    get list of all possible connection paths from flight connections
    :param flights list of all flights
    :param flight_connections dict of flight connactions
    :return list of all possible connection paths from flight connections
    """
    final_paths = []
    for src in flight_connections:
        src_flight = get_flight(flights=flights, flight_id=src)
        path = [src_flight]
        add_connections_to_paths(flight_connections=flight_connections, flights=flights, final_paths=final_paths, current_path=path)

    # final_paths.sort(key=lambda flight: flight.departure)
    return final_paths


def get_flight_diff(flight1, flight2):
    diff = flight2.departure - flight1.arrival
    minutes, seconds = divmod(diff, 60)
    hours, minutes = divmod(minutes, 60)
    return "{hours}h {minutes}m {seconds}s".format(hours=hours, minutes=minutes, seconds=seconds)

def path_to_string(path, flights):
    """
    get human readable string of path flights
    """
    output = ''

    i = 0
    while i < len(path):
        if i != 0:
            output += 'diff: {}\n'.format(get_flight_diff(path[i-1], path[i]))

        output += "{}\n".format(path[i])

        i += 1

    return output
