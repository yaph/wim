#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from os.path import splitext
from PIL import Image, ImageDraw, ImageFont


def add_text(img, font, fontsize, text):
    font = ImageFont.truetype(font, fontsize)
    text_width, text_height = font.getsize(text)
    draw = ImageDraw.Draw(img, 'RGBA')
    pos = ((img.size[0] - text_width) / 2, (img.size[1] - text_height))
    draw.text(pos, text, (0, 0, 0), font=font)


@click.command()
@click.option('--inplace', '-i', default=False, is_flag=True)
@click.option('--font', default='arial.ttf')
@click.option('--fontsize', default=16)
@click.option('--text', '-t')
@click.argument('filename')
def main(inplace, font, fontsize, text, filename):
    img = Image.open(filename)

    if inplace:
        outfile = filename
    else:
        # Insert .wim between file name and extension in the outfile name.
        parts = splitext(filename)
        outfile = parts[0] + '.wim' + parts[1]

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    if text:
        add_text(img, font, fontsize, text)

    img.save(outfile)


if __name__ == '__main__':
    main()
