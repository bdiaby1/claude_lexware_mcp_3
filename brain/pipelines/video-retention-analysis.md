# PIPELINE — Video Retention Analysis

Operational wrapper for this repo/environment; the brief below it is the method,
verbatim from Benjamin's handoff (drop-in replacement for VIDEO_ANALYSIS_BRIEF.md).

## Before you start (this environment)
- **Inputs Benjamin sends into the chat:** 480p proxy of Michael's cut (split in
  halves if too big — the first 60–90s alone cover ~80% of the retention decision)
  + ElevenLabs Scribe transcript with timestamps (.txt/.srt).
- **Install tools first** — NOT preinstalled in these containers (verified 2026-08-21):
  `apt-get install -y ffmpeg imagemagick` (gives `ffmpeg`, `ffprobe`, `montage`).
- **Work in the session scratchpad**, never in the repo: frames, contact sheets and
  the proxy are working material. Only the findings file is committed.
- **Load context before looking at a single frame:** the project's script, footage
  protocol and VO sheet (`brain/projects/<video>/`). The "missing best material"
  check is the one thing no tool can do — it only works if you know what was filmed.
- **If the input is a SCREEN RECORDING** (he films the player, e.g. from Drive): crop to
  the video area FIRST or every measurement is polluted by player UI and letterboxing.
  `ffprobe` the size, pull one full frame, look at it, then e.g.
  `-vf "crop=1152:648:180:0"` for a 16:9 video pillarboxed inside a 1512x648 screen.
  Verified 12 Sep 2026 on the Istanbul hook.
- **Scene detection UNDER-REPORTS cuts in dark footage.** The brief's `scene>0.3` is
  right for normal material, but night scenes have too little frame-to-frame contrast
  to cross it. On the Istanbul hook it reported a 6.8s static hold that did not exist —
  a second pass at `>0.12` showed five cuts inside that window. **Always re-run any
  suspected static stretch at a lower threshold before reporting it**, and cross-check
  with brightness: `fps=1,signalstats` → `YAVG` per second. A "hole" that is really a
  dark stretch is a legibility finding, not a pacing finding — two different notes for
  Michael.
- **Brightness is a real finding on its own.** YAVG under ~50 while the rest of the cut
  sits at 100+ means that stretch is close to unreadable on a phone in daylight. Worth
  flagging whenever the dark stretch carries an important line.
- **Output:** `brain/projects/<video>/findings/YYYY-MM-DD_<cutname>.md` — one line
  per issue, `timecode → problem → instruction for Michael`. Commit + push, update
  STATE.md + LOG.md per `brain/README.md`.
- **After publishing:** Benjamin screenshots the YouTube Studio retention curves →
  read the exact second people leave, compare against the findings file, and write
  the deltas into the same findings file (prediction vs proof). Durable lessons →
  dated MEMORY.md addition.

---

# VIDEO RETENTION ANALYSIS — BRIEF FOR CLAUDE CODE (verbatim)

## YOUR ROLE

You are the retention consultant / creative director. Michael cuts. You analyze and deliver timecoded instructions for him. You do NOT edit video.

You cannot watch video. You CAN read images extremely well. So the video must be translated into data: transcript with timestamps + frames + cut-frequency numbers.

## INPUTS

1. `transcript.txt` / `.srt` — timestamped transcript (from ElevenLabs Scribe).
2. `cut.mp4` — 480p compressed proxy of Michael's rough cut. (Full quality is too large. If the file is still too big: split in halves. The first 60–90 seconds alone already cover ~80% of the retention decision.)

## THE RULE THAT MATTERS MOST

Never analyze all frames blindly. A 7-minute video = ~420 frames at 1fps. Looking at all of them fills your working memory and you will start missing the important ones. Work in stages, cheapest first:

### Stage 1 — Extract frames, named by timestamp
```bash
ffmpeg -i cut.mp4 -vf fps=1 frames/frame_%04d.jpg
```
`frame_0043.jpg` = second 43. Never rename them — the filename IS the timecode.

### Stage 2 — Scene detection FIRST (numbers, not images)
```bash
ffmpeg -i cut.mp4 -filter:v "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep showinfo
```
This gives you every cut point as a number. Compute cuts-per-30-seconds per section. Any stretch >20s without a cut is a retention hole — you know that WITHOUT looking at a single image. Write it down.

### Stage 3 — Contact sheets (~30 frames per sheet, timestamps burned in)
```bash
montage frames/frame_00*.jpg -tile 6x5 -geometry 160x90+2+2 -label '%f' sheet_01.jpg
```
Scan the sheets. You are looking for: static stretches, repeated identical framings, chaos, and the strongest single images.

### Stage 4 — Targeted zoom ONLY on suspects
Cross the transcript against the sheets. Where a strong sentence sits on a weak or unrelated picture → open those individual frames full size. Aim for ~40–60 frames analyzed deeply — the RIGHT ones.

### Stage 5 — Write findings to a file as you go
`findings.md`, one line per issue: `timecode → problem → instruction for Michael`. Don't hold it in your head.

## WHAT TO LOOK FOR

