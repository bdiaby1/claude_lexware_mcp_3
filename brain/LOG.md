# SESSION LOG — append-only, newest last. One entry per session that touched content work.

Format: `## YYYY-MM-DD — <topic>` · what happened · decisions · still open. Short lines,
facts only. Never edit old entries — correct with a new one.

---

## 2026-08-21 — Brain created

- Ingested the handoff package: master doc (29 June), VIDEO_ANALYSIS_BRIEF,
  Görli files (script v2, footage protocol, VO sheet, Kamara cut plan v3, 5 shorts),
  Berlin RvP (preproduction 16 Aug, script v1), KL-swap thumbnail mocks A/B/C.
- Built `brain/`: MEMORY (master doc §1–12+14 verbatim, §13 → STATE), STATE (current
  view + verbatim 29-June snapshot), this log, project folders, retention pipeline doc.
- Both .docx scripts converted to markdown via `tools/docx_table_script_to_md.py`
  (content verified byte-identical to the docx text except the table header row);
  original .docx kept next to them.
- Environment facts recorded: containers are ephemeral, only pushed git survives;
  ffmpeg/imagemagick are NOT preinstalled (install step added to the pipeline doc);
  pandoc absent by default too — the tools/ converter needs only Python stdlib.
- Decision: brain lives in this repo (`bdiaby1/claude_lexware_mcp_3`), branch pushed;
  root CLAUDE.md routes content sessions here; Lexware sessions unaffected.
- Not started: no video proxy / transcript received yet, so no retention analysis run.
- Open: the 5 questions at the top of STATE.md (swap publish status + curves,
  Mohammed/Ahmed, rough-cut status, Waldorf weekend, first analysis target).

## 2026-08-23 — Görlitzer video is live; packaging read

- Benjamin sent the link: https://youtu.be/3lO8b-jyFmg. Görli is PUBLISHED, title
  exactly as locked ("Before They Were Dealers - Germany's Most Dangerous Park").
  STATE.md updated — it is no longer "in post".
- Tested what this container can reach: yt-dlp is blocked (HTTP 429 / bot-check on the
  datacenter IP) — no cut, no auto-subs, no view count. Public oEmbed and the ytimg
  thumbnail URL DO work. Recorded in MEMORY §14 so no future session retries it.
- Read the published thumbnail (archived as `published_thumbnail.jpg`): split,
  FRIDAY 1PM mosque / FRIDAY 3PM park, no readable faces. Full analysis in
  `projects/goerlitzer/findings/2026-08-23_packaging-live.md`.
- Two durable rules earned → MEMORY §8, dated: (1) when the blur rule collides with
  the readable-eyes rule, blur wins and something else must carry the emotion — here,
  the timestamps; (2) the most cinematic frame of the shoot is not automatically the
  thumbnail (the blue-lit mosque needs explaining, 1PM/3PM does not).
- Still not run: any retention analysis. Blocked on Benjamin sending the Studio curve
  plus the 480p proxy and Scribe transcript. STATE questions renumbered around that.

