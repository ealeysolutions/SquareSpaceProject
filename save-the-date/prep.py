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
k = sw / 2000                                  # hair polygon was drawn on a 2000px-wide frame
rgb = np.asarray(src).astype(np.float32)

mask = np.asarray(remove(src, session=new_session('u2net_human_seg'), only_mask=True)).astype(np.float32) / 255

# --- hair: dark, non-cap pixels inside a zone left of the cap/neck
zone = np.zeros((sh, sw), np.uint8)
poly = np.array([(828, 495), (906, 488), (907, 650),
                 (917, 652), (921, 722), (828, 722)], np.float32) * k
cv2.fillPoly(zone, [poly.astype(np.int32)], 1)
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
luma = 0.299 * r + 0.587 * g + 0.114 * b
cap = (luma > 150) | (b > r + 40)
hair = (zone > 0) & ~cap & (mask > 0.2)
hair = cv2.dilate(hair.astype(np.uint8), np.ones((5, 5), np.uint8))
hair = cv2.GaussianBlur(hair.astype(np.float32), (0, 0), 1.5 * k)
mask = np.clip(mask - hair, 0, 1)

# --- background plate: inpaint the people out at low res, then blur heavily
small = (500, round(500 * sh / sw))
hole = cv2.dilate((np.maximum(mask, hair) > 0.05).astype(np.uint8), np.ones((31, 31), np.uint8))
bg_s = cv2.inpaint(cv2.resize(rgb.astype(np.uint8), small, interpolation=cv2.INTER_AREA),
                   cv2.resize(hole, small, interpolation=cv2.INTER_NEAREST), 15, cv2.INPAINT_TELEA)
bg_s = cv2.GaussianBlur(bg_s.astype(np.float32), (0, 0), 14)
bg = cv2.resize(bg_s, (sw, sh), interpolation=cv2.INTER_CUBIC)
bg += np.random.default_rng(1).normal(0, 1.2, bg.shape)   # light grain so the blur doesn't band in print

m = mask[..., None]
out = rgb * m + bg * (1 - m)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(os.path.join(D, 'prepped.png'))
Image.fromarray((mask * 255).astype(np.uint8)).save(os.path.join(D, 'subject_mask.png'))
print('prepped', sw, sh)
