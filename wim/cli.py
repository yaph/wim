#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from PIL import Image, ImageOps

from wim.image import IMAGE_FORMATS, add_image, add_text, get_metadata, set_background
from wim.__about__ import __version__


def get_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Add text and manipulate images.')

    parser.add_argument(
        'filename', type=str, nargs='+', help='Input image filename. Use wildcard to process multiple files.'
    )
    parser.add_argument('--font', help='Path to TrueType font file. If not specified, uses system default font.')
    parser.add_argument('--font-size', type=int, default=16, help='Set the font size, default is 16.')
    parser.add_argument(
        '--format',
        choices=IMAGE_FORMATS,
        help='Output format (overrides input format)',
    )
    parser.add_argument(
        '-q', '--quantize', action='store_true', help='Quantize the image to reduce its filesize, default is False.'
    )
    parser.add_argument(
        '-s',
        '--scale',
        type=int,
        nargs=2,
        metavar=('WIDTH', 'HEIGHT'),
        help='Set the maximum width and height as integer values.',
    )
    parser.add_argument('-t', '--text', help='Set the text to append at the bottom of the image.')
    parser.add_argument('-w', '--watermark', help='Path to watermark/overlay image to add to the image.')
    parser.add_argument(
        '--watermark-position',
        default='bottom-right',
        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
        help='Position of watermark (default: bottom-right).',
    )
    parser.add_argument('--watermark-opacity', type=int, default=255, help='Opacity of watermark 0-255 (default: 255).')
    parser.add_argument(
        '--watermark-scale',
        type=int,
        nargs=2,
        metavar=('WIDTH', 'HEIGHT'),
        help='Scale watermark to WIDTH HEIGHT in pixels.',
    )
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        '-i', '--inplace', action='store_true', help='Edit the image in place (overwrites original).'
    )
    output_group.add_argument('-o', '--outdir', help='Output directory for processed images.')
    argv = parser.parse_args(args)

    if argv.inplace and argv.format:
        parser.error('--format cannot be used with --inplace (inplace preserves original format)')

    return argv


def get_dst(src: Path, argv: argparse.Namespace) -> Path:
    """Return destination path."""

    if argv.inplace:
        return src

    parent = Path(argv.outdir) if argv.outdir else src.parent
    parent.mkdir(exist_ok=True)
    suffix = argv.format if argv.format else src.suffix.lstrip('.')
    return parent / f'{src.stem}-wim.{suffix}'


def main(args=None) -> None:
    argv = get_args(args)

    for name in argv.filename:
        img = Image.open(name)
        img_format = img.format

        src = Path(name)
        dst = get_dst(src, argv)

        # First make sure the image orientation is correct.
        img = ImageOps.exif_transpose(img)  # type: ignore

        # Extract metadata before further image processing
        metadata = get_metadata(img)

        if argv.quantize:
            img = img.quantize()  # type: ignore

        if argv.scale:
            img.thumbnail(argv.scale)

        if argv.text:
            img = add_text(img, argv.font, argv.font_size, argv.text)

        if argv.watermark:
            img = add_image(
                img,
                argv.watermark,
                position=argv.watermark_position,
                scale=argv.watermark_scale,
                opacity=argv.watermark_opacity,
            )

        # Convert RGBA to RGB for JPEG files
        if img_format == 'JPEG' and img.mode == 'RGBA':
            img = set_background(img)

        # The stat call must take place before save because inplace edits modify the original image.
        stat = src.stat()

        print(f'Save image as: {dst}')
        # Add back original metadata when saving image
        img.save(dst, **metadata)

        # Keep timestamps of original image.
        os.utime(dst, (stat.st_atime, stat.st_mtime))


if __name__ == '__main__':
    main()
