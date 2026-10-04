"""Re-crop an approved 5x7 save-the-date to 4x6 for print.
usage: python3 to4x6.py <approved_5x7.jpg> [out_prefix]
Writes <prefix>_4x6_bleed.jpg/.pdf (4.25x6.25 in) and <prefix>_4x6_trim.jpg (4x6 in), 300 DPI,
plus <prefix>_4x6_guides.jpg showing trim (red) and 1/8 in safe zone (blue).
5x7 is wider than 4x6, so the sides are trimmed and nothing is stretched."""
import sys, os
from PIL import Image, ImageDraw, ImageFilter

DPI = 300
TRIM_W, TRIM_H = 4 * DPI, 6 * DPI
BLEED = round(0.125 * DPI + 0.01)
W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED

src = Image.open(sys.argv[1]).convert('RGB')
prefix = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(sys.argv[1])[0]
sw, sh = src.size
scale = H / sh                                 # fill the bleed canvas top to bottom
img = src.resize((round(sw * scale), H), Image.LANCZOS)
x0 = (img.width - W) // 2
assert x0 >= 0, 'source is narrower than 4x6 proportions'
img = img.crop((x0, 0, x0 + W, H))
if scale < 1:                                  # light re-sharpen after downsizing
    img = img.filter(ImageFilter.UnsharpMask(radius=0.8, percent=40, threshold=2))

img.save(prefix + '_4x6_bleed.jpg', quality=97, dpi=(DPI, DPI), subsampling=0)
img.save(prefix + '_4x6_bleed.pdf', resolution=DPI)
img.crop((BLEED, BLEED, W - BLEED, H - BLEED)).save(prefix + '_4x6_trim.jpg', quality=97, dpi=(DPI, DPI), subsampling=0)
g = img.copy(); d = ImageDraw.Draw(g)
d.rectangle((BLEED, BLEED, W - BLEED, H - BLEED), outline=(255, 0, 0), width=3)
s = BLEED + int(0.125 * DPI)
d.rectangle((s, s, W - s, H - s), outline=(0, 160, 255), width=2)
g.resize((W // 2, H // 2)).save(prefix + '_4x6_guides.jpg', quality=85)
print('source', sw, sh, 'scale', round(scale, 3), 'effective dpi', round(sh / 6.25))
