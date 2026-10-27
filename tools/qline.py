"""Compact question saver: python tools/qline.py <qline file>. One question per line, fields separated by ' ## ':
video ## b:x1,y1,x2,y2|x1,y1,x2,y2|x1,y1,x2,y2 ## f1,f2,f3 ## lab1;lab2;lab3 ## type ## question ## optA;optB;optC;optD
  ## answer letter ## fs-fe ## flags (; sep, "-" = none) ## check
The zoom column is always index 1. Options get '(A) ' prefixes added. Saved to $OUT_DIR/questions.jsonl,
one record per video (saving the same video again replaces it)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import OUT_DIR

OUT = f"{OUT_DIR}/questions.jsonl"


def load():
    return [json.loads(l) for l in open(OUT)] if os.path.exists(OUT) else []


def save(rec):
    os.makedirs(OUT_DIR, exist_ok=True)
    recs = [r for r in load() if r["video"] != rec["video"]] + [rec]
    recs.sort(key=lambda r: int(r["video"]))
    with open(OUT, "w") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("saved video", rec["video"], "total", len(recs))


for l in open(sys.argv[1]):
    l = l.strip()
    if not l or l.startswith("#"):
        continue
    vid, tid, fr, lab, typ, q, opts, ans, win, flags, chk = [x.strip() for x in l.split(" ## ")]
    if not tid.startswith("b:"):
        print("SKIP (boxes must be b:...)", vid); continue
    bx = [[int(x) for x in b.split(",")] for b in tid[2:].split("|")]
    cols = [dict(f=int(f), box=b, label=l2) for f, b, l2 in zip(fr.split(","), bx, lab.split(";"))]
    cols[1]["zoom"] = True
    L = "ABCD"; ol = opts.split(";")
    options = [f"({L[i]}) {x}" for i, x in enumerate(ol)]
    fs, fe = [int(x) for x in win.split("-")]
    save(dict(video=vid, type=typ, question=q, options=options, answer=options[L.index(ans)], f_start=fs, f_end=fe,
              flags=[x for x in flags.split(";") if x and x != "-"], cols=cols, check=chk))
