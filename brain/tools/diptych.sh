#!/usr/bin/env bash
# Stack two 16:9 frames into ONE 4:5 Instagram slide (1080x1350): two 1080x670 panels + a 10 px
# white divider (his split-thumbnail look). Frames are DOWNSCALED (2000 px -> 1080 px), so no upscaling.
#
# usage: diptych.sh TOP.png BOTTOM.png OUT.png [TOP_CROP] [BOTTOM_CROP] [BOTTOM_GAMMA] [BOTTOM_CONTRAST] [SHARPEN]
#   CROP = W:H:X:Y in source pixels; keep W/H = 1.612 (e.g. 1813:1125, 1450:900, 1386:860)
#   default crop = 1813:1125:93:0 (full height, centred on a 2000x1125 frame)
#   BOTTOM_GAMMA >1 lifts a dark panel (1.12 used for the Istanbul floor); default 1.0
#   SHARPEN = luma unsharp amount on the finished slide (0 = off; 0.7 is the ceiling that stays clean on
#   compressed chat-upload frames — more just enhances the codec blocks)
# Needs ffmpeg. Grading only — never invents pixels (MEMORY §6).
set -euo pipefail
TOP="$1"; BOT="$2"; OUT="$3"
TC="${4:-1813:1125:93:0}"; BC="${5:-1813:1125:93:0}"; G="${6:-1.0}"; C="${7:-1.0}"; SH="${8:-0}"
SHF=""; if [ "$SH" != "0" ]; then SHF=",unsharp=5:5:${SH}:5:5:0.0"; fi
ffmpeg -hide_banner -loglevel error -y -i "$TOP" -i "$BOT" -filter_complex \
"[0:v]crop=${TC},scale=1080:670:flags=lanczos[a];\
[1:v]crop=${BC},scale=1080:670:flags=lanczos,eq=gamma=${G}:contrast=${C}[b];\
color=c=white:s=1080x10:d=1[d];[a][d][b]vstack=inputs=3${SHF},format=yuv420p" -frames:v 1 "$OUT"
