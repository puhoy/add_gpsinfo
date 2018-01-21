import click
import os

from gpsinfo.exif_image import ExifImage
from gpsinfo.read_gpx import GPXCoords


def add_gpsdata(image_path, gpx_coords, max_diff, allow_overwrite):
    try:
        exif_image = ExifImage(image_path)
    except OSError as e:
        print(f'skipping {image_path} (could not load)')
        return

    if not exif_image.get_timestamp():
        print(f'skipping {image_path}: no timestamp found in exif data')
        return

    if not allow_overwrite or exif_image.has_gps_data():
        print(f'image {image_path} has gps data. skipping.')
        return

    timestamp = exif_image.get_timestamp()
    coords = gpx_coords.get_coords_for_timestamp(timestamp, max_diff)

    if not coords:
        print(f'no matching coords found for {image_path} and max time diff {max_diff}s')
        return

    exif_image.set_gps_location(coords.lat, coords.lon)
    print(f'tagged {image_path} ({exif_image.get_datetime()}) with {coords.lat}, '
          f'{coords.lon} from gpx point @{coords.time}')


@click.command()
@click.option('--image', type=click.Path(exists=True), help='image or folder with images')
@click.option('--gpx', type=click.Path(exists=True), help='gpx file')
@click.option('--max-diff', default=60 * 60, help='maximum difference from gpx timestamp to image time (in seconds)')
@click.option('--allow-overwrite', default=False, is_flag=True, help='allow overwrite')
def main(image, gpx, max_diff, allow_overwrite):
    gpx_coords = GPXCoords(gpx)

    if os.path.isdir(image):
        image_folder = image
        for f in os.listdir(image_folder):
            image = os.path.join(image_folder, f)
            add_gpsdata(image, gpx_coords, max_diff, allow_overwrite)

    add_gpsdata(image, gpx_coords, max_diff, allow_overwrite)


if __name__ == '__main__':
    main()
