"""Official RoadTextVQA OCR per video: python tools/ocr_words.py <vid> [<vid> ...]
The release's ocr.zip holds one Google Vision result per sampled frame (<vid>_<f>.json, f = 0,30,...,270):
textAnnotations[0] is the whole-frame text, the rest are single words with 4-corner boundingPoly in native pixels.
There is no track id, so words are grouped by identical text (case-insensitive) across frames.
For every word prints: frames where it was read, box height per frame (native px), and that height at 224x224,
sorted by first frame. OCR_PATH = ocr.zip or a folder with the extracted json files (searched recursively)."""
import json, os, sys, zipfile
import cv2
sys.path.insert(0, os.path.dirname(__file__))
from common import FRAMES_DIR

OCR_PATH = os.environ.get("OCR_PATH", "ocr.zip")


def ocr_files():
    if zipfile.is_zipfile(OCR_PATH):
        z = zipfile.ZipFile(OCR_PATH)
        return {os.path.basename(n): (lambda n=n: z.read(n)) for n in z.namelist() if n.endswith(".json")}
    out = {}
    for d, _, fs in os.walk(OCR_PATH):
        for f in fs:
            if f.endswith(".json"):
                out[f] = (lambda p=os.path.join(d, f): open(p, "rb").read())
    return out


files = ocr_files()
for vid in sys.argv[1:]:
    p = f"{FRAMES_DIR}/{vid}/f0000.jpg"
    H = cv2.imread(p).shape[0] if os.path.exists(p) else 1080
    words = {}
    for f in range(0, 300, 30):
        key = f"{vid}_{f}.json"
        if key not in files:
            continue
        ann = json.loads(files[key]()).get("textAnnotations") or []
        for a in ann[1:]:
            ys = [v.get("y", 0) for v in a["boundingPoly"]["vertices"]]
            xs = [v.get("x", 0) for v in a["boundingPoly"]["vertices"]]
            w = words.setdefault(a["description"].lower(), {"text": a["description"], "obs": []})
            w["obs"].append((f, max(ys) - min(ys), min(xs), min(ys), max(xs), max(ys)))
    print(f"== video {vid}  (H={H}; {sum(1 for f in range(0, 300, 30) if f'{vid}_{f}.json' in files)} OCR frames)")
    if not words:
        print("   no OCR")
    for w in sorted(words.values(), key=lambda w: (w["obs"][0][0], w["text"])):
        seen = " ".join(f"f{f}:{h}px({h * 224 / H:.1f})" for f, h, *_ in w["obs"])
        f0, _, x1, y1, x2, y2 = w["obs"][0]
        print(f"   {w['text'][:24]:<24} first f{f0} box {x1},{y1},{x2},{y2}  {seen}")
