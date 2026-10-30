#!/usr/bin/env bash
# Stack two 16:9 frames into ONE 4:5 Instagram slide (1080x1350) = two panels, optional white divider.
# Frames are DOWNSCALED (2000/4000 px -> 1080 px), so nothing is upscaled and it comes out crisp.
#
# usage: diptych.sh TOP BOTTOM OUT [TOP_CROP] [BOTTOM_CROP] [BOTTOM_GAMMA] [BOTTOM_CONTRAST] [SHARPEN] [DIVIDER_PX] [TOP_EQ]
#   CROP        W:H:X:Y in source pixels. Keep W/H = 1.6 when DIVIDER_PX=0 (panel 1080x675),
#               1.612 when DIVIDER_PX=10 (panel 1080x670). Default 1813:1125:93:0 (2000x1125 frame).
#   GAMMA       >1 lifts the BOTTOM panel (dark night/low-light frames); default 1.0
#   TOP_EQ      optional ffmpeg eq args for the TOP panel, e.g. "contrast=1.12:brightness=-0.03" (de-haze a sun-flared frame)
#   SHARPEN     luma unsharp on the finished slide; 0 = off. 0.7 = ceiling that stays clean
#   DIVIDER_PX  white bar between the panels; default 10; 0 = NONE (his preference since 30 Oct: both
#               seams already have a hard tonal break, the bar only costs pixels)
# Needs ffmpeg 6. Two stages on purpose: one filtergraph with two 4K inputs crashed ffmpeg 6.1.1
# ("malloc(): corrupted top size"). Grading only — never invents pixels (MEMORY §6).
set -euo pipefail
TOP="$1"; BOT="$2"; OUT="$3"
TC="${4:-1813:1125:93:0}"; BC="${5:-1813:1125:93:0}"; G="${6:-1.0}"; C="${7:-1.0}"; SH="${8:-0}"; DIV="${9:-10}"; TEQ="${10:-}"
TEQF=""; if [ -n "$TEQ" ]; then TEQF=",eq=${TEQ}"; fi
PH=$(( (1350 - DIV) / 2 ))
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
FF="ffmpeg -nostdin -hide_banner -loglevel error -y"
$FF -i "$TOP" -vf "crop=${TC},scale=1080:${PH}:flags=lanczos${TEQF}" "$T/a.png"
$FF -i "$BOT" -vf "crop=${BC},scale=1080:${PH}:flags=lanczos,eq=gamma=${G}:contrast=${C}" "$T/b.png"
SHF=""; if [ "$SH" != "0" ]; then SHF=",unsharp=5:5:${SH}:5:5:0.0"; fi
if [ "$DIV" -gt 0 ]; then
  $FF -i "$T/a.png" -i "$T/b.png" -filter_complex "color=c=white:s=1080x${DIV}:d=1[d];[0:v][d][1:v]vstack=inputs=3${SHF},format=yuv420p" -frames:v 1 "$OUT"
else
  $FF -i "$T/a.png" -i "$T/b.png" -filter_complex "[0:v][1:v]vstack=inputs=2${SHF},format=yuv420p" -frames:v 1 "$OUT"
fi
