# PACKAGING — published video, read from outside (2026-08-23)

Video is LIVE: https://youtu.be/3lO8b-jyFmg
Title as published: **"Before They Were Dealers - Germany's Most Dangerous Park"**
Channel: Benjamin Diaby (@benjamin-diaby)
Thumbnail archived: `../published_thumbnail.jpg` (1280×720)

What this is: a packaging read only. No retention analysis — the cut itself could not
be reached from here (see LIMIT below). Views, watch time and the retention curve are
invisible to Claude; they have to come from Benjamin as YouTube Studio screenshots.

## The thumbnail

Split frame, torn/perforated white divider. Left, white text **FRIDAY 1PM**: mosque
interior, warm gold light, ornament and chandelier, a Black man shot from behind in an
orange shirt and red-white cap, shoe racks in the foreground. Right, yellow text
**FRIDAY 3PM**: the park in daylight, green, two young Black men walking, faces blurred.

### Against the locked rules (MEMORY §8)
- **Title and thumbnail split the work — they never repeat each other.** ✓ Cleanly.
  Title carries the thesis ("before they were dealers"), thumbnail carries the
  contradiction ("1PM / 3PM"). Neither says what the other says.
- **Real frames, never AI.** ✓
- **Split with a divider, minimal text.** ✓ (Divider is a torn edge rather than the
  hard white line of the swap thumb — a variation, and it reads.)
- **Mobile first half of the title must grip alone.** ✓ "Before They Were Dealers"
  survives truncation and is the strongest half.
- **Click must equal payoff.** ✓ The 1PM/3PM claim is exactly VO block 3 and Short 1
  ("Same men. Same day.") — the video delivers it, and Kamara's faith answer closes it.

### The one real deviation — and it was the right call
§8 says: zoom until the **eyes are readable** at 320px. This thumbnail has no readable
eyes anywhere — the left man is shot from behind, the right two are blurred.

That is not sloppiness, it is §6 winning: consent before faces, blur everyone who
refused. On this kind of video the two rules collide and **blur has to win**. The
thumbnail solves it by replacing the face as the emotional carrier with the TIME
STAMPS — 1PM/3PM does the work eyes usually do. Worth keeping as a pattern.

### Deviation from the plan, also an improvement
The footage protocol nominated "the mosque lit blue by twenty police cars" as the
thumbnail candidate. That image is the most cinematic frame of the shoot, but it needs
a sentence of explanation to land. 1PM/3PM lands in half a second with no explanation.
The stronger *film* image was not the stronger *thumbnail* image — good instinct.

### One honest flag
Visually the left man and the right two men are not identifiably the same people (by
design — no faces). The picture asserts "same men" that it cannot itself prove; the VO
is careful and says "some of them". That is normal thumbnail compression and inside
"exaggerate for attention, never false claims" (§6) — but it is the one line where a
hostile comment could get traction. Answer is in the video, so it holds.

## LIMIT — what could not be done from here (verified 2026-08-23)
- yt-dlp on this container gets HTTP 429 and "Sign in to confirm you're not a bot" —
  YouTube blocks the datacenter IP. No video, no auto-subtitles, no view count.
- Public oEmbed works and returns title + channel + thumbnail URL. That is all.
- **So the pipeline input stays as designed:** Benjamin sends the 480p proxy + the
  ElevenLabs Scribe transcript into the chat. Do not spend another session trying to
  pull the cut from YouTube.
