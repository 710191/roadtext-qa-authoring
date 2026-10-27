"""Native-resolution looks at given frames: python tools/frame_crops.py <out.jpg> <vid> <f1,f2,...> [x1,y1,x2,y2]
Each frame is shown full (with a 100 px grid labelled in native pixels) and, if a region is given, that region
enlarged 3x below it, plus the same region as it looks after downscaling the frame to 224x224 (enlarged to match).
Frames are stacked vertically."""
import os, sys
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import read_frames, grid

out, vid, frs = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")]
reg = [int(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else None
fr = read_frames(vid, frs)
rows = []
for f in frs:
    im = fr[f]
    H, W = im.shape[:2]
    g = grid(im)
    cv2.putText(g, f"v{vid} f{f}", (10, H - 12), 0, 1.0, (0, 255, 255), 2)
    rows.append(g)
    if reg:
        x1, y1, x2, y2 = reg
        c = cv2.resize(im[y1:y2, x1:x2], ((x2 - x1) * 3, (y2 - y1) * 3), interpolation=cv2.INTER_CUBIC)
        s = cv2.resize(cv2.resize(im, (224, 224), interpolation=cv2.INTER_AREA), (W, H), interpolation=cv2.INTER_NEAREST)
        s = cv2.resize(s[y1:y2, x1:x2], c.shape[1::-1], interpolation=cv2.INTER_NEAREST)
        pair = np.hstack([c, s])
        pad = np.zeros((pair.shape[0], W, 3), np.uint8)
        pad[:, :min(W, pair.shape[1])] = pair[:, :W]
        cv2.putText(pad, "native x3 | as seen at 224x224", (10, 30), 0, 0.9, (0, 255, 255), 2)
        rows.append(pad)
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(out)
