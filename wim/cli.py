#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from PIL import Image, ImageOps

from wim.__about__ import __version__
from wim.image import (
    IMAGE_FORMATS,
    QUANTIZE_FORMATS,
    RGBA_FORMATS,
    add_image,
    add_text,
    get_metadata,
    get_quality,
    set_background,
)


def get_args(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Add text and manipulate images.')

    parser.add_argument(
        'filename', type=str, nargs='+', help='Input image filename. Use wildcard to process multiple files.'
    )
    parser.add_argument(
        '--font',
        help='Font name (e.g., DejaVuSans, Arial) or path to TrueType font file (.ttf). Falls back to system default if not specified or found.',
    )
    parser.add_argument('--font-size', type=int, help='Set the font size, requires font setting.')
    parser.add_argument(
        '--format',
        choices=IMAGE_FORMATS,
        help='Output format (overrides input format)',
    )
    parser.add_argument('--output-label', default='-wim', help='Label to append to the output file name.')
    parser.add_argument(
        '--quality', type=int, help='Output quality 1-100 (lower = smaller file). Works with JPEG and WebP.'
    )
    parser.add_argument('--quantize', type=int, help='Quantize the image with the desired number of colors, <= 256.')
    parser.add_argument(
        '-s',
        '--scale',
        type=int,
        nargs=2,
        metavar=('WIDTH', 'HEIGHT'),
        help='Set the maximum width and height as integer values.',
    )
    parser.add_argument('--strip', action='store_true', help='Strip image of all metadata.')
    parser.add_argument('-t', '--text', help='Set the text to append at the bottom of the image.')
    parser.add_argument('--trim', action='store_true', help='Trim uniform-color borders from image edges.')
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

    if argv.font_size and not argv.font:
        parser.error('--font-size requires --font to be specified')

    return argv


def get_dst(src: Path, argv: argparse.Namespace) -> Path:
    """Return destination path and ensure argv.format is set."""

    if argv.inplace:
        return src

    parent = Path(argv.outdir) if argv.outdir else src.parent
    parent.mkdir(exist_ok=True)
    argv.format = argv.format if argv.format else src.suffix.lstrip('.').lower()
    return parent / f'{src.stem}{argv.output_label}.{argv.format}'


def proc_image(img: Image.Image, argv: argparse.Namespace):
    # First make sure the image orientation is correct.
    img = ImageOps.exif_transpose(img)  # type: ignore

    # Extract metadata before further image processing.
    save_kwargs = {} if argv.strip else get_metadata(img)

    # Quality settings are applied when saving the image.
    if argv.quality:
        save_kwargs.update(get_quality(argv.quality, argv.format))

    # Apply trim before other image manipulations.
    if argv.trim:
        img = ImageOps.crop(img)

    if argv.quantize:
        if argv.format not in QUANTIZE_FORMATS:
            print(f'Skipping quantization, not supported for: {argv.format}')
        else:
            img = img.quantize(colors=argv.quantize)  # type: ignore

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

    # Turn into RGB with black background if necessary
    if img.mode == 'RGBA' and argv.format not in RGBA_FORMATS:
        img = set_background(img)

    return img, save_kwargs


def proc_file(name, argv: argparse.Namespace):
    img = Image.open(name)

    src = Path(name)
    # The stat call must take place before save because inplace edits modify the original image.
    stat = src.stat()
    dst = get_dst(src, argv)

    # Process and save image
    img, save_kwargs = proc_image(img, argv)
    print(f'Save image as: {dst}')
    img.save(dst, **save_kwargs)

    # Keep timestamps of original image.
    os.utime(dst, (stat.st_atime, stat.st_mtime))


def main(args=None) -> None:
    argv = get_args(args)
    for name in argv.filename:
        proc_file(name, argv)


if __name__ == '__main__':
    main()
