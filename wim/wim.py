#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from os.path import splitext
from PIL import Image, ImageDraw, ImageFont

MODE = 'RGBA'
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)


def add_text(img, font, fontsize, text):
    font = ImageFont.truetype(font, fontsize)
    text_width, text_height = font.getsize(text)
    text_img_height = int(text_height * 1.5)

    base_img = Image.new(MODE, (img.size[0], text_img_height + img.size[1]), BLACK)

    text_image = Image.new(MODE, (img.size[0], text_img_height), BLACK)
    draw = ImageDraw.Draw(text_image, MODE)

    # Center text on image.
    pos = ((text_image.size[0] - text_width) / 2, (text_image.size[1] - text_height) / 2)
    draw.text(pos, text, WHITE, font=font)

    base_img.paste(img, (0, 0))
    base_img.paste(text_image, (0, img.size[1]))

    return base_img


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

    if img.mode != MODE:
        img = img.convert(MODE)

    if text:
        img = add_text(img, font, fontsize, text)

    img.save(outfile)


if __name__ == '__main__':
    main()
