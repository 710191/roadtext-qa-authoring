# RoadTextVQA question authoring

Write one multiple-choice question per RoadTextVQA dashcam clip, following `AUTHORING_TEMPLATE.md`.

## Contents
- `AUTHORING_TEMPLATE.md` — the authoring rules (the prompt). Read it in full before starting.
- `sign_screen_ids.txt` — video ids to run, in order (see the end of the template).
- `tools/` — frame extraction, viewing, box check and saving scripts (Python 3, `opencv-python`, `numpy`).

## Setup
```bash
pip install -r requirements.txt
export VIDEO_DIR=/path/to/roadtextvqa/videos   # folder containing <id>.mp4
export FRAMES_DIR=frames                       # default
export OUT_DIR=out                             # default
export OCR_PATH=/path/to/roadtextvqa/ocr.zip   # official OCR from the RoadTextVQA release (zip or extracted folder)
```

## Workflow
```bash
# 1. extract every 15th frame (native + grid copy) for the id list; resumable
python tools/extract_frames.py sign_screen_ids.txt            # or: ... sign_screen_ids.txt <start id>

# 2. overview sheet per video (2x5, f0..f270 step 30) -> out/overview/ov<vid>.jpg
python tools/overview.py 1924 2001 2004

# 2b. official OCR words per video: which sampled frame (f0,f30..f270) first reads each word, box height native / at 224
python tools/ocr_words.py 1924 2001 2004

# 3. native look at chosen frames, optional region x1,y1,x2,y2 (native px) shown x3 and as seen at 224x224
python tools/frame_crops.py out/look_2004.jpg 2004 210,240 1700,380,1920,460

# 4. write questions in qline format (see template "Output") into a text file, then check boxes
python tools/box_check.py my_questions.txt                    # -> out/boxcheck/boxcheck_00.jpg

# 5. save -> out/questions.jsonl (one record per video; saving a video again replaces it)
python tools/qline.py my_questions.txt
```
