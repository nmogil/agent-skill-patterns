---
name: reviewr-manual-review
description: Use when opening, operating, or responding to Noah's Herdr Reviewr manual review flow for code, plans, or Obsidian note edits.
---

# Reviewr Manual Review

Reviewr (`persiyanov.reviewr`) is Noah's Herdr-native manual review/comment surface. It shows Git diffs, lets Noah leave line comments, and sends those comments back into the agent input when he presses `s`.

## When to open Reviewr

Open a visible Reviewr pane when either:

- Noah explicitly asks, e.g. “open Reviewr pane for me to review the changes once complete”; or
- the code, plan, or Obsidian-note change is important enough that Noah should manually review it before handoff.

Do **not** open Reviewr for every tiny edit unless Noah asked for that; use judgment and keep it useful.

## Correct invocation

Run `reviewr` from the Git repo/worktree whose diff Noah should review:

```bash
cd /path/to/repo
reviewr
```

The `/root/.local/bin/reviewr` wrapper is preferred over direct plugin commands because it opens Reviewr as a split targeted at the active agent pane when possible. That makes Reviewr's `s` / Send action resolve an unambiguous same-tab agent target.

## Critical Herdr rule

Reviewr Send works only when Reviewr can resolve:

1. an agent in the same tab, or
2. exactly one agent in the workspace.

Therefore:

- Open Reviewr from the target Claude/Hermes agent pane.
- Do not move an already-running Reviewr pane between tabs; its process keeps the original `HERDR_TAB_ID`.
- If Send fails with `agent failed: no unambiguous agent in this tab or workspace`, close the Reviewr pane and reopen it from the target agent pane with `reviewr`.

## Obsidian notes

For Noah's Obsidian vault, Reviewr uses a local-only Git baseline:

```bash
cd /root/obsidian
reviewr
```

Guardrails:

- Obsidian Sync remains the source of truth.
- Do not add a remote to `/root/obsidian` unless Noah explicitly asks.
- Track/review `99_Hermes/` by default; expand scope only when Noah asks.
- Avoid destructive Git commands in `/root/obsidian` (`reset --hard`, `checkout .`, `clean -fd`) unless Noah explicitly approves.

## Acting on Reviewr comments

When Noah sends comments from Reviewr, they arrive in the agent input as lines like:

```text
path/to/file.md:14
comment text
```

Treat those as the immediate action list:

1. Read the referenced file/lines.
2. Apply the requested changes.
3. Re-run relevant verification.
4. Reopen or refresh Reviewr if another review pass is needed.
5. Summarize what changed and which comments were addressed.

## Useful checks

Check same-tab agent resolution:

```bash
herdr pane list
herdr agent list
```

A healthy Reviewr send setup has Reviewr and exactly one target agent in the same tab.
