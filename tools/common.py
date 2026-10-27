"""Shared helpers. Paths come from environment variables:
  VIDEO_DIR   folder with the RoadTextVQA videos <id>.mp4 (required)
  FRAMES_DIR  where extract_frames.py writes frames (default ./frames)
  OUT_DIR     store / sheets output (default ./out)"""
import os
import cv2

VIDEO_DIR = os.environ.get("VIDEO_DIR", "")
FRAMES_DIR = os.environ.get("FRAMES_DIR", "frames")
OUT_DIR = os.environ.get("OUT_DIR", "out")


def video_path(vid):
    p = os.path.join(VIDEO_DIR, f"{vid}.mp4")
    if not os.path.exists(p):
        raise SystemExit(f"video not found: {p} (set VIDEO_DIR)")
    return p


def read_frames(vid, wanted):
    """Native frames {index: image} for the wanted frame indices (sequential read, exact indices)."""
    wanted = set(wanted)
    cap, i, out = cv2.VideoCapture(video_path(vid)), 0, {}
    while i <= max(wanted):
        ok, im = cap.read()
        if not ok:
            break
        if i in wanted:
            out[i] = im
        i += 1
    last = max(out) if out else None
    return {f: out.get(f, out.get(last)) for f in wanted}


def grid(im):
    g = im.copy()
    H, W = g.shape[:2]
    for x in range(0, W, 100):
        cv2.line(g, (x, 0), (x, H), (255, 255, 255), 1)
        cv2.putText(g, str(x), (x + 2, 14), 0, 0.45, (0, 255, 255), 1)
    for y in range(0, H, 100):
        cv2.line(g, (0, y), (W, y), (255, 255, 255), 1)
        cv2.putText(g, str(y), (2, y - 3), 0, 0.45, (0, 255, 255), 1)
    return g
