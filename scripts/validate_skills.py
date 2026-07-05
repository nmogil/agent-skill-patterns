#!/usr/bin/env python3
"""Lint skills/*/SKILL.md: frontmatter shape, naming, length, banned terms."""
import os
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
MAX_DESCRIPTION_CHARS = 500
MAX_BODY_LINES = 200  # warning only; target is 80-160; 200 avoids noisy failures
BANNED = [t.strip() for t in os.environ.get("AGENT_SKILL_BANNED_TERMS", "").split(",") if t.strip()]


def parse_frontmatter(text):
    """Return (dict, body) or (None, text) if no frontmatter block."""
    text = text.lstrip("\ufeff")
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.DOTALL)
    if not m:
        return None, text
    fields = {}
    key = None
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if kv:
            key, fields[kv.group(1)] = kv.group(1), kv.group(2).strip()
        elif key and line.startswith((" ", "\t")):  # folded continuation line
            fields[key] += " " + line.strip()
    return fields, m.group(2)


def main():
    errors, warnings = [], []
    dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir()) if SKILLS_DIR.is_dir() else []
    if not dirs:
        errors.append(f"no skill folders found under {SKILLS_DIR}")

    for d in dirs:
        label = f"skills/{d.name}"
        skill_md = d / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{label}: missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")

        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{label}: SKILL.md has no YAML frontmatter block")
            continue
        if fm.get("name") != d.name:
            errors.append(f"{label}: frontmatter name {fm.get('name')!r} != folder name {d.name!r}")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{label}: frontmatter description missing or empty")
        elif len(desc) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{label}: description is {len(desc)} chars (max {MAX_DESCRIPTION_CHARS})")

        for term in BANNED:
            if re.search(term, text, re.IGNORECASE):
                errors.append(f"{label}: contains banned reference {term!r}")

        n_lines = len(body.splitlines())
        if n_lines > MAX_BODY_LINES:
            warnings.append(f"{label}: body is {n_lines} lines (target <= 160)")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s) in {len(dirs)} skill(s).")
        return 1
    print(f"OK: {len(dirs)} skill(s) valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