- **Hook (0–30s):** does the first frame carry visual information? Does something change every few seconds? Is the collision/promise landed inside 30 seconds?
- **Re-hook rhythm:** a pattern interrupt roughly every 30 seconds — new location, new speaker, graphic, sound break.
- **Picture/text mismatch:** the strongest sentence must sit on the strongest picture. Flag every case where it doesn't.
- **Static stretches:** long VO over a barely-changing image = they leave.
- **Missing best material:** you know the footage notes (see the protocol files). If a beat that exists in the notes is missing from the cut, or arrives too late, say so. No tool can do this — only you, because you know what was filmed.
- **Loop hygiene:** every opened loop must close (except deliberate never-resolves). Check them by name against the script file.
- **Ending:** does the last line land on the right image, and is the CTA soft and short?

## WHAT YOU HONESTLY CANNOT DO

- Motion between frames (pans, whip transitions, shakiness) — invisible to you.
- Whether music FEELS right — you can only read audio levels/onsets technically, e.g.:
```bash
ffmpeg -i cut.mp4 -af "silencedetect=n=-30dB:d=0.5" -f null - 2>&1 | grep silence
```
That tells you where silence and loudness sit — not whether it's beautiful. That judgment stays with Benjamin and Michael. Say so instead of guessing.

## OUTPUT FORMAT (what Michael receives)

```
[00:45–00:58] VO is strong, picture is static (no cut for 13s).
→ Michael: cut in the refusal shots here, or push in slowly.

[01:12] "They became criminals here" — the line of the video — sits on a wide shot.
→ Michael: put the interview close-up here. Music out.

[03:40] The bathrobe/blue-light frame arrives too late — it's the strongest image in the film.
→ Michael: move it earlier or repeat it as a chapter divider.
```

Short lines. Timecode, problem, instruction. No essays.

## AFTER PUBLISHING

Retention curves in YouTube Studio are the truth. Benjamin screenshots them → you read the exact second people leave and why, then compare against these findings. Pre-publish analysis is prediction, curves are proof. Both together is the loop that makes the next video better.

## Addendum 2026-10-30 — stills for IG posts: pick first, upscale last
- `brain/tools/best_frame.py clip.mp4 --out frames --start S --end E` → top-5 REAL frames scored
  on sharpness/exposure/face/eyes + contact sheet. Run on the original export, never the IG/YT
  re-encode. A 4K frame (3840×2160) already exceeds an IG 4:5 post (1080×1350) → crop, don't
  upscale.
- Upscaling (1080p + tight crop only), in order of "stays real": Lightroom Super Resolution 2× ·
  Topaz Photo AI with Face Recovery OFF · Upscayl / Real-ESRGAN 2× (running it in the sandbox: UNVERIFIED — see 30 Oct status below) · never
  Magnific/Krea on faces (they redraw skin/eyes — §6 real-frames rule). Test: at 100 % is it still
  HIS face? Instagram recompresses on upload — frame choice survives, extra sharpness mostly not.

### Upscaling status 30 Oct (what is verified, what is not)
- Question from him: is "the same engine here" an API key or a skill? Answer: neither — Real-ESRGAN is
  open-source software installed INSIDE the sandbox (no licence, no key). Claude's earlier "I can run
  it here" was said WITHOUT testing — corrected.
- Verified: sandbox = 4 CPUs, 16 GB RAM, NO GPU; GitHub release assets reachable through the proxy;
  official `realesrgan-ncnn-vulkan` v0.2.5.0 (2022-04-24, 47 MB, models realesrgan-x4plus etc.) downloaded
  and unpacked to the scratchpad; `libvulkan1` + `mesa-vulkan-drivers` installed.
- NOT verified: that it runs, its speed on CPU, its output quality. Executing the downloaded binary was
  BLOCKED by the auto-mode permission classifier ("code from external"); not worked around. It needs his
  explicit allow (permission rule / approval) before it is retried.
- Intended run (unverified): `realesrgan-ncnn-vulkan -i in.png -o out_4x.png -n realesrgan-x4plus -s 4 -g -1 -m <models dir>`
  then 4x -> target size with `ffmpeg -vf scale=W:H:flags=lanczos` (x4plus is native 4x only).
- Paid route that works WITH Claude: Topaz Labs API (pay-per-use credits, X-API-Key header; Precision
  Upscale = 24 output MP per credit; Generative/Creative models invent detail -> not for faces).
  A 1080x1350 output is 1.46 MP = ~0.06 credit. A desktop licence (Topaz Photo AI / Gigapixel / Lightroom)
  is a GUI app on his computer; Claude cannot operate it from the cloud container.

### Stills from video — quality rules (30 Oct, after "too unsharp, every time")
- Inputs: ZIP of ORIGINAL 6–10 s clips (not chat images; those arrive ≤2000 px at 0.25–0.7 bpp).
- Pick: `best_frame.py clip --start S --end E --keyframes` → check the contact sheet → crop → export.
- Build: 4:5 split via `diptych.sh` (downscale only, white 10 px divider); sharpen ≤0.7; light gamma only.
- Shoot: photos beside the video at ≥1/250 s for anything meant as a still.
- Ratio: stay 4:5 (3:4 if he never boosts); 1:1 rejected (grid crops a square by 25 % width).
