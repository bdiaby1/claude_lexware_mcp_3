#!/usr/bin/env python3
"""Pick the best still frames from a video clip for an IG post / thumbnail.

Scores every extracted frame on sharpness (Laplacian variance), exposure (mean luma not
crushed/blown), and — if OpenCV's face cascade is available — face size and open eyes.
Writes the top-N frames as PNG plus a contact sheet, so the choice is made from REAL frames
(MEMORY §6: real frames only; upscaling is restoration, never invention).

Usage:
  python3 best_frame.py clip.mp4 --out frames/ [--fps 5] [--top 5] [--start 12 --end 20] [--keyframes]
Needs: ffmpeg on PATH, python3 with numpy + opencv-python-headless<5 (python3 -m pip install "opencv-python-headless<5").
Tip: run on the ORIGINAL export, not the IG/YouTube re-encode. 4K source → crop, don't upscale.
"""
import argparse, os, re, subprocess, sys, glob, shutil

def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--out", default="frames")
    ap.add_argument("--fps", type=float, default=5.0); ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--start", type=float, default=None); ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--keyframes", action="store_true",
                    help="only I-frames (the highest-quality frames of an H.264/H.265 clip) instead of fps sampling")
    a = ap.parse_args()
    try:
        import cv2, numpy as np
    except ImportError:
        sys.exit("pip install numpy opencv-python-headless")
    os.makedirs(a.out, exist_ok=True)
    raw = os.path.join(a.out, "_raw"); shutil.rmtree(raw, ignore_errors=True); os.makedirs(raw)
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "info" if a.keyframes else "error"]
    if a.start is not None: cmd += ["-ss", str(a.start)]
    cmd += ["-i", a.video]
    if a.end is not None: cmd += ["-to", str(a.end - (a.start or 0))]
    if a.keyframes:
        cmd += ["-vf", "select='eq(pict_type,I)',showinfo", "-fps_mode", "vfr", "-q:v", "2", os.path.join(raw, "f_%05d.png")]
    else:
        cmd += ["-vf", f"fps={a.fps}", "-q:v", "2", os.path.join(raw, "f_%05d.png")]
    res = run(cmd)
    kf_times = [float(m) for m in re.findall(r"pts_time:\s*([0-9.]+)", res.stderr)] if a.keyframes else []
    # Haar cascades exist in OpenCV 4.x (pip install "opencv-python-headless<5"); OpenCV 5 dropped
    # them — then we score without faces rather than fail.
    cascade = eyes = None
    if hasattr(cv2, "CascadeClassifier"):
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        eyes = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    else:
        print("note: no CascadeClassifier in this OpenCV — scoring sharpness/exposure only", file=sys.stderr)
    scored = []
    for f in sorted(glob.glob(os.path.join(raw, "f_*.png"))):
        img = cv2.imread(f); g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sharp = cv2.Laplacian(g, cv2.CV_64F).var()
        luma = g.mean(); expo = 1.0 - abs(luma - 110) / 110  # best around mid-grey
        faces = cascade.detectMultiScale(g, 1.1, 5, minSize=(40, 40)) if cascade is not None and not cascade.empty() else []
        face_score, eye_bonus = 0.0, 0.0
        for (x, y, w, h) in faces:
            face_score = max(face_score, (w * h) / (g.shape[0] * g.shape[1]))
            roi = g[y:y + h // 2, x:x + w]
            if eyes is not None and not eyes.empty() and len(eyes.detectMultiScale(roi, 1.1, 3)) >= 2: eye_bonus = 1.0
        idx = int(os.path.basename(f)[2:7]) - 1
        t = (kf_times[idx] if a.keyframes and idx < len(kf_times) else idx / a.fps) + (a.start or 0)
        score = sharp * (0.5 + expo) * (1 + 3 * face_score) * (1 + 0.5 * eye_bonus)
        scored.append((score, t, f, sharp, luma, len(faces), eye_bonus))
    scored.sort(reverse=True)
    # keep winners at least 0.6s apart so the top-N are different moments
    picks, used = [], []
    for s in scored:
        if all(abs(s[1] - u) >= 0.6 for u in used): picks.append(s); used.append(s[1])
        if len(picks) >= a.top: break
    outs = []
    for i, (score, t, f, sharp, luma, nf, eb) in enumerate(picks, 1):
        dst = os.path.join(a.out, f"best_{i:02d}_t{t:06.2f}s.png"); shutil.copy(f, dst); outs.append(dst)
        print(f"{i}. t={t:6.2f}s  sharp={sharp:7.1f}  luma={luma:5.1f}  faces={nf}  eyes={'y' if eb else 'n'}  -> {dst}")
    if shutil.which("montage") and outs:
        run(["montage"] + outs + ["-tile", f"{len(outs)}x1", "-geometry", "+6+6", "-label", "%f",
             os.path.join(a.out, "contact_sheet.jpg")])
        print("contact sheet:", os.path.join(a.out, "contact_sheet.jpg"))
    shutil.rmtree(raw, ignore_errors=True)

if __name__ == "__main__":
    main()
