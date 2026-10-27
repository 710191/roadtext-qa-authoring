"""Check manual b: boxes in qline files: python tools/box_check.py <qline files...>
For every question draws its three boxes on the three frames (red) and writes contact sheets of 8 questions each
(one row per question: 3 frames, 480x270 each) to $OUT_DIR/boxcheck/boxcheck_<n>.jpg."""
import os, sys
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import OUT_DIR, read_frames

out = f"{OUT_DIR}/boxcheck"
os.makedirs(out, exist_ok=True)
rows = []
for fn in sys.argv[1:]:
    for l in open(fn):
        p = [x.strip() for x in l.split(" ## ")]
        if len(p) < 4 or not p[1].startswith("b:"):
            continue
        rows.append((p[0], [[int(x) for x in b.split(",")] for b in p[1][2:].split("|")], [int(x) for x in p[2].split(",")], p[3].split(";")))
sheets = []
for vid, boxes, frs, labs in rows:
    fr = read_frames(vid, frs)
    tiles = []
    for b, f, lab in zip(boxes, frs, labs):
        im = fr[f].copy()
        cv2.rectangle(im, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 8)
        im = cv2.resize(im, (480, 270))
        cv2.putText(im, f"v{vid} f{f} {lab[:30]}", (4, 22), 0, 0.6, (0, 255, 255), 2)
        tiles.append(im)
    sheets.append(np.hstack(tiles))
    print(vid, flush=True)
for i in range(0, len(sheets), 8):
    cv2.imwrite(f"{out}/boxcheck_{i // 8:02d}.jpg", np.vstack(sheets[i:i + 8]), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(f"{out}/boxcheck_{i // 8:02d}.jpg")
