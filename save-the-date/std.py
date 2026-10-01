import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
F = lambda n: os.path.join(D, 'fonts', n)
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, '..', 'images', '1.jpg')
OUT = os.path.join(D, 'out')

DPI = 300
TRIM_W, TRIM_H = 5 * DPI, 7 * DPI          # 5x7 in
BLEED = round(0.125 * DPI + 0.01)                   # 1/8 in each side
W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
CENTER_X = 0.505                           # subject centre as a fraction of source width
INK = (28, 28, 30)

NAMES = "Lanny & Allison"
LINES = dict(top="save the date", date="4 . 30 . 27", place="DURHAM, NC")

# --- crop the photo to the bleed canvas, full source height
src = Image.open(SRC).convert('RGB')
sw, sh = src.size
cw = round(sh * W / H)
x0 = max(0, min(sw - cw, round(sw * CENTER_X - cw / 2)))
img = src.crop((x0, 0, x0 + cw, sh)).resize((W, H), Image.LANCZOS)

# --- text layer (positions are fractions of trim height, measured from trim top)
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
cx = W / 2
y = lambda f: BLEED + f * TRIM_H

def text(s, font, fy, spacing=0):
    if spacing:
        widths = [d.textlength(c, font=font, features=['lnum']) for c in s]
        total = sum(widths) + spacing * (len(s) - 1)
        x = cx - total / 2
        for c, w in zip(s, widths):
            d.text((x, y(fy)), c, font=font, fill=INK, anchor='ls', features=['lnum'])
            x += w + spacing
    else:
        d.text((cx, y(fy)), s, font=font, fill=INK, anchor='ms')

serif = ImageFont.truetype(F('cormorant-garamond-latin-500-normal.ttf'), int(0.040 * TRIM_H))
serif_b = ImageFont.truetype(F('cormorant-garamond-latin-600-normal.ttf'), int(0.046 * TRIM_H))
caps = ImageFont.truetype(F('cormorant-garamond-latin-600-normal.ttf'), int(0.027 * TRIM_H))
script = ImageFont.truetype(F('pinyon-script-latin-400-normal.ttf'), int(0.080 * TRIM_H))

text(LINES['top'], serif, 0.714, spacing=0.004 * TRIM_H)
# divider with heart
ly, gap, half = y(0.738), 0.030 * TRIM_W, 0.20 * TRIM_W
lw = max(2, round(0.0015 * TRIM_H))
d.line((cx - gap - half, ly, cx - gap, ly), fill=INK, width=lw)
d.line((cx + gap, ly, cx + gap + half, ly), fill=INK, width=lw)
r = 0.0075 * TRIM_W
d.ellipse((cx - 2 * r, ly - 1.4 * r, cx, ly + 0.6 * r), fill=INK)
d.ellipse((cx, ly - 1.4 * r, cx + 2 * r, ly + 0.6 * r), fill=INK)
d.polygon([(cx - 1.95 * r, ly - 0.15 * r), (cx + 1.95 * r, ly - 0.15 * r), (cx, ly + 2.0 * r)], fill=INK)
text(NAMES, script, 0.822)
text(LINES['date'].replace(' ', ''), serif_b, 0.900, spacing=0.010 * TRIM_H)
text(LINES['place'], caps, 0.942, spacing=0.008 * TRIM_H)

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
trim.resize((1200, 1680), Image.LANCZOS).save(os.path.join(OUT, 'save-the-date_text-email.jpg'), quality=88, optimize=True, progressive=True)
# preview with trim + safe guides
pv = img.copy(); g = ImageDraw.Draw(pv)
g.rectangle((BLEED, BLEED, W - BLEED, H - BLEED), outline=(255, 0, 0), width=3)
s = BLEED + int(0.125 * DPI)
g.rectangle((s, s, W - s, H - s), outline=(0, 160, 255), width=2)
pv.resize((W // 2, H // 2)).save(os.path.join(OUT, 'preview_guides.jpg'), quality=85)
print('crop', x0, cw, 'of', sw, sh, 'scale', H / sh)
