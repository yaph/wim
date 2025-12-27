from PIL import Image, ImageFont, ImageDraw

import wim.image as image


class _FakeFont:
    """Wrap a PIL ImageFont and provide getbbox/getsize/getmask expected by wim.image.add_text."""
    def __init__(self, base_font):
        self.base = base_font

    def getbbox(self, text):
        # Prefer the font's own getbbox if available
        if hasattr(self.base, "getbbox"):
            bbox = self.base.getbbox(text)
            # Normalize to (left, top, right, bottom)
            return bbox
        # Fallback to drawing on a tiny canvas and using textbbox
        im = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(im)
        bbox = draw.textbbox((0, 0), text, font=self.base)
        return bbox

    def getsize(self, text):
        # Compute width/height using getbbox
        bbox = self.getbbox(text)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

    def getmask(self, *args, **kwargs):
        if hasattr(self.base, "getmask"):
            return self.base.getmask(*args, **kwargs)
        # Fallback: use ImageDraw to render into a mask
        size = self.getsize(args[0] if args else "")
        im = Image.new("L", size, 0)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), args[0] if args else "", fill=255, font=self.base)
        return im


def test_calculate_position():
    base = (100, 50)
    overlay = (20, 10)
    # top-left
    assert image.calculate_position(base, overlay, 'top-left', 5) == (5, 5)
    # top-right
    assert image.calculate_position(base, overlay, 'top-right', 5) == (100 - 20 - 5, 5)
    # bottom-left
    assert image.calculate_position(base, overlay, 'bottom-left', 3) == (3, 50 - 10 - 3)
    # bottom-right
    assert image.calculate_position(base, overlay, 'bottom-right', 0) == (100 - 20, 50 - 10)
    # center
    assert image.calculate_position((101, 51), (21, 11), 'center', 0) == ((101 - 21) // 2, (51 - 11) // 2)
    # unknown position falls back to bottom-right
    assert image.calculate_position(base, overlay, 'not-a-position', 2) == image.calculate_position(base, overlay, 'bottom-right', 2)


def test_ensure_rgba_converts_and_keeps_rgba():
    rgb = Image.new('RGB', (10, 10), (1, 2, 3))
    converted = image.ensure_rgba(rgb)
    assert converted.mode == 'RGBA'
    # If it's already RGBA, return unchanged (mode at least)
    rgba = Image.new('RGBA', (5, 5), (4, 5, 6, 255))
    returned = image.ensure_rgba(rgba)
    assert returned.mode == 'RGBA'


def test_add_text_changes_image(monkeypatch):
    # Create a simple base image (opaque white)
    base = Image.new('RGBA', (120, 40), (255, 255, 255, 255))

    # Create and store a real default font before monkeypatching to avoid recursion.
    stored_default_font = ImageFont.load_default()

    # Fake truetype that accepts extra kwargs (Pillow may pass layout_engine, etc.)
    def fake_truetype(path, size, *args, **kwargs):
        # Always return a wrapper around the stored default font.
        return _FakeFont(stored_default_font)

    # Monkeypatch the ImageFont.truetype used in the image module.
    monkeypatch.setattr(image, 'ImageFont', ImageFont, raising=False)
    monkeypatch.setattr(image.ImageFont, 'truetype', fake_truetype, raising=False)

    # Add text and assert resulting image differs from original bytes
    result = image.add_text(base, font='dummy.ttf', font_size=12, text='hello', bg_alpha=64, position='bottom-right', padding=2)
    assert isinstance(result, Image.Image)
    assert result.size == base.size
    assert result.mode == 'RGBA'
    # Ensure something changed in the image bytes (i.e., text/background was drawn)
    assert result.tobytes() != base.tobytes()


def test_add_image_pastes_and_respects_opacity(tmp_path):
    base = Image.new('RGBA', (50, 50), (255, 255, 255, 255))
    overlay = Image.new('RGBA', (10, 10), (255, 0, 0, 255))
    overlay_path = tmp_path / "overlay.png"
    overlay.save(overlay_path)

    # Paste with some padding at top-left and translucent opacity
    result = image.add_image(base, str(overlay_path), position='top-left', padding=5, opacity=128)
    assert isinstance(result, Image.Image)
    # Pixel at overlay top-left position should no longer be the original white
    px = result.getpixel((5, 5))
    assert px[:3] != (255, 255, 255)


def test_set_background_uses_black_and_preserves_opaque_pixels():
    # Create RGBA image with a single opaque white pixel and others transparent
    img = Image.new('RGBA', (2, 2), (0, 0, 0, 0))
    img.putpixel((0, 0), (255, 255, 255, 255))
    # Convert to RGB with black background
    rgb = image.set_background(img)
    assert rgb.mode == 'RGB'
    # The pixel that was opaque white should be white now
    assert rgb.getpixel((0, 0)) == (255, 255, 255)
    # Transparent pixels should become black
    assert rgb.getpixel((1, 1)) == (0, 0, 0)