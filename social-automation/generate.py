#!/usr/bin/env python3
"""Generate per-platform social drafts from topics.csv into an approval queue.

Usage:
  export ANTHROPIC_API_KEY=...
  python generate.py generate --ids 1 2 3 [--platforms linkedin x instagram]
  python generate.py generate --pillar bias_of_week --limit 5
  python generate.py list                      # show queue status
  python generate.py approve <draft_file>      # human sign-off (required to publish)
  python generate.py reject  <draft_file>

Nothing is ever published by this script; approved drafts are just marked so a
scheduler (Buffer/Typefully/API) can pick them up.
"""
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
QUEUE = HERE / "queue"
MODEL = os.environ.get("DRAFT_MODEL", "claude-sonnet-5-5")

PLATFORM_SPECS = {
    "linkedin": "LinkedIn post, 120-200 words, strong first line, short paragraphs, 3 hashtags max, end with a question.",
    "x": "X thread of 4-6 posts, each under 270 characters, numbered 1/, 2/ ... first post is the hook.",
    "instagram": "Instagram carousel: 6-8 slides. Output slide-by-slide text (max 20 words per slide), plus a caption under 100 words.",
}

SYSTEM = (
    "You are a cybersecurity educator writing social media content on the psychology of "
    "social engineering and security behavior. Be accurate and concrete. Never give "
    "operational attack instructions; describe how the manipulation works at a conceptual "
    "level and focus on defense. Do not invent statistics, named incidents, or citations. "
    "If a claim is uncertain, leave it out. Return only the post content."
)


def load_topics():
    with open(HERE / "topics.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def select(rows, args):
    if args.ids:
        wanted = {str(i) for i in args.ids}
        rows = [r for r in rows if r["id"] in wanted]
    if args.pillar:
        rows = [r for r in rows if r["pillar"] == args.pillar]
    if args.kids_only:
        rows = [r for r in rows if r["kids_safe"] == "yes"]
    return rows[: args.limit] if args.limit else rows


def build_prompt(row, platform):
    audience = "children aged 7-12 and their parents; simple words, no scary detail" if row["kids_safe"] == "yes" and row["pillar"] == "kids_family" else "working professionals and security-curious readers"
    return (
        f"Topic: {row['topic']} (origin: {row['origin']})\n"
        f"Hook idea: {row['hook']}\n"
        f"How attackers exploit it: {row['attack_scenario']}\n"
        f"Defensive action: {row['defense_action']}\n"
        f"Suggested hashtags: {row['hashtags']}\n"
        f"Audience: {audience}\n\n"
        f"Write: {PLATFORM_SPECS[platform]}"
    )


def cmd_generate(args):
    import anthropic  # imported lazily so list/approve work without the SDK

    client = anthropic.Anthropic()
    QUEUE.mkdir(exist_ok=True)
    for row in select(load_topics(), args):
        for platform in args.platforms:
            out = QUEUE / f"{int(row['id']):03d}_{platform}.json"
            if out.exists() and not args.force:
                print(f"skip {out.name} (exists)")
                continue
            msg = client.messages.create(
                model=MODEL,
                max_tokens=1200,
                system=SYSTEM,
                messages=[{"role": "user", "content": build_prompt(row, platform)}],
            )
            text = "".join(b.text for b in msg.content if b.type == "text").strip()
            out.write_text(json.dumps({
                "topic_id": row["id"],
                "topic": row["topic"],
                "platform": platform,
                "status": "pending",
                "created": datetime.now(timezone.utc).isoformat(),
                "fact_check_needed": True,
                "content": text,
            }, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"wrote {out.name}")


def cmd_list(_):
    for p in sorted(QUEUE.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        print(f"{d['status']:9} {p.name:24} {d['topic']}")


def set_status(path, status):
    p = Path(path)
    if not p.is_absolute() and not p.exists():
        p = QUEUE / p.name
    d = json.loads(p.read_text(encoding="utf-8"))
    d["status"] = status
    d[f"{status}_at"] = datetime.now(timezone.utc).isoformat()
    if status == "approved":
        d["fact_check_needed"] = False
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{p.name}: {status}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--ids", nargs="*", type=int)
    g.add_argument("--pillar")
    g.add_argument("--limit", type=int)
    g.add_argument("--kids-only", action="store_true")
    g.add_argument("--platforms", nargs="+", choices=PLATFORM_SPECS, default=list(PLATFORM_SPECS))
    g.add_argument("--force", action="store_true")
    g.set_defaults(fn=cmd_generate)
    sub.add_parser("list").set_defaults(fn=cmd_list)
    for name, status in (("approve", "approved"), ("reject", "rejected")):
        s = sub.add_parser(name)
        s.add_argument("file")
        s.set_defaults(fn=lambda a, st=status: set_status(a.file, st))
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
