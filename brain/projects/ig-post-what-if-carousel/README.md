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

| split | top | bottom | source | status |
|---|---|---|---|---|
| 1 | G-Klasse/Rolex street, Berlin | him pulling Tahsin's cart, Kadıköy night | 4K PNGs (his ZIP 1) | **FINAL** `split1_…FINAL…jpg` — he: "sieht krass aus" |
| 2 | Waldorf marble bath, teacup toast | Istanbul floor, heart blanket, smiling | 4K PNGs (`split_2.zip`: `1030(26)`, `1030(27)`) | **FINAL** `split2_…4K_FINAL…jpg` (bath face detail 2× vs chat copy) |
| 3 | G-Klasse interior, eye contact + friend (`1030(22)`, sun-flare haze) | dark Istanbul scrap-depot yard (`1030(33)`) | `split_3.zip` | **NOT BUILT** — depot frame breaks his own rules (see flags) |
| 4 | Waldorf spa pool (`1030(13)`) | **Tahsin on the Kadıköy bull**, Fenerbahçe jersey, arms wide (WhatsApp photo 2026-09-01) | `split_4.zip` | **DRAFT** (my pairing) `split4_…DRAFT…jpg` |
| — | Berlin underpass (`1030(4)`) | — | `split_4.zip` | **NOT USED** (dignity, faces, plates) |

Recommended carousel: **1 → 2 → 4** (three punches; a fourth dilutes). Split 4 is the "what if the man
you look down on is better than you" slide: the happiest person in the whole set is the one with least —
but poverty is NOT visible in it, so the first comment must carry Tahsin ("the floor is Tahsin's. he
cooked for me there."). Pairing 4 was my call; swap if he meant the underpass.

## Flags
- Depot frame (`1030(33)`): a youth (looks young — possibly a minor, face not visible) walks through a
  WIDE shot of the depot, dark, with a smeared hand in the corner. His own Istanbul brief: "no wide shots
  that identify the location · no footage of the children" (+ MEMORY §6 child-safety line). Replace with
  a depot image without people, or drop split 3.
- Underpass frame (`1030(4)`): a man's torn trousers expose his buttocks; seated people recognisable
  (consent unknown); several number plates legible. Dignity before drama (§1b) → do not use; if ever,
  crop/blur heavily.
- Split 4 bottom is a compressed WhatsApp JPG (1536×2048): fine at this size.

## Rebuild recipe (brain/tools/diptych.sh; PNG→rgb24 first: `ffmpeg -i in.png -pix_fmt rgb24 out.png`)
```
split 1: diptych.sh o3_rgb.png o2_rgb.png OUT.png 2672:1670:250:0 2848:1780:100:380 1.10 1.0 0.7 0
split 2: diptych.sh z2_1.png z2_2.png OUT.png 3456:2160:384:0 3456:2160:0:0 1.12 1.03 0.7 0   (4K bath/floor, rgb24)
split 4: diptych.sh z4_5.png z4_7.png OUT.png 3456:2160:264:0 1536:960:0:400 1.0 1.0 0.7 0   (pool / bull JPG)
```
Slide 1 specifics: top crop x 250–2922, y 0–1670 → excludes the parked GLA's plate (B JP 176, razor-sharp
at 4K, x≈3216–3336) and the garbled zebra-stripe artefacts (y>1680); bottom crop = the whole usable
picture height of the cart frame (y 380–2160) because o1/o2 carry baked-in black bars (top 380 px,
right 76 px) and his legs are cut at the bottom → the clip was shifted in his timeline. A frame grab
from the UNTOUCHED source clip would give the full 16:9 (more cart, his legs).
Cart frame choice: o2 over o1 (face sharpness 66 vs 57, direct gaze).

## Open
1. His call: carousel 1→2→4? Replace/drop split 3? Confirm the pairing of split 4.
2. Optional first comment: "the floor is Tahsin's. he cooked for me there."
3. Rejected: frame 9 thumbs-up on the floor (dignity), frame 10 dark bath, frame 8 yacht (no human), 1:1.
