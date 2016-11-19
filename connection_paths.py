"""
flights connection paths related functionality
"""

def add_connections_to_paths(flight_connections, final_paths, current_path):
    """
    add current path with its connections to final list of paths
    :param flight_connections dict of flight connactions
    :param final_paths list of all final connection paths
    """
    src = current_path[-1]
    if src not in flight_connections:
        return

    paths = [current_path + [dest] for dest in flight_connections[src]]
    for path in paths:
        if len(path) == 0 or path[0] == path[-1]:
            continue

        final_paths.append(path)
        add_connections_to_paths(flight_connections, final_paths, path)

def get_all_paths(flight_connections):
    """
    get list of all possible connection paths from flight connections
    :param flight_connections dict of flight connactions
    :return list of all possible connection paths from flight connections
    """
    final_paths = []
    for src in flight_connections:
        path = [src]
        add_connections_to_paths(flight_connections, final_paths, path)

    final_paths.sort()
    return final_paths
