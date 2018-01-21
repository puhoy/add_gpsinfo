import collections
import json
import math
import datetime

from .abstract_coords import AbstractCoords
from .coords import Coords

class GoogleJSONCoords(AbstractCoords):
    """
    reads your google location history
    get here https://takeout.google.com/settings/takeout/custom/location_history
    """

    coord_exp = math.pow(10, 7)

    @staticmethod
    def get_coords(json_path: str) -> collections.OrderedDict:
        points = collections.OrderedDict()

        with open(json_path, 'r') as f:
            points_json = json.load(f)

        for point in points_json['locations']:

            ts = int(point['timestampMs'][:10])
            lat = point['latitudeE7'] / GoogleJSONCoords.coord_exp
            lon = point['longitudeE7'] / GoogleJSONCoords.coord_exp
            alt = point.get('altitude', 0)
            dt = datetime.datetime.fromtimestamp(ts)
            points[ts] = Coords(lat=lat, lon=lon, elevation=alt, time=dt)

        return points
