#!/usr/bin/env python
import argparse
import os
from pathlib import Path

from PIL import Image

from wim.image import IMAGE_FORMATS, add_image, add_text, auto_orient, set_background


def main(args=None) -> None:
    parser = argparse.ArgumentParser(description='Add text and manipulate images.')

    parser.add_argument(
        'filename', type=str, nargs='+', help='Input image filename. Use wildcard to process multiple files.'
    )
    parser.add_argument('--font', default='arial.ttf', help='Set the font family, default is arial.ttf.')
    parser.add_argument('--font-size', type=int, default=16, help='Set the font size, default is 16.')
    parser.add_argument(
        '--format',
        default='webp',
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

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        '-i', '--inplace', action='store_true', help='Edit the image in place (overwrites original).'
    )
    output_group.add_argument('-o', '--outdir', help='Output directory for processed images.')

    argv = parser.parse_args(args)

    if argv.inplace and argv.format:
        parser.error('--format cannot be used with --inplace (inplace preserves original format)')

    for name in argv.filename:
        img = Image.open(name)
        p_src = Path(name)

        # Set destination path
        parent = Path(argv.outdir) if argv.outdir else p_src.parent
        parent.mkdir(exist_ok=True)
        p_dst = p_src if argv.inplace else parent / f'{p_src.stem}-wim.{argv.format}'

        if argv.quantize:
            img = img.quantize()  # type: ignore

        if argv.scale:
            img.thumbnail(argv.scale)

        # Make sure the image orientation is correct when adding text or images.
        # This must happen after scaling the image.
        if argv.text or argv.watermark:
            img = auto_orient(img)

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
        if p_dst.suffix.lower() in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
            img = set_background(img)

        # Keep timestamps of original image. The stat call must take place before save because of possible inplace edits.
        stat = p_src.stat()
        img.save(p_dst)
        os.utime(p_dst, (stat.st_atime, stat.st_mtime))


if __name__ == '__main__':
    main()
