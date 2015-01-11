# -*- coding: utf-8 -*-
import click

from PIL import Image, ImageDraw, ImageFont, ImageEnhance


@click.command()
@click.argument('filename')
@click.argument('text')
def main(filename, text):
    ttf = 'arial.ttf'
    opacity = 0.50
    size = 40

    im = Image.open(filename)
    outfile = filename + '.jpg'

    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    watermark = Image.new('RGBA', im.size, (0, 0, 0, 0))

    font = ImageFont.truetype(ttf, size)
    text_width, text_height = font.getsize(text)

    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - text_width) / 2,
              (watermark.size[1] - text_height)),
              text, font=font)

    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)

    try:
        Image.composite(watermark, im, watermark).save(outfile)
    except IOError:
        print('Cannot add watermark to image: ', filename)


if __name__ == '__main__':
    main()
