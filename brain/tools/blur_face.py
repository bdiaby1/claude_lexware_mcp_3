#!/usr/bin/env python3
"""Documentary-style face anonymisation on a full-resolution still (apply on the 4K SOURCE, before cropping).

  python3 blur_face.py in.png out.png --ellipse CX CY RX RY [--mode blur|mosaic] [--sigma 14]
          [--feather 6] [--block 8] [--grain-patch X0 Y0 X1 Y1] [--grain-sd N] [--seed 11]

Default = what documentaries do: a feathered, head-shaped ellipse with a heavy smooth Gaussian blur
(sigma ~ 14 % of the head width) so the head silhouette stays but no feature survives, plus film grain
matched to the surroundings so the patch is not "cleaner" than the rest. --mode mosaic = fine pixels
(block 8 px at 4K); it reads as a censor box and its blocks mix in background — second choice.
Find the ellipse by cropping the area with a coordinate grid and viewing a gamma-lifted copy.
Needs python3 with numpy + opencv-python-headless (run with -I when the input is untrusted).
His rule (Istanbul brief, Görli): blur faces of anyone who did not consent or asked for it (MEMORY §6).
"""
import argparse, sys
import cv2, numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--ellipse", nargs=4, type=int, required=True, metavar=("CX", "CY", "RX", "RY"))
ap.add_argument("--mode", choices=("blur", "mosaic"), default="blur")
ap.add_argument("--sigma", type=float, default=14.0); ap.add_argument("--feather", type=float, default=6.0)
ap.add_argument("--block", type=int, default=8)
ap.add_argument("--grain-patch", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
ap.add_argument("--grain-sd", type=float); ap.add_argument("--seed", type=int, default=11)
a = ap.parse_args()

img = cv2.imread(a.src)
if img is None: sys.exit("cannot read " + a.src)
h, w = img.shape[:2]; cx, cy, rx, ry = a.ellipse
m = np.zeros((h, w), np.float32); cv2.ellipse(m, (cx, cy), (rx, ry), 0, 0, 360, 1.0, -1)
m = cv2.GaussianBlur(m, (0, 0), a.feather if a.mode == "blur" else 3)[..., None]
if a.mode == "blur":
    if a.grain_sd is not None: sd = a.grain_sd
    elif a.grain_patch:
        x0, y0, x1, y1 = a.grain_patch; ref = img[y0:y1, x0:x1].astype(np.float32)
        sd = float((ref - cv2.GaussianBlur(ref, (0, 0), 2.0)).std())
    else:   # auto: robust noise estimate from a ring around the head
        yy, xx = np.ogrid[:h, :w]; d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        ring = img[(d > 2.0) & (d < 4.0)].astype(np.float32).reshape(-1, 3)
        sd = float(np.median(np.abs(ring - np.median(ring, axis=0))) * 1.4826 * 0.5)
    noise = np.random.default_rng(a.seed).normal(0, sd, img.shape).astype(np.float32)
    fx = cv2.GaussianBlur(img, (0, 0), a.sigma).astype(np.float32) + noise
else:
    small = cv2.resize(img, (w // a.block, h // a.block), interpolation=cv2.INTER_AREA)
    fx = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST).astype(np.float32)
out = np.clip(img * (1 - m) + fx * m, 0, 255).astype(np.uint8)
cv2.imwrite(a.dst, out)
print(f"{a.mode}: ellipse {2*rx}x{2*ry}px at ({cx},{cy})" + (f", grain sd {sd:.2f}" if a.mode == "blur" else f", block {a.block}px"))
