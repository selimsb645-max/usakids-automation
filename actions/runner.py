"""USA Kids Channel - runner: produce one lesson video, upload with publishAt,
commit ledgers, write report. Runs on GitHub Actions (zero-cost).

Usage:
  python3 actions/runner.py --mode produce   (default: render + upload)
  python3 actions/runner.py --mode selftest  (render only, no upload)
  python3 actions/runner.py --mode status    (slot + ledger summary)
"""
import argparse
import datetime as _dt
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kids import upload as yt
from kids.lessons import LESSONS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACT = os.path.join(REPO, "factory")
STATE_F = os.path.join(FACT, "state.json")
RUNS = os.path.join(FACT, "runs")
REPORTS = os.path.join(REPO, "actions", "reports")
os.makedirs(RUNS, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)


def log(m):
    print(m, flush=True)


def load_state():
    if os.path.exists(STATE_F):
        return json.load(open(STATE_F))
    return {"rotation": 0, "published": []}


def save_state(st):
    os.makedirs(FACT, exist_ok=True)
    json.dump(st, open(STATE_F, "w"), indent=1)


def next_lesson(st):
    used = {p["lesson"] for p in st["published"]}
    idx = st.get("rotation", 0) % len(LESSONS)
    lesson = LESSONS[idx]
    # never repeat a lesson already published
    for _ in range(len(LESSONS)):
        if lesson["id"] not in used:
            break
        st["rotation"] = (st.get("rotation", 0) + 1) % len(LESSONS)
        idx = st["rotation"]
        lesson = LESSONS[idx]
    return lesson


def commit(path, msg):
    tok = os.environ.get("GITHUB_TOKEN", "")
    if not tok:
        log("commit skipped (no token): " + path)
        return
    subprocess.run(["git", "config", "user.name", "usakids-bot"], check=False)
    subprocess.run(["git", "config", "user.email", "usakids-bot@users.noreply.github.com"], check=False)
    subprocess.run(["git", "add", path], check=False)
    subprocess.run(["git", "commit", "-m", msg, "--no-verify"], check=False)
    r = subprocess.run(["git", "push"], check=False,
                       env={**os.environ,
                            "GIT_USERNAME": "x-access-token",
                            "GIT_PASSWORD": tok})
    # rewrite remote with token if plain push fails
    if r.returncode != 0:
        url = subprocess.run(["git", "remote", "get-url", "origin"],
                             capture_output=True, text=True).stdout.strip()
        if url.startswith("https://"):
            subprocess.run(["git", "remote", "set-url", "origin",
                            url.replace("https://", f"https://x-access-token:{tok}@")],
                           check=False)
            subprocess.run(["git", "push"], check=False)
            subprocess.run(["git", "remote", "set-url", "origin", url], check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="produce", choices=["produce", "selftest", "status"])
    ap.add_argument("--lesson", default=None, help="force a lesson id")
    args = ap.parse_args()
    st = load_state()

    if args.mode == "status":
        pub_at, local = yt.next_slot()
        log(f"slot: {pub_at} ({local} BD)")
        log(f"published: {len(st.get('published', []))} videos; rotation={st.get('rotation')}")
        return

    if args.lesson:
        lesson = next(l for l in LESSONS if l["id"] == args.lesson)
    else:
        lesson = next_lesson(st)

    run_id = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=6))).strftime("%Y%m%d_%H%M")
    workdir = os.path.join(RUNS, f"{run_id}_{lesson['id']}")
    os.makedirs(workdir, exist_ok=True)
    log(f"lesson: {lesson['id']} ({len(lesson['beats'])} beats)")

    from kids import render as R
    mp4, total = R.render(lesson, workdir)
    thumb = R.make_thumb(lesson, workdir)

    if args.mode == "selftest":
        log(f"selftest OK: {mp4} ({total:.1f}s) - no upload")
        rep = {"mode": "selftest", "lesson": lesson["id"], "duration": round(total, 1),
               "file": os.path.basename(mp4), "ts": run_id}
        json.dump(rep, open(os.path.join(REPORTS, f"{run_id}_selftest.json"), "w"), indent=1)
        return

    pub_at, local = yt.next_slot()
    vid = yt.upload(lesson, mp4, thumb, pub_at)
    st.setdefault("published", []).append({
        "lesson": lesson["id"], "videoId": vid, "publishAt": pub_at,
        "local_slot": local, "date": run_id[:8]})
    st["rotation"] = (st.get("rotation", 0) + 1) % len(LESSONS)
    save_state(st)
    commit(STATE_F, f"publish {lesson['id']} -> {vid} @ {pub_at}")
    rep = {"mode": "produce", "lesson": lesson["id"], "videoId": vid,
           "publishAt": pub_at, "local_slot": local, "duration": round(total, 1)}
    json.dump(rep, open(os.path.join(REPORTS, f"{run_id}_publish.json"), "w"), indent=1)
    commit("actions/reports", f"report {run_id} {vid}")
    log(f"DONE video https://www.youtube.com/watch?v={vid} scheduled {local} BD")


if __name__ == "__main__":
    main()
