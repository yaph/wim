from PIL import Image, ImageDraw, ImageFont

IMAGE_FORMATS = ['bmp', 'jpeg', 'jpg', 'png', 'webp']
MODE = 'RGBA'
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
FULL_OPACITY = 255


def calculate_position(base_size, overlay_size, position, padding):
    """
    Calculate the position for placing an overlay on a base image.

    Args:
        base_size: Tuple of (width, height) for the base image
        overlay_size: Tuple of (width, height) for the overlay
        position: One of 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'
        padding: Padding in pixels from the edges

    Returns:
        Tuple of (x, y) coordinates for the overlay position
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


def ensure_rgba(img):
    """Convert to RGBA if needed."""

    return img if img.mode == MODE else img.convert(MODE)


def add_text(img, font, font_size, text, bg_alpha=32, position='bottom-right', padding=0):
    """
    Add text with a semi-transparent background to an image.

    Args:
        img: PIL Image object
        font: Path to font file
        font_size: Size of the font
        text: Text to add
        bg_alpha: Alpha value for background (0-255, default 32)
        position: Position of text ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
        padding: Padding from edges in pixels

    Returns:
        PIL Image object with text added
    """

    font = ImageFont.truetype(font, font_size)
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
    text_y = y_pos + (text_img_height - text_height) / 2

    # Draw text with full opacity (alpha = 255)
    text_draw.text((text_x, text_y), text, WHITE, font=font)

    # Composite the text overlay
    return Image.alpha_composite(base_layer, text_overlay)


def add_image(img, overlay_path, position='bottom-right', padding=0, scale=None, opacity=FULL_OPACITY):
    """
    Blend an image over the base image.

    Args:
        img: PIL Image object (base image)
        overlay_path: Path to the overlay image file
        position: Position of overlay ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
        padding: Padding from edges in pixels
        scale: Scale overlay to this size (width, height) or None to keep original size
        opacity: Opacity of the overlay (0-255, default 255 for fully opaque)

    Returns:
        PIL Image object with overlay added
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


def set_background(img):
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
