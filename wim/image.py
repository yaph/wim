from PIL import Image, ImageDraw, ImageFont

"""
This module provides utility functions for image manipulation using the Python Imaging Library (PIL).
It includes functions for adding overlays, text, and metadata extraction, as well as image format
handling and quality optimization.

Functions:
    - add_image: Blend an overlay image onto a base image with customizable position, scale, and opacity.
    - add_text: Add text with a semi-transparent background to an image.
    - calculate_position: Calculate the position for placing an overlay on a base image.
    - ensure_rgba: Ensure an image is in RGBA mode.
    - get_metadata: Extract metadata from an image, including EXIF, ICC profile, and other common metadata.
    - get_quality: Generate quality and optimization options for saving images in specific formats.
    - load_font: Load a TrueType font with fallback to the default system font.
    - set_background: Convert an RGBA image to RGB mode with a black background.

Constants:
    - IMAGE_FORMATS: Supported image formats for processing.
    - QUALITY_FORMATS: Formats that support quality optimization.
    - QUANTIZE_FORMATS: Formats that support quantization.
    - OPTIMIZE_FORMATS: Formats that support optimization.
    - RGBA_FORMATS: Formats that support RGBA mode.
    - MODE: Default image mode ('RGBA').
    - BLACK: Black color in RGBA mode.
    - WHITE: White color in RGBA mode.
    - FULL_OPACITY: Maximum opacity value (255).
"""

IMAGE_FORMATS = {'bmp', 'gif', 'ico', 'jpeg', 'jpg', 'png', 'webp'}
QUALITY_FORMATS = {'jpeg', 'jpg', 'webp'}
QUANTIZE_FORMATS = {'png', 'gif'}
OPTIMIZE_FORMATS = {'png', 'gif'}
RGBA_FORMATS = {'png', 'webp', 'gif', 'ico'}

MODE = 'RGBA'
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
FULL_OPACITY = 255


def add_image(
    img: Image.Image,
    overlay_path: str,
    position: str = 'bottom-right',
    padding: int = 0,
    scale: tuple[int, int] | None = None,
    opacity: int = FULL_OPACITY,
):
    """
    Blend an overlay image onto a base image at a specified position with optional scaling, padding, and opacity.

    This function allows you to overlay an image onto a base image, with options to control the position, size, and transparency of the overlay. The resulting image is returned as a new PIL Image object.

    Args:
        img (PIL.Image.Image): The base image onto which the overlay will be added.
        overlay_path (str): The file path to the overlay image.
        position (str, optional): The position of the overlay on the base image.
            Options are 'top-left', 'top-right', 'bottom-left', 'bottom-right', and 'center'.
            Defaults to 'bottom-right'.
        padding (int, optional): The padding in pixels between the overlay and the edges of the base image.
            Defaults to 0.
        scale (tuple[int, int] or None, optional): The desired size (width, height) to scale the overlay image.
            If None, the overlay retains its original size. Defaults to None.
        opacity (int, optional): The opacity level of the overlay, ranging from 0 (completely transparent)
            to 255 (fully opaque). Defaults to FULL_OPACITY (255).

    Returns:
        PIL.Image.Image: A new image with the overlay blended onto the base image.
    """

    # Load and prepare overlay image
    overlay_img = ensure_rgba(Image.open(overlay_path))

    # Scale if requested
    if scale:
        overlay_img.thumbnail(scale)

    # Adjust opacity if needed
    if opacity < FULL_OPACITY:
        # Create a copy to avoid modifying the original
        overlay_img = overlay_img.copy()
        # Get alpha channel and adjust it
        alpha = overlay_img.getchannel('A')
        alpha = alpha.point(lambda x: int(x * opacity / FULL_OPACITY))
        overlay_img.putalpha(alpha)

    # Create a transparent canvas the same size as the base image
    canvas = Image.new(MODE, img.size, (0, 0, 0, 0))

    # Calculate position
    x_pos, y_pos = calculate_position(img.size, overlay_img.size, position, padding)

    # Paste overlay onto canvas
    canvas.paste(overlay_img, (x_pos, y_pos), overlay_img)

    # Composite with base image
    return Image.alpha_composite(ensure_rgba(img), canvas)


