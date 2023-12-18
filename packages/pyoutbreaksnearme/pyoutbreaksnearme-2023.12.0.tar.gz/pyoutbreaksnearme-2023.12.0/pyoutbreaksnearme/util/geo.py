"""Define various geographical utilities."""
from math import asin, cos, radians, sin, sqrt


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Determine the distance between two latitude/longitude pairs.

    Args:
        lat1: The first latitude.
        lon1: The first longitude.
        lat2: The second latitude.
        lon2: The second longitude.

    Returns:
        The distance between the two coordinates.
    """
    lon1, lat1, lon2, lat2 = (radians(val) for val in (lon1, lat1, lon2, lat2))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    calc_a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    calc_c = 2 * asin(sqrt(calc_a))
    return 6371 * calc_c
