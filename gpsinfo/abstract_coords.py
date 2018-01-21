import collections

from typing import Union

import gpxpy
import gpxpy.gpx

from .coords import Coords

class AbstractCoords:
    def __init__(self, gpx_path):
        self.coords = self.get_coords(gpx_path)
        self.timestamps = self.coords.keys()

    @staticmethod
    def get_coords(gpx_path: str) -> collections.OrderedDict:
        raise NotImplementedError

    def _get_closest_timestamp(self, timestamp, threshold) -> float:
        closest = False
        closest_diff = threshold + 1

        for ts in self.timestamps:
            diff = abs(ts - timestamp)
            if diff <= threshold:
                if diff < closest_diff:
                    closest = ts
                    closest_diff = diff

        return closest

    def get_coords_for_timestamp(self, timestamp, max_seconds_away) -> Union[bool, Coords]:
        closest = self._get_closest_timestamp(timestamp, max_seconds_away)
        if not closest:
            return False

        return self.coords[closest]
