#!/usr/bin/env python3
"""Turn a raw talking-head recording into a 1080x1920 Reel/Short.

Does: center-crop to 9:16, loudness-normalise audio, burn in a hook title for the
first 3 seconds, burn in captions. Requires ffmpeg (with libass + drawtext).

Usage:
  python edit_video.py raw.mp4 out.mp4 --script queue/001_reels.json
  python edit_video.py raw.mp4 out.mp4 --script queue/001_reels.json --srt my.srt
  python edit_video.py raw.mp4 out.mp4 --hook "Your CEO won't text you gift cards"

Caption source, in order: --srt file > Whisper (if installed) > rough estimate
spread evenly over the clip from the script's SAY lines. The estimate will drift
from your real timing, so prefer --srt or Whisper for anything you publish.
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
# SRT styles use libass's default 384x288 canvas, which ffmpeg scales to the video
# (1920/288 = 6.67x for 1080x1920). Values below are in that canvas, not pixels:
# FontSize 10 ~ 66px, Outline 1 ~ 7px, MarginV 60 ~ 400px (clear of Reels/Shorts UI).
CAPTION_STYLE = (
    "FontName=DejaVu Sans,FontSize=10,Bold=1,PrimaryColour=&H00FFFFFF,"
    "OutlineColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0,"
    "Alignment=2,MarginV=60,MarginL=10,MarginR=10"
)


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def read_script(path):
    p = Path(path)
    d = json.loads(p.read_text(encoding="utf-8"))
    hook, say = None, []
    for line in d["content"].splitlines():
        if line.startswith("HOOK_TEXT:"):
            hook = line.split(":", 1)[1].strip()
        elif line.startswith("SAY:"):
            say.append(line.split(":", 1)[1].strip())
    return hook, " ".join(say)


def ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02}:{int(m):02}:{int(s):02},{int((s % 1) * 1000):03}"


def estimate_srt(text, total, lead_in=0.3, tail=0.5):
    """Fallback: spread 4-word chunks across the clip proportional to word count."""
    words = text.split()
    chunks = [" ".join(words[i:i + 4]) for i in range(0, len(words), 4)]
    span = max(total - lead_in - tail, 1.0)
    per_word = span / max(len(words), 1)
    t, lines = lead_in, []
    for n, c in enumerate(chunks, 1):
        d = per_word * len(c.split())
        lines.append(f"{n}\n{ts(t)} --> {ts(t + d)}\n{c}\n")
        t += d
    return "\n".join(lines)


def whisper_srt(video, outdir):
    """Use faster-whisper if the user has it installed; return SRT text or None."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    model = WhisperModel("base", compute_type="int8")
    segs, _ = model.transcribe(str(video), word_timestamps=True)
    words = [w for s in segs for w in s.words]
    lines, n = [], 1
    for i in range(0, len(words), 4):
        grp = words[i:i + 4]
        lines.append(f"{n}\n{ts(grp[0].start)} --> {ts(grp[-1].end)}\n"
                     f"{''.join(w.word for w in grp).strip()}\n")
        n += 1
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("out")
    ap.add_argument("--script", help="queue/NNN_reels.json (gives hook + caption fallback)")
    ap.add_argument("--hook", help="hook title text (overrides script)")
    ap.add_argument("--srt", help="your own SRT captions")
    ap.add_argument("--hook-seconds", type=float, default=3.0)
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found")
    font = next((f for f in FONT_CANDIDATES if Path(f).exists()), None)
    if not font:
        sys.exit("No bold font found; edit FONT_CANDIDATES")

    hook, spoken = (None, "")
    if args.script:
        hook, spoken = read_script(args.script)
    hook = args.hook or hook
    total = duration(args.raw)
    if total > 90:
        print(f"warning: clip is {total:.0f}s; Reels/Shorts work best under 60s")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if args.srt:
            srt = Path(args.srt).read_text(encoding="utf-8")
            source = "your SRT"
        elif (srt := whisper_srt(args.raw, tmp)) is not None:
            source = "Whisper"
        elif spoken:
            srt = estimate_srt(spoken, total)
            source = "ESTIMATED timing (check before posting!)"
        else:
            srt, source = None, "none"
        print(f"captions: {source}")

        shutil.copy(font, tmp / "font.ttf")
        vf = ["scale=1080:1920:force_original_aspect_ratio=increase", "crop=1080:1920", "setsar=1"]
        if hook:
            (tmp / "hook.txt").write_text(textwrap.fill(hook, 20), encoding="utf-8")
            vf.append(
                "drawtext=fontfile=font.ttf:textfile=hook.txt:fontsize=72:fontcolor=white:text_align=C:"
                "borderw=4:bordercolor=black:x=(w-text_w)/2:y=240:"
                f"enable='between(t,0,{args.hook_seconds})'")
        if srt:
            (tmp / "c.srt").write_text(srt, encoding="utf-8")
            vf.append(f"subtitles=c.srt:force_style='{CAPTION_STYLE}'")

        out = Path(args.out).resolve()
        raw = Path(args.raw).resolve()
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw),
             "-vf", ",".join(vf), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "160k", "-r", "30", "-movflags", "+faststart",
             str(out)], cwd=tmp)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
