import pyexiv2
import fractions


class ExifImage:
    def __init__(self, filename):
        self.filename = filename
        self.exiv_image = pyexiv2.ImageMetadata(self.filename)
        self.exiv_image.read()

    def _to_deg(self, value, loc):
        # see https://gist.github.com/maxim75/985060
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg = int(abs_value)
        t1 = (abs_value - deg) * 60
        min = int(t1)
        sec = int((t1 - min) * 60)
        return (deg, min, sec, loc_value)

    def has_gps_data(self):
        for tag in ["Exif.GPSInfo.GPSLatitude", "Exif.GPSInfo.GPSLatitudeRef", "Exif.GPSInfo.GPSLongitude",
                    "Exif.GPSInfo.GPSLongitudeRef"]:
            if tag in self.exiv_image.keys() and self.exiv_image.get(tag, '') is not '':
                return True
        return False

    def get_timestamp(self):
        if not self.get_datetime():
            return False
        return self.get_datetime().timestamp()

    def get_datetime(self):
        date = self.exiv_image.get('Exif.Image.DateTime', False)
        if not date:
            return False

        return date.value

    def set_gps_location(self, lat, lng):
        """
        adapted from https://gist.github.com/maxim75/985060

        Adds GPS position as EXIF metadata
        Keyword arguments:
        file_name -- image file
        lat -- latitude (as float)
        lng -- longitude (as float)
        """

        lat_deg = self._to_deg(lat, ["S", "N"])
        lng_deg = self._to_deg(lng, ["W", "E"])

        # convert decimal coordinates into degrees, minutes and seconds

        exiv_lat = [fractions.Fraction(lat_deg[0] * 60 + lat_deg[1], 60), fractions.Fraction(lat_deg[2] * 100, 6000),
                    fractions.Fraction(0, 1)]
        exiv_lng = [fractions.Fraction(lng_deg[0] * 60 + lng_deg[1], 60), fractions.Fraction(lng_deg[2] * 100, 6000),
                    fractions.Fraction(0, 1)]

        self.exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
        self.exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
        self.exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
        self.exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]

        self.exiv_image["Exif.Image.GPSTag"] = 654
        self.exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
        self.exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'
        self.exiv_image.write()
        return True
