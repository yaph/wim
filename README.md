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
usage: wim [-h] [-i | -o OUTDIR] [--strip] [--trim] [--version] [--format {ico,jpg,png,webp,jpeg,bmp,gif}]
                             [--output-label OUTPUT_LABEL] [--quality QUALITY] [--quantize QUANTIZE] [-s WIDTH HEIGHT]
                             [--font FONT] [--font-size FONT_SIZE] [-t TEXT] [-w WATERMARK]
                             [--watermark-opacity WATERMARK_OPACITY] [--watermark-scale WIDTH HEIGHT]
                             [--watermark-position {top-left,top-right,bottom-left,bottom-right,center}]
                             filename [filename ...]

Edit, optimize, and watermark images from the command line.

positional arguments:
  filename              Input image filename. Use wildcard to process multiple files.

options:
  -h, --help            show this help message and exit
  -i, --inplace         Edit the image in place (overwrites original).
  -o OUTDIR, --outdir OUTDIR
                        Output directory for processed images.
  --strip               Strip image of all metadata.
  --trim                Trim uniform-color borders from image edges.
  --version             show program's version number and exit
  --format {ico,jpg,png,webp,jpeg,bmp,gif}
                        Set the output format. If not set, original format is used.
  --output-label OUTPUT_LABEL
                        Label to append to the output file name. Ignored if --inplace is used.
  --quality QUALITY     Output quality 1-100 (lower = smaller file). Works with JPEG and WebP.
  --quantize QUANTIZE   Quantize the image with the desired number of colors, <= 256.
  -s WIDTH HEIGHT, --scale WIDTH HEIGHT
                        Set the maximum width and height as integer values.
  --font FONT           Font name (e.g., DejaVuSans, Arial) or path to TrueType font file (.ttf), requires font size setting.
                        Falls back to system default if not specified or found.
  --font-size FONT_SIZE
                        Set the font size, requires font setting.
  -t TEXT, --text TEXT  Set the text to add to the image.
  -w WATERMARK, --watermark WATERMARK
                        Path to watermark/overlay image to add to the image.
  --watermark-opacity WATERMARK_OPACITY
                        Opacity of watermark 0-255 (default: 255).
  --watermark-scale WIDTH HEIGHT
                        Scale watermark to WIDTH HEIGHT in pixels.
  --watermark-position {top-left,top-right,bottom-left,bottom-right,center}
                        Position of watermark (default: bottom-right).

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