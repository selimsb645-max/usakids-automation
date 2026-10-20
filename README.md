# USA Kids Automation

Autonomous nursery-rhyme / early-learning video factory for the
**USA Kids Channel** (youtube.com/@USAKidsChannel-m8g, account selimsb642@gmail.com).
Runs entirely on GitHub Actions free minutes - zero cost.

## How it works
- Deterministic lesson library (kids/lessons.py): ABC phonics, counting, colors, shapes.
  No LLM, no research calls, no stock footage: visuals are PIL-drawn colorful animations,
  voice is Kokoro TTS (af_heart), music bed is numpy-synthesized marimba.
- runner.py renders the next lesson in rotation, uploads via YouTube Data API
  (own OAuth client, refresh token in secret YT_TOKEN_JSON) as private + publishAt.
- Public slot: 18:30 Asia/Dhaka daily (= 8:30 AM ET, US kids morning).
- Production cron: 10:30 BD daily (04:30 UTC), 8h lead. Made for Kids flag set on upload.

## Secrets
- YT_TOKEN_JSON: full token json (client_id, client_secret, refresh_token, ...)
- ASSETS_GH_TOKEN: fine-grained PAT that can read the nextai-video-automation
  release (used to download the shared Kokoro voice model tarball)

## Manual dispatch
gh workflow run factory.yml -f mode=produce   # or selftest
