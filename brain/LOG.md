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


## 2026-09-12 — Istanbul: script into the brain, first retention analysis run

- New project: Istanbul / Tahsin, "He Eats From the Trash of Istanbul's Rich". Benjamin
  pasted the full script + 3-shorts brief in chat on 11 Sep; both saved verbatim to
  `projects/istanbul/` — they existed nowhere else and would have died with the session.
- He sent a 50-second screen recording of the first cut (played from Drive). **First
  time the retention pipeline actually ran end to end.**
- Method notes worth keeping (added to the pipeline doc): a screen recording needs
  cropping to the video area first (here 1152x648 inside 1512x648, pillarboxed); and
  scene detection at the standard 0.3 threshold UNDER-REPORTS cuts in very dark
  footage — it claimed a 6.8s static hold that a 0.12 pass showed was five cuts.
  Checking that before reporting saved a wrong headline finding.
- Findings: `projects/istanbul/findings/2026-09-12_hook-cut-50s.md`. Pace is good
  (~19 cuts/30s, his 4-second rule holds everywhere). The real problems are order and
  picture choice: the knife story — his scripted line one — starts at 0:17 behind a
  wordless montage; the payoff line "You give me money." sits on a wide of him in a
  park instead of on Tahsin; "Tonight I pulled it with him" sits on a taxi; the closing
  promise sits on the weakest frame in the cut. Plus: bin-climb and 50kg lift are both
  on his own hook shot list and absent; the coffee terrace is spent twice.
- Flagged for him, not changed: the knife shot at 0:19.5 is an unlabelled re-enactment
  cut among real footage — brand risk against "real frames only", his call.
- Still open: whether this 50s is the whole hook or an excerpt; the rest of the cut;
  and the Görli retention curve, which has now been outstanding since 23 Aug.

## 2026-09-29 — Rio day clip: format call + "such tool das du es kannst"

- Benjamin asked whether rio_day.mp4 is a Reel, a Story, or nothing — and told me to
  find a tool so I can actually see it (older chat-me had said "I can't watch frames";
  that belief is wrong and now retired — this is the 3rd video I've read via ffmpeg).
- Ran the pipeline on the 33s vertical clip. It is NOT a throwaway: full engine in 33s
  — resort + Land Rover + helicopter (wealth) vs a warm laughing moment with an older
  man in green + a person sleeping at the luxury fence (the invisible).
- Verdict: green-shirt-man moment is Reel/short gold if more footage exists; the clip
  as-is → Story into the "On the road" highlight; not a standalone Reel (no single
  spine). Flagged dignity/consent on the fence-sleeper (face down / not identifiable
  in the frame checked, so defensible, but §6 applies for anything permanent).
- New brain folder `projects/instagram-highlights/` holds the "On the road" concept,
  the format rules agreed in chat (15s story split, Reel vs Story, no explaining
  caption, no self-diminishing text), and the Rio verdict.
- Still open (unchanged): Görli retention curve (since 23 Aug), Istanbul rest-of-cut,
  and whether the Istanbul 50s was hook or excerpt.
