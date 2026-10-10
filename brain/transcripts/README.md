# TRANSCRIPTS — his published videos, his spoken words

How they got here (works any session, no help from him needed): Composio has HIS YouTube
account connected (channel UCoGcLab29YZoWbUiN4a1OBw). `COMPOSIO_SEARCH_TOOLS` → toolkit youtube →
`YOUTUBE_LIST_CAPTION_TRACK {video_id}` → `YOUTUBE_LOAD_CAPTIONS {id: <track id>, tfmt: srt}`
(owner-only endpoint — allowed because the videos are his). Full response lands in the Composio
sandbox (`/mnt/files/mex/this.json`); read it with `COMPOSIO_REMOTE_BASH_TOOL`. Every other route
(watch page, innertube, yt-dlp, transcript sites, Piped/Invidious) is bot-blocked from here.

Rule: before writing ANY line for him, read the transcript of the video it comes from. His
sentences beat generated ones (MEMORY §4/§5). Quote, don't paraphrase.

Files: one per video, `<videoId>_<slug>.md`. Pull more with the same two calls.
