"""
flight class with flight related data
"""

from itertools import count
from datetime import datetime
import calendar

def string2timestamp(datetime_string):
    """convert datetime string to timestamp
    :param datetime_string datetime string
    :return imestamp value
    """
    return calendar.timegm(datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S').utctimetuple())

def timestamp2string(timestamp):
    """
    convert timestamp value to string
    :param timestamp timestamp ValueError
    :return string value
    """
    return datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')

class Flight(object):
    """
    flight info
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

    def parse_from_string(self, string):
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
         bag_price_s) = string.split(',')

        try:
            self.departure = string2timestamp(departure_s)
        except ValueError:
            return "Invalid departure date: {}".format(departure_s)

        try:
            self.arrival = string2timestamp(arrival_s)
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
            st=timestamp2string(self.departure),
            end=timestamp2string(self.arrival))

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

        if diff > (4 * 60 * 60):
            return False

        if diff < (1 * 60 * 60):
            return False

        return True
