# IG POST — "What if the G-Class is not mine?" — split carousel (status 30 Oct 2026)

Form (his idea): each slide = ONE split image, luxury on top / human underneath, 4:5 = 1080×1350.
Caption: FINAL in `../shorts-from-archive/what_if_reel_caption.md` (his typed voice).

## Decisions (his, 30 Oct) + mine
- **NO divider bar** (his call: "weg sieht besser aus"). Both seams already have a hard tonal break
  (bright street → night; warm marble → cold concrete); a bar only costs pixels. Panels = 1080×675.
- **Order: luxury top, human bottom** (he was unsure). Reasons: first look = like-magnet, last look =
  the brand (MEMORY §10); bottom = the floor, light-above-dark is tonally stable; the caption's
  "the man you look down on is better than you" then flips the viewer's own habit. Flip = swap the two args.
- **As much picture as possible**: full-height crops, aspect 1.6 (≈90 % of a 16:9 width), him in the
  SAME horizontal spot top and bottom (the "same man, two worlds" rhyme). Sharpen 0.7 (he liked it).

| slide | top | bottom | source | status |
|---|---|---|---|---|
| 1 | G-Klasse/Rolex street, Berlin | him pulling Tahsin's cart, Kadıköy night | **4K originals from his ZIP** (`1030(19).png` = o3, `1030 (1)(7).png` = o2) | **DONE** `slide1_gklasse_over_cart_FINAL…jpg` |
| 2 | Waldorf marble bath, teacup toast | Istanbul floor, heart blanket | chat copies 2000 px (soft) | v3 built, **rebuild from 4K originals** |

## Rebuild recipe (brain/tools/diptych.sh; PNG→rgb24 first: `ffmpeg -i in.png -pix_fmt rgb24 out.png`)
```
slide 1: diptych.sh o3_rgb.png o2_rgb.png OUT.png 2672:1670:250:0 2848:1780:100:380 1.10 1.0 0.7 0
slide 2: diptych.sh f6.png f7.png OUT.png 1800:1125:150:0 1700:1062:20:63 1.12 1.03 0.7 0
```
Slide 1 specifics: top crop x 250–2922, y 0–1670 → excludes the parked GLA's plate (B JP 176, razor-sharp
at 4K, x≈3216–3336) and the garbled zebra-stripe artefacts (y>1680); bottom crop = the whole usable
picture height of the cart frame (y 380–2160) because o1/o2 carry baked-in black bars (top 380 px,
right 76 px) and his legs are cut at the bottom → the clip was shifted in his timeline. A frame grab
from the UNTOUCHED source clip would give the full 16:9 (more cart, his legs).
Cart frame choice: o2 over o1 (face sharpness 66 vs 57, direct gaze).

## Open
1. 4K PNG originals of the bath and floor (same way as the ZIP) → rebuild slide 2 crisp.
2. Optional first comment: "the floor is Tahsin's. he cooked for me there."
3. Rejected: frame 9 thumbs-up on the floor (dignity), frame 10 dark bath, frame 8 yacht (no human), 1:1.
