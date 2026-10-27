"""Overview sheet: 2 rows x 5 native frames f0..f270 step 30 (from extracted frames), each tile 640x360 and
labelled "<vid> fNNNN". usage: python tools/overview.py <vid> [<vid> ...]  ->  $OUT_DIR/overview/ov<vid>.jpg"""
import os, sys
import cv2, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import FRAMES_DIR, OUT_DIR

os.makedirs(f"{OUT_DIR}/overview", exist_ok=True)
for vid in sys.argv[1:]:
    tiles = []
    for f in range(0, 300, 30):
        p = f"{FRAMES_DIR}/{vid}/f{f:04d}.jpg"
        t = cv2.resize(cv2.imread(p), (640, 360)) if os.path.exists(p) else np.zeros((360, 640, 3), np.uint8)
        cv2.putText(t, f"{vid} f{f:04d}", (6, 28), 0, 0.9, (0, 0, 0), 4)
        cv2.putText(t, f"{vid} f{f:04d}", (6, 28), 0, 0.9, (0, 255, 255), 2)
        tiles.append(t)
    sheet = np.vstack([np.hstack(tiles[:5]), np.hstack(tiles[5:])])
    cv2.imwrite(f"{OUT_DIR}/overview/ov{vid}.jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(f"{OUT_DIR}/overview/ov{vid}.jpg")
