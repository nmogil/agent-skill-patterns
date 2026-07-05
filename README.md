# agent-skill-patterns

Reusable design patterns for Agent Skills, packaged as portable `SKILL.md` folders you can sync into Claude Code, Hermes, or any harness that reads the Agent Skills format.

This is a pattern library, not a framework. Each skill is a self-contained folder; the scripts are thin stdlib-only helpers for validation and copying. Nothing here has runtime dependencies.

## Repo layout

```
skills/                        # one folder per skill, each with SKILL.md
  herdr-claude-pr-lane/        # run PR-sized Claude Code work through Herdr
  claude-code-goal-contract/   # turn vague asks into bounded contracts
  agent-verification-contracts/# verification loops per change type
  folder-agent-context/        # project-local CLAUDE.md + AGENTS.md
  agent-handoff/               # handoff artifacts for fresh sessions
scripts/
  validate_skills.py           # lint skill folders (frontmatter, naming, length)
  sync_skills.py               # copy skills to destinations (dry-run by default)
docs/
  design-principles.md         # the design notes behind these patterns
```

## Skill format

Every skill is a folder under `skills/` containing a `SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill            # must match the folder name
description: One or two sentences saying when to use this skill.
---

Body: concrete steps, templates, verification, pitfalls.
```

That's the whole contract. Harnesses load the description to decide relevance and read the body only when the skill fires (progressive disclosure — see `docs/design-principles.md`).

## Install / sync

Validate first, then sync. Both scripts are Python 3 stdlib only.

```sh
# lint all skills
python3 scripts/validate_skills.py

# preview what would be copied (dry-run is the default)
python3 scripts/sync_skills.py --to claude

# actually copy
python3 scripts/sync_skills.py --to claude --apply
python3 scripts/sync_skills.py --to all --apply

# custom destination(s)
python3 scripts/sync_skills.py --dest ~/some/agent/skills --apply
```

Default destinations:

- `--to claude` → `~/.claude/skills`
- `--to hermes` → `$HERMES_SKILLS_DIR` if set, else `~/.hermes/skills`
- `--to all` → both

Sync copies whole skill folders and overwrites files that changed. It does not delete destination skills. If a skill is removed from this repo, delete that destination folder manually after reviewing it.

## Operating principles

Short version — the full notes are in `docs/design-principles.md`:

1. **Small skills, one job each.** A skill that tries to cover everything never fires at the right moment. Split by decision point, not by topic area.
2. **Progressive disclosure.** The description is the trigger; the body is the payload. Keep descriptions honest about *when*, keep bodies short enough to read in one pass (target under ~160 lines).
3. **State-check before action.** Skills should tell the agent to verify current state (git status, existing files, running processes) before mutating anything.
4. **Verification is part of the work.** A change without a check is half a change. Every skill that produces output includes how to verify it.
5. **Portable by default.** No harness-specific APIs in skill bodies unless the skill is explicitly about that harness. Person- or machine-specific notes go in a clearly marked optional section.

## Adding a skill

1. `mkdir skills/my-skill` and write `skills/my-skill/SKILL.md` with the frontmatter above.
2. Keep it roughly 80–160 lines: trigger, steps, templates/commands, verification, pitfalls.
3. `python3 scripts/validate_skills.py` — fix anything it flags.
4. Sync.

## License

MIT — see `LICENSE`.
