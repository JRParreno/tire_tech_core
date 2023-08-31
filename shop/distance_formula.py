from math import sin, cos, sqrt, atan2, radians


def get_distance(from_long, from_lat, to_long, to_lat):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(from_lat)
    lon1 = radians(from_long)
    lat2 = radians(to_lat)
    lon2 = radians(to_long)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
