# Authoring template (APPROVED by user 2026-10-22; used from r1k id 264 on)
# REVISED 2026-10-22 (user OK): all `relaxed` escape hatches removed; Qwen gate (STEP 5b) enforced before saving;
# a video that cannot pass is reported to the user, not relaxed.

Adapted from: StreamingBench App. B.3 (QA-generation prompt), OVO-Bench §7.1 (volunteer guidelines incl. CRR),
StreamReady App. C (future-dependent questions + evidence-window checks), MMDuet §5.2 ("Not Mentioned" rejection),
StreamBridge (arXiv 2505.05467, NeurIPS 2025) App. B.3 Table 8 "Prompts used to generate QA pairs with GPT-4o" + its 8 task
descriptions, StreamingBench B.2 (caption-first for multi-frame, clue time range).
PDFs/txt: /work/a28133781/papers/qa_templates/ (2505.05467.txt lines 943-1062).
Our own rules added on top (advisor 10/21: both criteria must be FORCED).

---------------------------------------------------------------------------------------------------
You are writing ONE multiple-choice question for a ~10-second dashcam clip (RoadText-1K or RoadTextVQA).
Resolution differs per video (RoadText-1K 1280x720; RoadTextVQA 1280x720 or 1920x1080) -> read W x H from the video, never assume.
You have (commands in README.md):
  the overview sheet (tools/overview.py: 2x5 grid, native frames f0..f270 step 30), the pre-extracted native frames
  every 15th frame (tools/extract_frames.py -> frames/<vid>/fNNNN.jpg, grid copy gNNNN.jpg with 100 px lines labelled
  in native pixels), native crops on request (tools/frame_crops.py, shows the region native x3 and as seen at 224x224),
  and the official OCR words per sampled frame (tools/ocr_words.py: first frame each word is read, box height native / at 224).

STEP 1  Describe before you ask   (StreamingBench caption step)
  1. Write a short timeline of what is VISIBLE, with frame numbers: ego motion (stop / turn / pass), people, vehicles, signs.
  2. Only what is visible. Nothing you are unsure about. No guesses about intent.
  3. Mark which objects are SMALL (< ~60 px tall natively, unreadable at 224x224).

STEP 2  Pick two events   (OVO CRR guideline + StreamReady "Scene A / Scene B")
  1. Event A = a clear anchor everyone can find: our car turns / stops / passes X; a light changes; a bus leaves.
  2. Event B = what happens to a SMALL target after A (who appears first, which way it goes, what it does).
  3. A and B must be at least ~0.5 s apart (was ~1 s; user 2026-10-28).
  4. Mark A_time and the answer time t_ans (the first frame where B is decided). t_ans must be well before the clip end.
  4b. PRE-A TRAP (required, advisor via user 2026-10-23): with A as the boundary, BEFORE A the clip must show at least one
     object of the SAME kind as the answer — any kind: another sign / shop name, another person, another vehicle,
     another cyclist ... (user 2026-10-23) — readable at
     native resolution. It must be one of the distractors. An object of the same kind that appears together with the
     answer (same gantry / same sign / same frame, after A) does NOT count. No pre-A same-kind object -> no question.
  5. If the clip has no usable pair: do NOT relax. Try other targets / other event pairs; if none can pass STEP 5,
     STOP and report the video id to the user (no question is saved for it until the user decides).

STEP 3  Write the question   (StreamingBench GUIDE + user-supplied "Table 8" GPT-4o QA prompt, adapted)
  0. First pick the ONE question type that best suits THIS clip (Table 8 USER step); rotate types across clips.
     Prefer types that need two moments: order of events (before/after), cause -> effect, sudden change, linked event sequence
     (Table 8 rule 3). Pure attribute / current-action / position / text questions are NOT allowed (single-frame).
  1. Only about things visible in the clip; IGNORE contradictory or unreasonable parts of your own timeline (rule 1-2).
  2. Referent = the SHORTEST description that is still unique in the clip (user 2026-10-22). The referent must not leak the answer.
     a. From the STEP 1 timeline, count the objects of the same kind as the target (and as the event-A anchor) that are visible
        around the clue segment.
     b. Only one of its kind -> name it by kind alone ("the upcoming airport direction sign"), with NO side (left/right),
        NO screen position, NO color, NO extra text from the sign. "next / upcoming / first ... after A" is allowed (it is the time anchor).
     c. Several of its kind -> add only the ONE attribute that separates the target from the others (prefer what the object is or
        says over where it is on screen). Never add a second attribute "for safety".
     Write in the check field: "uniq: <kind> before A x<n> / after A x<m>, kept <attribute>".
     Example (312): over-hinted "which terminal letter is on the left green-and-orange sign at the next overhead gantry ahead?"
     -> "which terminal letter appears on the upcoming airport direction sign?"
  3. Answerable by watching the clip, without extra assumptions or outside inference (rule 4).
  4. No "in the video" / "in the beginning of the clip"; present / recent past tense is fine ("just now", "after we turn ...") (rule 7-8).
  5. No source references: never "according to ...", "which frame", "sequence of pictures", "which photo"; no "which second" (rule 9-10).
  6. Grammar, person and tense checked (rule 5, 8).
  7. No answers that settle only at the clip end (no totals, no "does it ever change").
  8. Record the clue segment = minimal span needed to answer = [A_time, t_ans] (StreamingBench B.2).

