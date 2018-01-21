import collections

from typing import Union

import gpxpy
import gpxpy.gpx

Coords = collections.namedtuple('Coords', ['lat', 'lon', 'elevation', 'time'])

class GPXCoords:
    def __init__(self, gpx_path):
        self.coords = GPXCoords.get_coords(gpx_path)
        self.timestamps = self.coords.keys()

    @staticmethod
    def get_coords(gpx_path: str) -> collections.OrderedDict:
        points = collections.OrderedDict()

        with open(gpx_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points[point.time.timestamp()] = Coords(lat=point.latitude, lon=point.longitude, elevation=point.elevation, time=point.time)

        return points

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
