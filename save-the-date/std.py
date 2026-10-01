"""Lay out the save-the-date on the prepped photo (run prep.py first).
usage: python3 std.py [prepped.png] [subject_mask.png]
Every text line is sized so it stays inside the shirt, with a margin."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
F = lambda n: os.path.join(D, 'fonts', n)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, 'prepped.png')
MASK = sys.argv[2] if len(sys.argv) > 2 else os.path.join(D, 'subject_mask.png')
OUT = os.path.join(D, 'out')

DPI = 300
TRIM_W, TRIM_H = 5 * DPI, 7 * DPI          # 5x7 in
BLEED = round(0.125 * DPI + 0.01)          # 1/8 in each side
W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
CENTER_X = None                            # subject centre as a fraction of source width (None = auto)
SHIRT_MARGIN = 0.09                        # keep text this fraction of shirt width in from each edge
INK = (28, 28, 30)

NAMES = "Lanny & Allison"
TOP, DATE, PLACE = "save the date", "4.30.27", "DURHAM, NC"

# --- crop photo + mask to the bleed canvas, full source height
src = Image.open(SRC).convert('RGB')
sw, sh = src.size
cw = round(sh * W / H)
_m = np.asarray(Image.open(MASK).convert('L')) > 128
if CENTER_X is None:                       # centre on the subject's columns
    cols = np.flatnonzero(_m[int(sh * 0.6):].any(axis=0))
    CENTER_X = (cols.min() + cols.max()) / 2 / sw
x0 = max(0, min(sw - cw, round(sw * CENTER_X - cw / 2)))
box = (x0, 0, x0 + cw, sh)
img = src.crop(box).resize((W, H), Image.LANCZOS)
img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=2))   # print output sharpening
mask = np.asarray(Image.open(MASK).convert('L').crop(box).resize((W, H), Image.BILINEAR)) > 128

def shirt_span(top, bottom):
    """Narrowest left/right shirt edge over rows top..bottom, minus margin."""
    L, R = 0, W
    for row in mask[int(top):int(bottom) + 1]:
        xs = np.flatnonzero(row)
        # ignore small specks (e.g. her hand at his waist): take the widest run around the centre
        c = W // 2
        l = c
        while l > 0 and row[l - 1]: l -= 1
        r = c
        while r < W - 1 and row[r + 1]: r += 1
        L, R = max(L, l), min(R, r)
    m = SHIRT_MARGIN * (R - L)
    return L + m, R - m

layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
y = lambda f: BLEED + f * TRIM_H
FEAT = ['lnum']

def measure(s, font, spacing):
    widths = [d.textlength(c, font=font, features=FEAT) for c in s]
    return widths, sum(widths) + spacing * (len(s) - 1)

# one shared centre line for the whole block: middle of the shirt across the text area
_L, _R = shirt_span(y(0.69), y(0.95))
CX = (_L + _R) / 2

def fits(width, top, bottom):
    L, R = shirt_span(top, bottom)
    return width / 2 <= min(CX - L, R - CX)

def text(s, fontfile, size, fy, spacing=0.0):
    """Draw centred on CX; shrink until it fits between the shirt edges."""
    while True:
        font = ImageFont.truetype(F(fontfile), int(size * TRIM_H))
        sp = spacing * TRIM_H
        widths, total = measure(s, font, sp)
        asc, desc = font.getmetrics()
        if fits(total, y(fy) - asc, y(fy) + desc) or size < 0.01:
            break
        size *= 0.97
    x = CX - total / 2
    for c, w in zip(s, widths):
        d.text((x, y(fy)), c, font=font, fill=INK, anchor='ls', features=FEAT)
        x += w + sp

cx = CX
text(TOP, 'cormorant-garamond-latin-500-normal.ttf', 0.040, 0.714, 0.004)

# divider with heart, also kept inside the shirt
ly = y(0.738)
L, R = shirt_span(ly - 10, ly + 10)
gap = 0.030 * TRIM_W
half = min(0.17 * TRIM_W, min(cx - L, R - cx) - gap)
lw = max(2, round(0.0015 * TRIM_H))
d.line((cx - gap - half, ly, cx - gap, ly), fill=INK, width=lw)
d.line((cx + gap, ly, cx + gap + half, ly), fill=INK, width=lw)
r = 0.0075 * TRIM_W
d.ellipse((cx - 2 * r, ly - 1.4 * r, cx, ly + 0.6 * r), fill=INK)
d.ellipse((cx, ly - 1.4 * r, cx + 2 * r, ly + 0.6 * r), fill=INK)
d.polygon([(cx - 1.95 * r, ly - 0.15 * r), (cx + 1.95 * r, ly - 0.15 * r), (cx, ly + 2.0 * r)], fill=INK)

text(NAMES, 'pinyon-script-latin-400-normal.ttf', 0.080, 0.822)
text(DATE, 'cormorant-garamond-latin-600-normal.ttf', 0.046, 0.900, 0.010)
text(PLACE, 'cormorant-garamond-latin-600-normal.ttf', 0.027, 0.942, 0.008)

# soft light halo behind the type so it reads on the shirt texture
halo = Image.new('L', (W, H), 0)
halo.paste(255, mask=layer.split()[3].filter(ImageFilter.MaxFilter(9)))
halo = halo.filter(ImageFilter.GaussianBlur(int(0.012 * TRIM_H))).point(lambda v: int(v * 0.35))
img = Image.composite(Image.new('RGB', (W, H), (250, 250, 250)), img, halo)
img.paste(layer, mask=layer.split()[3])

os.makedirs(OUT, exist_ok=True)
img.save(os.path.join(OUT, 'save-the-date_5x7_print_bleed.jpg'), quality=97, dpi=(DPI, DPI), subsampling=0)
img.save(os.path.join(OUT, 'save-the-date_5x7_print_bleed.pdf'), resolution=DPI)
trim = img.crop((BLEED, BLEED, W - BLEED, H - BLEED))
trim.save(os.path.join(OUT, 'save-the-date_5x7_print_trim.jpg'), quality=97, dpi=(DPI, DPI), subsampling=0)
trim.resize((1200, 1680), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=0.7, percent=45, threshold=2)).save(os.path.join(OUT, 'save-the-date_text-email.jpg'), quality=88, optimize=True, progressive=True)

# preview with trim (red), safe (blue) and shirt-edge (green) guides
pv = img.copy(); g = ImageDraw.Draw(pv)
g.rectangle((BLEED, BLEED, W - BLEED, H - BLEED), outline=(255, 0, 0), width=3)
s = BLEED + int(0.125 * DPI)
g.rectangle((s, s, W - s, H - s), outline=(0, 160, 255), width=2)
edge = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.FIND_EDGES)
pv.paste((0, 200, 0), mask=edge.filter(ImageFilter.MaxFilter(3)))
pv.resize((W // 2, H // 2)).save(os.path.join(OUT, 'preview_guides.jpg'), quality=85)
print('crop', x0, cw, 'of', sw, sh, 'scale', round(H / sh, 3))