def add_text(
    img: Image.Image,
    font_name: str,
    font_size: int,
    text: str,
    bg_alpha: int = 32,
    position: str = 'bottom-right',
    padding: int = 0,
):
    """
    Adds text with a semi-transparent background to an image.

    Args:
        img (PIL.Image.Image): The base image to which the text will be added.
        font_name (str): Name of the font or path to the font file to be used for the text.
        font_size (int): Size of the font to be used.
        text (str): The text to be added to the image.
        bg_alpha (int, optional): Alpha value (transparency) for the background rectangle.
            Defaults to 32 (semi-transparent).
        position (str, optional): Position of the text on the image. Can be 'bottom-right',
            'bottom-left', 'top-right', 'top-left', or other custom positions. Defaults to 'bottom-right'.
        padding (int, optional): Padding around the text background rectangle. Defaults to 0.

    Returns:
        PIL.Image.Image: The image with the added text and background.
    """

    font = load_font(font_name, font_size)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_img_height = int(text_height * 1.5)
    text_img_width = int(text_width * 1.1)

    # Create a transparent overlay the same size as the base image
    base_overlay = Image.new(MODE, img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(base_overlay, MODE)

    # Calculate position
    x_pos, y_pos = calculate_position(img.size, (text_img_width, text_img_height), position, padding)

    # Draw semi-transparent background rectangle
    bg_color = (0, 0, 0, bg_alpha)
    draw.rectangle([(x_pos, y_pos), (x_pos + text_img_width, y_pos + text_img_height)], fill=bg_color)

    # Composite the semi-transparent background first
    base_layer = Image.alpha_composite(ensure_rgba(img), base_overlay)

    # Now draw the fully opaque text on a new overlay
    text_overlay = Image.new(MODE, img.size, (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_overlay, MODE)

    # Calculate centered text position
    text_x = x_pos + (text_img_width - text_width) / 2

    # Draw text with full opacity (alpha = 255)
    text_draw.text((text_x, y_pos), text, WHITE, font=font)

    # Composite the text overlay
    return Image.alpha_composite(base_layer, text_overlay)


def calculate_position(base_size: tuple, overlay_size: tuple, position: str, padding: int) -> tuple:
    """
    This function determines the (x, y) coordinates for positioning an overlay image
    on top of a base image, based on the specified position and padding.

    Args:
        base_size (tuple): A tuple (width, height) representing the dimensions of the base image.
        overlay_size (tuple): A tuple (width, height) representing the dimensions of the overlay image.
        position (str): A string specifying the desired position of the overlay.
            Options include:
            - 'top-left': Places the overlay at the top-left corner.
            - 'top-right': Places the overlay at the top-right corner.
            - 'bottom-left': Places the overlay at the bottom-left corner.
            - 'bottom-right': Places the overlay at the bottom-right corner.
            - 'center': Places the overlay at the center of the base image.
        padding (int): The number of pixels to pad from the edges of the base image.

    Returns:
        tuple: A tuple (x, y) representing the calculated coordinates for the overlay position.
        If the specified position is invalid, defaults to 'bottom-right'.
    """
    base_width, base_height = base_size
    overlay_width, overlay_height = overlay_size

    positions = {
        'top-left': (padding, padding),
        'top-right': (base_width - overlay_width - padding, padding),
        'bottom-left': (padding, base_height - overlay_height - padding),
        'bottom-right': (base_width - overlay_width - padding, base_height - overlay_height - padding),
        'center': ((base_width - overlay_width) // 2, (base_height - overlay_height) // 2),
    }

    return positions.get(position, positions['bottom-right'])


def ensure_rgba(img: Image.Image) -> Image.Image:
    """Ensure the image is in RGBA mode."""

    return img if img.mode == MODE else img.convert(MODE)


def get_metadata(img: Image.Image) -> dict:
    """Extract metadata from an image.

    Args:
        img: PIL Image object

    Returns:
        dict: Metadata dictionary
    """
    metadata: dict = {}

    if not hasattr(img, 'info'):
        return metadata

    info = img.info

    # EXIF data (JPEG) - contains GPS, camera info, etc.
    if 'exif' in info:
        metadata['exif'] = info['exif']

    # ICC color profile
    if 'icc_profile' in info:
        metadata['icc_profile'] = info['icc_profile']

    # DPI/resolution
    if 'dpi' in info:
        metadata['dpi'] = info['dpi']

    # PNG metadata
    if 'transparency' in info:
        metadata['transparency'] = info['transparency']

    # Other common metadata
    for key in ['gamma', 'chromaticity', 'photoshop', 'iptc']:
        if key in info:
            metadata[key] = info[key]

    return metadata


def get_quality(quality: int, img_format: str) -> dict:
    """
    Generate image processing options based on the provided quality and format.

    Args:
        quality (int): The quality level for the image (used for formats that support it).
        img_format (str): The format of the image (e.g., 'jpeg', 'png', 'gif').

    Returns:
        dict: A dictionary containing options for image processing. This may include:
            - 'quality': The quality level (if applicable to the format).
            - 'optimize': A boolean indicating whether optimization is enabled.
            - 'compress_level': The compression level (only for PNG format).
    """

    options = {}

    if img_format in QUALITY_FORMATS:
        options['quality'] = quality
        options['optimize'] = True
    elif img_format in OPTIMIZE_FORMATS:
        # PNG and GIF don't use quality parameter, but support optimization
        options['optimize'] = True
        if img_format == 'png':
            options['compress_level'] = 9

    return options


def load_font(font_path: str, font_size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """
    Load a TrueType font with fallback to default font.

    Args:
        font_path: Path to TrueType font file or None
        font_size: Size of the font (ignored for default font)

    Returns:
        ImageFont object
    """
    # If no font path provided, use default immediately
    if font_path is None:
        print('Using system default font.')
        return ImageFont.load_default(size=font_size)

    try:
        return ImageFont.truetype(font_path, font_size)
    except (OSError, PermissionError) as e:
        print(f"Warning: Could not load font '{font_path}': {e}")
        print('Falling back to system default font')
        return ImageFont.load_default()


def set_background(img: Image.Image) -> Image.Image:
    """
    Convert RGBA image to RGB with black background.

    Args:
        img: PIL Image object in RGBA mode

    Returns:
        PIL Image object in RGB mode
    """
    rgb_img = Image.new('RGB', img.size, BLACK)
    rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
    return rgb_img
