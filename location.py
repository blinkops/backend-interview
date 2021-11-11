from typing import Optional
from haversine import haversine

from default_values import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE


class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if value < MIN_LATITUDE or value > MAX_LATITUDE:
            raise ValueError("Invalid latitude")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if value < MIN_LONGITUDE or value > MAX_LONGITUDE:
            raise ValueError("Invalid longitude")
        self._longitude = value

    def calculate_distance(self, other_location: Optional['Location']) -> Optional[float]:
        """
        Calculates the distance between 'my' location and other_location using the haversine library.
        :param other_location: Location object
        :return: float -> distance in km if other_location is not None, else None
        """

        if other_location is None:
            return None
        return haversine((self.latitude, self.longitude), (other_location.latitude, other_location.longitude))


def parse_location(location: str) -> Location:
    """
    Parses a location string into a Location object.
    :param location: '<latitude>,<longitude>'
    :return: location object
    """

    if location is None:
        raise ValueError("Location is required")
    try:
        lat, long = location.split(',')
    except ValueError:
        raise ValueError("Invalid location format")

    return Location(float(lat), float(long))
