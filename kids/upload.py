"""USA Kids Channel - YouTube auth (own OAuth client) + resumable upload + slot logic."""
import datetime as _dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
TOKEN_F = os.environ.get("YT_TOKEN_FILE",
                         os.path.join(os.path.dirname(BASE), "yt-auth", "token_usakids.json"))
TZ = _dt.timezone(_dt.timedelta(hours=6))          # Asia/Dhaka
SLOT_LOCAL_H, SLOT_LOCAL_M = 18, 30                # public slot 18:30 BD daily
LEAD_MIN = 3 * 60                                  # min lead production -> publish


def log(m):
    print(m, flush=True)


def get_token():
    tok = json.load(open(TOKEN_F)) if os.path.exists(TOKEN_F) else {}
    now = int(time.time())
    if tok.get("access_token") and tok.get("expires_at", 0) > now + 120:
        return tok
    if not (tok.get("refresh_token") and tok.get("client_id") and tok.get("client_secret")):
        raise SystemExit("TOKEN_MISSING_NO_REFRESH")
    body = urllib.parse.urlencode({
        "client_id": tok["client_id"], "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=body)
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read().decode())
    tok["access_token"] = out["access_token"]
    tok["expires_at"] = now + int(out.get("expires_in", 3599))
    json.dump(tok, open(TOKEN_F, "w"), indent=1)
    log("token: minted headlessly (own OAuth client)")
    return tok


def next_slot(now=None):
    """Next 18:30 BD slot at least LEAD_MIN ahead. Returns ISO (Z) + local str."""
    now = now or _dt.datetime.now(TZ)
    target = now.replace(hour=SLOT_LOCAL_H, minute=SLOT_LOCAL_M, second=0, microsecond=0)
    if (target - now).total_seconds() < LEAD_MIN:
        target += _dt.timedelta(days=1)
    return target.astimezone(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), \
        target.strftime("%Y-%m-%d %H:%M")


def _yt(tok, path, method="GET", data=None):
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/" + path,
        data=data, method=method,
        headers={"Authorization": "Bearer " + tok["access_token"],
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"YT_API {e.code}: " + e.read().decode(errors="replace")[:300])


def slot_taken(publish_at):
    """Is the slot already booked on YouTube (duplicate guard)?"""
    try:
        tok = get_token()
        ch = _yt(tok, "channels?part=contentDetails&mine=true")
        upl = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        pl = _yt(tok, "playlistItems?part=contentDetails&maxResults=15&playlistId=" + upl)
        ids = [it["contentDetails"]["videoId"] for it in pl.get("items", [])]
        if not ids:
            return False
        vs = _yt(tok, "videos?part=status&id=" + ",".join(ids))
        target = _dt.datetime.fromisoformat(publish_at.replace("Z", "+00:00"))
        for v in vs.get("items", []):
            pa = v["status"].get("publishAt")
            if not pa:
                continue
            when = _dt.datetime.fromisoformat(pa.replace("Z", "+00:00"))
            if abs((when - target).total_seconds()) <= 45 * 60:
                log(f"slot {publish_at} already booked by {v['id']} - skipping")
                return True
    except SystemExit:
        raise
    except Exception as ex:
        log("slot check warning: " + str(ex)[:140])
    return False


def upload(lesson, mp4, thumb, publish_at, playlist=None):
    tok = get_token()
    if slot_taken(publish_at):
        raise SystemExit("SLOT_ALREADY_TAKEN")
    DISC = ("This video includes AI-generated visuals and voiceover for educational "
            "purposes. Made for Kids: family-friendly, safe, and COPPA-compliant.")
    tags = list(lesson["tags"])
    kw = ", ".join(tags[:10])
    hashtags = " ".join("#" + t.title().replace(" ", "") for t in tags[:4])
    desc = lesson["desc"].strip()
    desc += "\n\nRelated searches: " + kw
    desc += "\n\n" + hashtags
    if playlist:
        desc += "\n\nWatch more: " + playlist
    if DISC not in desc:
        desc += "\n\n" + DISC
    meta = {
        "snippet": {
            "title": lesson["title"][:99],
            "description": desc[:4900],
            "tags": tags,
            "categoryId": "27",          # Education
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": True,
        },
    }
    body = json.dumps(meta).encode()
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos"
        "?uploadType=resumable&part=snippet,status",
        data=body, method="POST",
        headers={"Authorization": "Bearer " + tok["access_token"],
                 "Content-Type": "application/json",
                 "Content-Length": str(len(body))})
    try:
        with urllib.request.urlopen(req, timeout=60) as r0:
            loc = r0.headers["Location"]
    except urllib.error.HTTPError as e:
        raise SystemExit(f"UPLOAD_INIT_FAILED {e.code}: " + e.read().decode(errors="replace")[:300])
    with open(mp4, "rb") as f:
        data = f.read()
    req2 = urllib.request.Request(loc, data=data, method="PUT",
                                  headers={"Content-Type": "video/mp4",
                                           "Content-Length": str(len(data))})
    try:
        with urllib.request.urlopen(req2, timeout=600) as r2:
            out = json.loads(r2.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"UPLOAD_FAILED {e.code}: " + e.read().decode(errors="replace")[:300])
    vid = out.get("id")
    if not vid:
        raise SystemExit("UPLOAD_NO_ID")
    log(f"upload: OK videoId={vid} publishAt={publish_at}")
    # thumbnail
    try:
        with open(thumb, "rb") as f:
            tdata = f.read()
        req3 = urllib.request.Request(
            f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
            data=tdata, method="POST",
            headers={"Authorization": "Bearer " + tok["access_token"],
                     "Content-Type": "image/jpeg",
                     "Content-Length": str(len(tdata))})
        with urllib.request.urlopen(req3, timeout=60) as r3:
            log("thumb: set " + str(json.loads(r3.read().decode()).get("default", {}).get("url", ""))[:40])
    except Exception as ex:
        log("thumb: warning " + str(ex)[:140])
    return vid


def upload_rhymes(comp, mp4, thumb, publish_at):
    """Upload a nursery-rhyme compilation (list of rhyme dicts from rhymes.py)."""
    primary = comp[0]
    titles = [r["title"] for r in comp]
    lesson = {
        "title": primary["title_full"][:99],
        "desc": ("Sing along with " + ", ".join(titles) + "!\n\n"
                 "USA Kids presents fun nursery rhymes and kids songs for babies, "
                 "toddlers and preschoolers. Colorful animation, friendly voices and "
                 "easy sing-along lyrics make learning letters, numbers, colors and "
                 "good habits joyful. Perfect for playtime, bedtime and family fun!\n\n"
                 "Chapters:\n" + "\n".join(f"0{i+1}. {t}" for i, t in enumerate(titles))),
        "tags": [t.strip() for r in comp for t in r["keywords"].split(",")][:18],
    }
    # YouTube tags cap: keep total under 480 chars
    while len(" ".join(lesson["tags"])) > 480:
        lesson["tags"].pop()
    return upload(lesson, mp4, thumb, publish_at)
