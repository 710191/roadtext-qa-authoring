"""Pre-extract authoring frames so questions can be written without re-reading the video.
For every video id in <id list> (optionally from <start id> on): every STEP-th frame at native resolution ->
  $FRAMES_DIR/<vid>/f0000.jpg ... and a copy with a 100 px grid labelled in native pixels -> g0000.jpg
Skips videos whose folder already has a DONE marker (resumable).
usage: python tools/extract_frames.py <id list> [start id] [step=15]"""
import os, sys
import cv2
sys.path.insert(0, os.path.dirname(__file__))
from common import FRAMES_DIR, video_path, grid

ids = [l.strip() for l in open(sys.argv[1]) if l.strip()]
if len(sys.argv) > 2:
    ids = ids[ids.index(sys.argv[2]):]
step = int(sys.argv[3]) if len(sys.argv) > 3 else 15

for n, vid in enumerate(ids):
    d = f"{FRAMES_DIR}/{vid}"
    if os.path.exists(f"{d}/DONE"):
        continue
    os.makedirs(d, exist_ok=True)
    cap, i, size = cv2.VideoCapture(video_path(vid)), 0, "?"
    while True:
        ok, im = cap.read()
        if not ok:
            break
        size = f"{im.shape[1]}x{im.shape[0]}"
        if i % step == 0:
            cv2.imwrite(f"{d}/f{i:04d}.jpg", im, [cv2.IMWRITE_JPEG_QUALITY, 92])
            cv2.imwrite(f"{d}/g{i:04d}.jpg", grid(im), [cv2.IMWRITE_JPEG_QUALITY, 92])
        i += 1
    open(f"{d}/DONE", "w").write(str(i))
    print(f"{n + 1}/{len(ids)} {vid} frames={i} size={size}", flush=True)
