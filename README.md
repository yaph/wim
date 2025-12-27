# WIM - Web Image Maker

A command-line tool for creating and optimizing images for the web with text overlays, watermarks, and more.

## Installation

```bash
pipx install wim
```

Or install from source:

```bash
git clone https://github.com/yaph/wim.git
cd wim
pip install -e .
```

## Quick Start

```bash
# Add text overlay
wim input.jpg -t "Hello World"

# Add watermark
wim input.jpg -w logo.png

# Scale and add text
wim input.jpg -s 800 -t "Resized Image"

# Add semi-transparent watermark in top-right corner
wim photo.jpg -w logo.png --watermark-position top-right --watermark-opacity 128
```

## Features

### Text Overlays

- Add text with semi-transparent backgrounds
- Customize font, size, and position
- Automatic text centering and padding

### Watermarks & Overlays

- Blend images over your photos
- Adjust opacity for subtle watermarks
- Scale overlays to any size
- Position overlays anywhere (corners, center)

### Image Optimization

- Scale images to maximum dimensions
- Quantize to reduce file size
- Convert between formats (PNG, JPEG)
- Automatic RGBA to RGB conversion for JPEG

### Smart Defaults

- Non-destructive by default (adds `-wim` to file name stems)
- RGBA support with proper alpha blending
- High-quality image resampling

## Usage Examples

```bash
# Add text with custom font and size
wim input.jpg -t "Caption" --font times.ttf --font-size 24

# Add watermark with 50% opacity in bottom-right
wim photo.jpg -w logo.png --watermark-opacity 128

# Scale watermark to specific size
wim photo.jpg -w logo.png --watermark-scale 150 150

# Multiple operations at once
wim input.jpg -s 1200 -t "Summer 2024" -w logo.png --watermark-position top-right

# Edit image in place
wim input.jpg -i -t "Updated"

# Reduce file size with quantization
wim input.png -q
```

## Command Line Options

```bash
wim --help
```

<!-- START: DO NOT EDIT -->
```text
usage: wim [-h] [-i] [--font FONT] [--font-size FONT_SIZE] [--format {webp,jpg,jpeg,png,bmp}] [-q]
                             [-s WIDTH HEIGHT] [-t TEXT] [-w WATERMARK]
                             [--watermark-position {top-left,top-right,bottom-left,bottom-right,center}]
                             [--watermark-opacity WATERMARK_OPACITY] [--watermark-scale WIDTH HEIGHT]
                             filename

Add text and manipulate images.

positional arguments:
  filename              Input image filename

options:
  -h, --help            show this help message and exit
  -i, --inplace         Edit the image inplace, default is False.
  --font FONT           Set the font family, default is arial.ttf.
  --font-size FONT_SIZE
                        Set the font size, default is 16.
  --format {webp,jpg,jpeg,png,bmp}
                        Output format (overrides input format)
  -q, --quantize        Quantize the image to reduce its filesize, default is False.
  -s WIDTH HEIGHT, --scale WIDTH HEIGHT
                        Set the maximum width and height as integer values.
  -t TEXT, --text TEXT  Set the text to append at the bottom of the image.
  -w WATERMARK, --watermark WATERMARK
                        Path to watermark/overlay image to add to the image.
  --watermark-position {top-left,top-right,bottom-left,bottom-right,center}
                        Position of watermark (default: bottom-right).
  --watermark-opacity WATERMARK_OPACITY
                        Opacity of watermark 0-255 (default: 255).
  --watermark-scale WIDTH HEIGHT
                        Scale watermark to WIDTH HEIGHT in pixels.

```
<!-- END: DO NOT EDIT -->

## Requirements

- Python ≥ 3.10
- Pillow

## Development

```bash
# Clone repository
git clone https://github.com/yaph/wim.git
cd wim

# Run in development mode
hatch shell wim-dev

# Run tests
hatch run qa

# Clean build artifacts
hatch run clean
```

## License

MIT License - see LICENSE file for details

## Author

Ramiro Gómez ([@yaph](https://github.com/yaph))

## Links

- **Documentation**: https://github.com/yaph/wim#readme
- **Issues**: https://github.com/yaph/wim/issues
- **Source Code**: https://github.com/yaph/wim