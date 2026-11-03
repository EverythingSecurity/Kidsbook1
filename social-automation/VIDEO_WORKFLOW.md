# Talking-head Reels / Shorts workflow

## 1. Script
```bash
python generate.py generate --ids 1 --platforms reels     # or use the pilot scripts in queue/
python generate.py teleprompter queue/001_reels.json      # spoken lines only, paste into a teleprompter app
```
Review the script, fix facts, then `python generate.py approve queue/001_reels.json`.

## 2. Shoot (phone is fine)
- Vertical 9:16, 1080p, 30fps. Lens at eye level, window light in front of you (not behind).
- Frame chest-up with space above your head. Keep key content out of the top 250px
  (hook title goes there) and the bottom 450px (captions and platform UI).
- Record in a quiet room, phone mic 20-30cm away, or a cheap lav mic. Audio matters more than video.
- Do each script in 1-3 takes. Speak slightly faster than normal; leave 0.5s of silence at start and end.
- First sentence = the hook. Start talking immediately, no "hi guys".
- Optional: film the `BROLL:` cues as screen recordings of mock emails/prompts (use fake brands and
  domains only) and cut them in with your editor over the matching `SAY:` lines.

## 3. Edit
```bash
python edit_video.py raw.mp4 reel_001.mp4 --script queue/001_reels.json --srt my_captions.srt
```
Crops to 1080x1920, normalises loudness to -16 LUFS, burns in the hook title (first 3s) and captions.

Caption timing sources, best first:
1. `--srt` your own file (export from CapCut / Descript / YouTube Studio, or any transcriber).
2. Whisper, if `pip install faster-whisper` is available on your machine (automatic).
3. Fallback: estimated timing from the script. It WILL drift from your real speech; check before posting.

## 4. Review checklist before posting
- [ ] Facts match the script you approved; no invented stats or named incidents.
- [ ] Mock screens use fake brands/domains.
- [ ] Captions match what you actually said and are readable on a phone.
- [ ] Hook text is legible and not cut off; nothing important under the platform UI.
- [ ] Under 60s. Title + caption + hashtags copied from the script JSON.
- [ ] Reels: upload with caption. Shorts: upload with TITLE, add #Shorts.

## Pilot scripts
`queue/001_reels.json` (authority bias), `002_reels.json` (urgency), `008_reels.json` (MFA fatigue).
