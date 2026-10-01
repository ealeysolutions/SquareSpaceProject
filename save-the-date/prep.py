"""Prepare the photo: cut out the couple, drop the hair beside the cap,
and replace the garage door with a soft blurred background.
usage: python3 prep.py <photo.jpg>   -> writes prepped.png + subject_mask.png"""
import sys, os
import numpy as np, cv2
from PIL import Image
from rembg import remove, new_session

D = os.path.dirname(os.path.abspath(__file__))
src = Image.open(sys.argv[1]).convert('RGB')
sw, sh = src.size
k = sw / 4000                                  # polygons were drawn on the 4000px export of DSCF6597
rgb = np.asarray(src).astype(np.float32)

mask = np.asarray(remove(src, session=new_session('u2net_human_seg'), only_mask=True)).astype(np.float32) / 255

# --- hair: dark, non-cap pixels inside a zone left of the cap/neck
zone = np.zeros((sh, sw), np.uint8)
poly = np.array([(1640, 1120), (1808, 1120), (1808, 1255), (1785, 1255), (1785, 1290), (1798, 1290), (1800, 1400),
                 (1820, 1410), (1822, 1540), (1640, 1545)], np.float32) * k
cv2.fillPoly(zone, [poly.astype(np.int32)], 1)
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
luma = 0.299 * r + 0.587 * g + 0.114 * b
cap = (luma > 200) | (b > r + 40)
# his left ear sits against her braids just left of the brim. No outline is drawn: the
# original pixels in a padded zone around the ear are kept untouched and fade out softly
# into the blurred background, so the ear is exactly as photographed.
ear = np.zeros((sh, sw), np.float32)
cv2.ellipse(ear, (int(1779 * k), int(1322 * k)), (int(27 * k), int(62 * k)), 10, 0, 360, 1, -1)
ear = cv2.GaussianBlur(ear, (0, 0), 5 * k)
hair = (zone > 0) & ~cap & (mask > 0.2)
hair = cv2.dilate(hair.astype(np.uint8), np.ones((5, 5), np.uint8))
hair = cv2.GaussianBlur(hair.astype(np.float32), (0, 0), 1.5 * k) * (1 - ear)
mask = np.clip(mask - hair, 0, 1)

# --- background plate: inpaint the people out at low res, then blur heavily
small = (500, round(500 * sh / sw))
hole = cv2.dilate((np.maximum(mask, hair) > 0.05).astype(np.uint8), np.ones((31, 31), np.uint8))
# studio watermark in the lower-left corner: fill it in too so it can't bleed into the blur
cv2.rectangle(hole, (int(150 * k), int(2420 * k)), (int(500 * k), int(2780 * k)), 1, -1)
bg_s = cv2.inpaint(cv2.resize(rgb.astype(np.uint8), small, interpolation=cv2.INTER_AREA),
                   cv2.resize(hole, small, interpolation=cv2.INTER_NEAREST), 15, cv2.INPAINT_TELEA)
bg_s = cv2.GaussianBlur(bg_s.astype(np.float32), (0, 0), 14)
bg = cv2.resize(bg_s, (sw, sh), interpolation=cv2.INTER_CUBIC)
bg += np.random.default_rng(1).normal(0, 1.2, bg.shape)   # light grain so the blur doesn't band in print

# --- ring: local sharpen + a little sparkle so the halo and pave survive the downscale
ring = np.zeros((sh, sw), np.float32)
cv2.ellipse(ring, (int(2068 * k), int(1824 * k)), (int(62 * k), int(40 * k)), -15, 0, 360, 1, -1)
ring = cv2.GaussianBlur(ring, (0, 0), 8 * k)[..., None]
soft = cv2.GaussianBlur(rgb, (0, 0), 1.2 * k)
sharp = np.clip(rgb + 1.4 * (rgb - soft), 0, 255)
lum = sharp.mean(axis=2, keepdims=True)
sparkle = np.clip(sharp + 0.25 * np.clip(lum - 150, 0, None), 0, 255)   # lift only the bright stones/metal
rgb = rgb * (1 - ring) + sparkle * ring

m = mask[..., None]
out = rgb * m + bg * (1 - m)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(D, 'prepped.png'))
Image.fromarray((mask * 255).astype(np.uint8)).save(os.path.join(D, 'subject_mask.png'))
print('prepped', sw, sh)
