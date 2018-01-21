

# requirements

py3exiv2 requirements:

    http://python3-exiv2.readthedocs.io/en/latest/developers.html

in my case thats
    
    sudo apt-get install libboost-python1.58.0 libboost-python-dev libexiv2-dev libexiv2-14

afterwards install the stuff in requirements.txt (maybe in a virtualenv)

    pip install -r requirements.txt


# usage

    $ python add_gpsinfo.py --help
    Usage: add_gpsinfo.py [OPTIONS]
    
    Options:
      --image PATH        image or folder with images
      --gpx PATH          gpx file
      --max-diff INTEGER  maximum difference from gpx timestamp to image time (in
                          seconds)
      --allow-overwrite   allow overwrite
      --help              Show this message and exit.

for example

    python add_gpsinfo.py --image path/to/image_folder --gpx path/to/gpx_file.gpx --max-diff 300