STEP 4  Write the options   (StreamingBench GUIDE + OVO option rules + our rule)
  1. 4 options, same format and similar length; terse.
  2. As far as possible, options should be things that really appear in the clip (time trap): e.g. a person/vehicle
     that appears BEFORE event A, or a second candidate that appears after B. Use invented distractors only when the
     clip offers no more candidates, and never let the answer be "the only option that appears".
  3. Distractors must be clearly distinguishable from the answer (no white vs silver, black vs dark blue).
  4. Avoid permutation options (Qwen guesses the "natural" order from text alone).

STEP 5  Self-check   (StreamReady evidence-window checks + MMDuet rejection)
  [ ] Before t_ans the answer is NOT knowable; at t_ans it is.
  [ ] Pre-A trap (STEP 2.4b): a same-kind object is visible before A and is one of the options; check field records
      "preA: <option text> f<frame>".
  [ ] At 224x224 the target of B is not identifiable (SR necessity); at native resolution it is.
  If any box fails -> rewrite (new target / new distractors / new event pair). No `relaxed` flag exists any more:
  a question either passes every box AND STEP 5b below, or it is not saved (STOP + report, see STEP 2.5).

STEP 5b  Filter — run BEFORE saving, per question   (enforced; replaces the old Qwen2.5-VL-7B gate, user 2026-10-23)
  The filter must not use any model that will be evaluated on the set (old gate made Qwen2.5-VL-7B 100% on multi by construction).
  1. Size (SR necessity, model-free): measure the answer target at t_ans in NATIVE pixels from its box.
     The detail that decides the answer (text, or what separates the target from the distractors: clothing,
     carried object, vehicle type ...) must be, in the author's judgment, NOT identifiable at 224x224 (x 224/W, x 224/H),
     while readable at native resolution. No fixed px threshold (user 2026-10-23); still record
     "size: <detail> Hpx native -> hpx at 224" in the check field.
  2. Readable (answerability, human): at native resolution the answer must be clearly readable in at least one
     frame in [t_ans, fe] that is a multiple of 30 (the 1-fps sampled frames). Look at that frame with frame_crops.py
     and write "readable: f<frame>" in the check field. If it is only readable between sampled frames, move fe or reject.

STEP 6  Boxes and save
  b: boxes in the video's NATIVE pixels (read them off the grid copy gNNNN.jpg / frame_crops.py; if measured on an
  overview tile 640x360: subtract tile offset, then x W/640 and x H/360);
  3 frames = [before A or at A, zoom frame, after]. Save with tools/qline.py <qline file>.
  Run tools/box_check.py on the qline file and look at every sheet before saving.

Output (qline):
vid ## tid|b:boxes ## f1,f2,f3 ## lab1;lab2;lab3 ## Event order ## question ## optA;optB;optC;optD ## letter ## fs-fe ## flags ## check
check field must state: A_time, t_ans, where each option appears (frames), size of the target at t_ans (px native / px at 224).

Gate = STEP 5b (deciding detail not identifiable at 224 (author judgment), readable on a sampled frame), checked per question
before saving; flags field is "-" for questions saved under this gate.
(Single-frame / shuffle probes were shown NOT to separate multi- vs single-frame questions on OVO-Bench -> not used as gates.)
---------------------------------------------------------------------------------------------------

## Worked example (from trial, video 185)
Timeline: f0-25 woman in white + child cross in front (big); f150-175 we pass blue "goodwill" truck (event A);
f225-240 man in dark blue jacket steps out between parked cars far left (~40 px); f250-300 he crosses.
Q: After we drive past the blue "goodwill" donation truck parked on the right, who is the first person to walk across the avenue in front of us?
Options: woman in white holding a child's hand (appears before A = time trap) / man in a dark blue jacket / nobody crosses
Known weakness found by qtest: the man is still identifiable at 224 -> SR box fails; a smaller/farther target is needed.

## Worked example that PASSED the current gate (r1k 941, saved 2026-10-27; answer later moved to D by shuffle_opts)
941 ## b:810,40,1010,200|636,156,710,208|640,138,726,198 ## 0,150,180 ## roadside sign KEEP RIGHT (pre-A);NEXT RIGHT tiny on the gantry panel [zoom];panel closer ## Event order ## After we pass the black roadside airport exit sign, what instruction is printed at the bottom of the next airport exit sign? ## KEEP RIGHT;EXIT ONLY;NEXT RIGHT;LEFT LANE ## C ## 0-180 ## - ## A_time f15-30 (we pass the dark roadside "Airport Exit via JFK Expwy To Belt Pkwy KEEP RIGHT" sign on the right), t_ans f150 (readable: f150); preA: KEEP RIGHT f0 (roadside sign = event A object); EXIT ONLY, LEFT LANE invented; size: "NEXT RIGHT" text ~5 px native -> ~1.5 px at 224 (f150); uniq: next airport exit sign after A = gantry, only panel (d) has bottom text, kept "next"; boxes checked


===================================================================================================
VIDEOS TO RUN (RoadTextVQA ids, in this order, one question per video)
===================================================================================================
every id in sign_screen_ids.txt, in list order from the first.
