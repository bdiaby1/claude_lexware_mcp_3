# BRAIN — Benjamin Diaby, persistent memory across Claude sessions

Why this exists: Claude Code sessions run in throwaway containers. Chat context dies
with the session. The only thing that survives is this git repository. So the memory
lives here — read at session start, written back before session end, **pushed**.
**Unpushed = forgotten.** That is the whole trick.

This directory is for Benjamin's content work (YouTube channel, shorts, Instagram,
video retention analysis). Lexware/bookkeeping/MCP-server sessions ignore it — their
instructions are the root `CLAUDE.md`.

## Layout

| Path | What | How it changes |
|---|---|---|
| `MEMORY.md` | Earned rules: brand engine, voice, playbooks, fact-check rules. His words. | Slowly. Additions dated, never rewritten. |
| `STATE.md` | Where everything stands NOW + open questions for Benjamin | Rewritten every session |
| `LOG.md` | Session journal | Append-only, newest last |
| `projects/<video>/` | Scripts, footage protocols, cut plans, thumbnails, `findings/` | As work happens |
| `pipelines/` | Reusable how-tos (video retention analysis) | Rarely |
| `tools/` | Small helper scripts (docx→md converter) | Rarely |

## Session protocol

**START — staged, cheapest first (same principle as the frame analysis: never read
everything blindly):**
1. This file.
2. `STATE.md` — current truth. If it lists open questions, ask them ONCE at the start,
   then write the answers back.
3. The relevant `projects/<x>/README.md` and only the files the task needs.
4. `MEMORY.md` — before any creative or packaging work, read it fully; otherwise grep
   the section you need (§2 engine, §4 voice, §6 fact-check/risk, §7 retention,
   §8 packaging, §9 shorts, §10 Instagram).

**END — mandatory whenever content state changed:**
1. Rewrite `STATE.md` to the new truth (answered questions out, new ones in).
2. Append one `LOG.md` entry: date · what happened · decisions · still open.
3. New artifacts into the project folder. Retention findings:
   `projects/<video>/findings/YYYY-MM-DD_<cutname>.md`.
4. A durable rule was earned (he corrected you, or data proved something)? → dated
   addition to the matching MEMORY.md section.
5. `git add brain/ && git commit && git push -u origin <branch>`. The session is not
   finished until the push succeeded.

## Hard rules

- **His words are the master.** MEMORY.md and everything under `projects/` keep his
  exact phrasing. The known failure mode is flattening his raw material into generic
  AI-smooth lines (MEMORY §5) — do not do it in the brain either.
- `LOG.md` is append-only. Never edit history; correct mistakes with a new entry.
- Mirror Benjamin's current language in chat (he switches German/English and corrects
  drift hard). Files stay in whatever language they were written in.
- Videos/frames/transcripts are working material, not memory: process them in the
  session scratchpad. Only the *findings* are committed. Never commit video files.
- Real names, faces and stories of vulnerable people appear in these files. Nothing
  from here leaves this repo (no external services, no other repos, no artifacts)
  unless Benjamin asks.
