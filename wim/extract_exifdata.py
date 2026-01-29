#!/usr/bin/env python
import argparse
import json
from pathlib import Path

import PIL.ExifTags
from PIL import Image


def convert_exif_value(v):
    """Convert EXIF value to JSON-serializable type"""
    if isinstance(v, PIL.TiffImagePlugin.IFDRational):
        return float(v)
    if isinstance(v, bytes):
        return v.decode('utf-8', errors='ignore').strip('\x00')
    if isinstance(v, tuple):
        return [convert_exif_value(x) for x in v]
    if isinstance(v, dict):
        return {k: convert_exif_value(val) for k, val in v.items()}
    if isinstance(v, int | float | str):
        return v
    return str(v)


def convert_gps_to_decimal(gps_info):
    """Convert GPS info from PIL/EXIF format to decimal degrees"""

    # Extract latitude
    lat_deg, lat_min, lat_sec = gps_info[2]
    latitude = lat_deg + (lat_min / 60.0) + (lat_sec / 3600.0)
    if gps_info[1] == 'S':
        latitude = -latitude

    # Extract longitude
    lon_deg, lon_min, lon_sec = gps_info[4]
    longitude = lon_deg + (lon_min / 60.0) + (lon_sec / 3600.0)
    if gps_info[3] == 'W':
        longitude = -longitude

    # Extract altitude (already in decimal format)
    altitude = gps_info[6]

    return {'latitude': latitude, 'longitude': longitude, 'altitude': altitude}


def main():
    parser = argparse.ArgumentParser(description='Extract exif data from images.')
    parser.add_argument(
        'filename', type=str, nargs='+', help='Input image filename. Use wildcard to process multiple files.'
    )
    parser.add_argument('--convert-gps', action='store_true', help='Convert GPS info to decimal degrees.')
    argv = parser.parse_args()

    for filename in argv.filename:
        img = Image.open(filename)
        if not (exif_data := img._getexif()):  # noqa: SLF001
            print(f'No EXIF data found in {filename}')
            continue
        exif = {PIL.ExifTags.TAGS.get(k, k): convert_exif_value(v) for k, v in exif_data.items()}
        if argv.convert_gps and 'GPSInfo' in exif:
            exif['GPSInfo'] = convert_gps_to_decimal(exif['GPSInfo'])
        data_file = Path(filename).with_suffix('.exif.json')
        print(f'Saving EXIF data to {data_file}')
        data_file.write_text(json.dumps(exif))


if __name__ == '__main__':
    main()
