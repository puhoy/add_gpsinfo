import collections

import gpxpy
import gpxpy.gpx

from .abstract_coords import AbstractCoords
from .coords import Coords


class GPXCoords(AbstractCoords):

    @staticmethod
    def get_coords(gpx_path: str) -> collections.OrderedDict:
        points = collections.OrderedDict()

        with open(gpx_path, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points[point.time.timestamp()] = Coords(lat=point.latitude, lon=point.longitude,
                                                            elevation=point.elevation, time=point.time)

        return points
