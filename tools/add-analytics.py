#!/usr/bin/env python3
"""Add the shared analytics loader to every page's <head>.

Safe to re-run: pages that already have the tag are skipped. Run it after
adding a new page that was not built from the blog templates, then commit.
Demo pages are left out on purpose.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TAG = '<script src="/analytics.js" defer></script>'
SKIP = {"demos"}

added = skipped = 0
for path in sorted(ROOT.rglob("*.html")):
    rel = path.relative_to(ROOT)
    if rel.parts[0] in SKIP or rel.parts[0].startswith("."):
        continue
    text = path.read_text(encoding="utf-8")
    if TAG in text:
        skipped += 1
        continue
    if text.count("</head>") != 1:
        print(f"skip (expected one </head>): {rel}")
        continue
    path.write_text(text.replace("</head>", TAG + "</head>", 1), encoding="utf-8")
    added += 1
    print(f"added: {rel}")

print(f"done: {added} added, {skipped} already had it")
