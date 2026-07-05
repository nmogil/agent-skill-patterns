---
name: folder-agent-context
description: Use when deciding whether a project or subdirectory needs its own agent context file, and how to set it up - a project-local CLAUDE.md with an AGENTS.md symlink so multiple harnesses read the same instructions.
---

# Folder-level agent context

One context file per project, maintained like code, symlinked so every harness
reads the same one. The file exists to prevent repeated mistakes, not to
document the project — that's what the README is for.

## When to add one

Add a `CLAUDE.md` when at least one of these is true:

- An agent made the same mistake twice in this repo (wrong test command, touched
  generated files, missed a convention).
- The repo has non-obvious invariants: "never edit `src/gen/`", "migrations are
  append-only", "this deploys from `release/`, not `main`".
- The build/test/run commands aren't discoverable from standard files
  (package.json scripts, Makefile) alone.

Don't add one when the repo is small and standard — an empty or obvious context
file is noise the agent must read every session. YAGNI applies.

## Setup

```sh
cd path/to/project
$EDITOR CLAUDE.md                 # write the content, see template below
ln -s CLAUDE.md AGENTS.md         # other harnesses (Codex, etc.) read AGENTS.md
git add CLAUDE.md AGENTS.md
```

The symlink makes CLAUDE.md the single source of truth; edits propagate to
every harness automatically. If a harness on your platform can't follow
symlinks, fall back to a one-line AGENTS.md: "See CLAUDE.md" — worse, but works.

For subdirectories in a monorepo: nested `CLAUDE.md` files apply to work under
that directory. Only add one where the subproject's rules genuinely differ from
the root's; duplicating the root file per package is maintenance debt.

## Content template

Keep it under ~60 lines. Every line should change agent behavior; delete lines
that merely describe.

```markdown
# <project> — agent context

## Commands
- test: <exact command>
- lint/typecheck: <exact command>
- run locally: <exact command>

## Invariants (do not violate)
- <e.g. never edit src/gen/** — regenerate with `make codegen`>
- <e.g. DB migrations are append-only>

## Conventions
- <e.g. errors are returned, not thrown, in core/>
- <only conventions an agent got wrong or would get wrong>

## Gotchas
- <e.g. tests need the daemon running: `make dev` first>
```

## Maintenance

- **Write rules from incidents.** The best entries are postmortems in one line:
  agent did X wrong → add the rule that would have prevented it.
- **Prune on contact.** Reading the file and finding a stale command? Fix it in
  the same commit as your change. A context file with one wrong command loses
  the agent's trust in all of them.
- **Review it in PRs** like any other file. Rules nobody reviewed become rules
  nobody follows.

## Pitfalls

- **The kitchen-sink file.** Architecture essays, style guides, aspirational
  process. Agents read this every session — every non-actionable line taxes
  every future task. Link out instead of inlining.
- **Secrets or personal details.** The file ships with the repo. Machine-specific
  paths, tokens, or private context belong in your user-level config, not here.
- **Duplicating what tools already say.** If `package.json` has the scripts and
  they're standard, don't restate them; state only the surprising ones.
- **Forgetting the symlink is committed.** `ln -s` then not adding AGENTS.md to
  git means only your machine has it.
