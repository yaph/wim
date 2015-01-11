# -*- coding: utf-8 -*-
import click

from os.path import splitext
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


@click.command()
@click.option('--inplace', '-i', default=False, is_flag=True)
@click.option('--fontsize', default=12)
@click.option('--text', '-t')
@click.argument('filename')
def main(inplace, fontsize, text, filename):
    ttf = 'arial.ttf'
    opacity = 0.50

    im = Image.open(filename)

    if inplace:
        outfile = filename
    else:
        # Insert .wim between file name and extension in the outfile name.
        parts = splitext(filename)
        outfile = parts[0] + '.wim' + parts[1]

    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    watermark = Image.new('RGBA', im.size, (0, 0, 0, 0))

    font = ImageFont.truetype(ttf, fontsize)
    text_width, text_height = font.getsize(text)

    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - text_width) / 2,
              (watermark.size[1] - text_height)),
              text, font=font)

    # alpha = watermark.split()[3]
    # alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    # watermark.putalpha(alpha)

    try:
        Image.composite(watermark, im, watermark).save(outfile)
    except IOError:
        print('Cannot add watermark to image: ', filename)


if __name__ == '__main__':
    main()
