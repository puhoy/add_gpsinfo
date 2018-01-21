import click
import os

from gpsinfo.exif_image import ExifImage
from gpsinfo.gpx_coords import GPXCoords
from gpsinfo.google_json_coords import GoogleJSONCoords


def add_gpsdata(image_path, all_coords, max_diff, allow_overwrite):
    try:
        exif_image = ExifImage(image_path)
    except OSError as e:
        print(f'skipping {image_path} (could not load)')
        return

    if not exif_image.get_timestamp():
        print(f'skipping {image_path}: no timestamp found in exif data')
        return

    if not allow_overwrite:
        if exif_image.has_gps_data():
            print(f'image {image_path} has gps data. skipping.')
            return

    timestamp = exif_image.get_timestamp()
    coords = all_coords.get_coords_for_timestamp(timestamp, max_diff)

    if not coords:
        print(f'no matching coords found for {image_path} and max time diff {max_diff}s')
        return

    exif_image.set_gps_location(coords.lat, coords.lon)
    print(f'tagged {image_path} ({exif_image.get_datetime()}) with {coords.lat}, '
          f'{coords.lon} from gpx point @{coords.time}')


@click.command()
@click.option('--image', type=click.Path(exists=True), help='image or folder with images')
@click.option('--coords', type=click.Path(exists=True), help='gpx or (google-history-)json file')
@click.option('--max-diff', default=60 * 60, help='maximum difference from gpx timestamp to image time (in seconds)')
@click.option('--allow-overwrite', default=False, is_flag=True, help='allow overwrite')
def main(image, coords: str, max_diff, allow_overwrite):
    all_coords = []
    if coords.endswith('.json'):
        all_coords = GoogleJSONCoords(coords)
    elif coords.endswith('.gpx'):
        all_coords = GPXCoords(coords)
    else:
        print('is your coords file in the right format? (we need gpx or json)')
        exit(1)

    if os.path.isdir(image):
        image_folder = image
        for f in os.listdir(image_folder):
            image = os.path.join(image_folder, f)
            add_gpsdata(image, all_coords, max_diff, allow_overwrite)

    add_gpsdata(image, all_coords, max_diff, allow_overwrite)


if __name__ == '__main__':
    main()
