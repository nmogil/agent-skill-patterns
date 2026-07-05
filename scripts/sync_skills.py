#!/usr/bin/env python3
"""Copy skills/ folders to agent skill directories. Dry-run by default."""
import argparse
import filecmp
import os
import shutil
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

NAMED_DESTS = {
    "claude": Path.home() / ".claude" / "skills",
    "hermes": Path(os.environ.get("HERMES_SKILLS_DIR", Path.home() / ".hermes" / "skills")),
}


def sync_skill(src, dest_dir, apply):
    """Copy one skill folder; return list of changed file paths."""
    changed = []
    for f in sorted(p for p in src.rglob("*") if p.is_file()):
        target = dest_dir / src.name / f.relative_to(src)
        if target.is_file() and filecmp.cmp(f, target, shallow=False):
            continue
        changed.append(target)
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
    return changed


def extra_skills(dest_dir, source_names):
    """Destination skill folders that are not managed by this repo."""
    if not dest_dir.is_dir():
        return []
    return sorted(
        d for d in dest_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file() and d.name not in source_names
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--to", action="append", choices=[*NAMED_DESTS, "all"], default=[],
                    help="named destination (repeatable)")
    ap.add_argument("--dest", action="append", type=Path, default=[],
                    help="explicit destination directory (repeatable)")
    ap.add_argument("--apply", action="store_true",
                    help="actually copy files (default: dry-run)")
    args = ap.parse_args()

    targets = list(args.dest)
    names = set(args.to)
    if "all" in names:
        names = set(NAMED_DESTS)
    targets += [NAMED_DESTS[n] for n in sorted(names)]
    if not targets:
        ap.error("no destination: pass --to claude|hermes|all and/or --dest PATH")

    skills = sorted(d for d in SKILLS_DIR.iterdir()
                    if d.is_dir() and (d / "SKILL.md").is_file())
    if not skills:
        print(f"no skills found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    verb = "copy" if args.apply else "would copy"
    source_names = {s.name for s in skills}
    for dest in targets:
        print(f"==> {dest}")
        for skill in skills:
            changed = sync_skill(skill, dest, args.apply)
            if changed:
                print(f"  {verb} {skill.name} ({len(changed)} file(s))")
            else:
                print(f"  up-to-date {skill.name}")
        extras = extra_skills(dest, source_names)
        if extras:
            print("  note: other destination skills left untouched: " + ", ".join(e.name for e in extras))

    if not args.apply:
        print("\ndry-run: no files written. Re-run with --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
