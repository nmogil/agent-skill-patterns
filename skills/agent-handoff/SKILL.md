---
name: agent-handoff
description: Use when ending a session with unfinished work, or when work must move to a fresh agent session or a different agent. Produces a concise handoff artifact so the next session starts working in minutes instead of re-deriving context.
---

# Agent handoff

A fresh session knows nothing you learned this session. The handoff artifact is
the diff between "what the repo shows" and "what's in your head" — write only
that diff. Everything discoverable from the code, git log, or tracker doesn't
belong in it.

## When this applies

- Context is running long and the work will continue in a new session.
- Handing work from one agent/harness to another (Claude Code → Hermes, or vice versa).
- Pausing multi-day work where future-you is effectively a different agent.
- Skip it when the work is done (write a summary/PR description instead) or when
  the next step is trivially obvious from `git status`.

## The artifact

One file, checked into the work branch (or the tracker ticket if there's no
branch): `HANDOFF.md` at the repo root, or `docs/handoffs/<date>-<topic>.md`
for repos that accumulate them. Target 20–40 lines. If it's over 60, you're
documenting the project, not the delta.

```markdown
# Handoff: <topic> (<date>)

## Goal
<one sentence — the contract this work is under, link it if it exists>

## State
- Done: <what is complete AND verified — note how it was verified>
- In progress: <the exact thing mid-flight, and where the edit point is: file:line>
- Not started: <remaining known work, in intended order>

## Next action
<the single concrete step the next session should take first —
 a command to run or a file to open. Not a paragraph of options.>

## Landmines
- <things tried that failed, and why — the most valuable section>
- <non-obvious constraints discovered: "X must init before Y", "test T is flaky">

## Verify
- <commands that confirm current state: what passes today, what is expected to fail>
```

## Writing it well

1. **Write "Next action" first.** It forces you to decide where the work actually
   stands. If you can't name the next action, the handoff isn't ready — resolve
   the ambiguity now, while you still have context.
2. **Landmines over achievements.** "Tried the async approach; deadlocks because
   the pool is shared" saves the next session hours. "Refactored cleanly" saves
   nothing.
3. **Distinguish verified from believed.** "Tests pass (ran `pytest`, 42 passed)"
   vs "should work". The next session must know which claims to trust.
4. **Anchor to stable references.** file:line, commit hashes, exact command
   strings — not "the function we discussed" or "the earlier approach".
5. **Run the Verify commands before writing them down.** A handoff whose
   stated-passing check fails on arrival poisons the whole artifact.

## Picking it up (next session)

1. Read the handoff, then run its Verify commands before anything else. Mismatch
   between claimed and actual state? Trust the actual state and re-plan.
2. Do the Next action.
3. Delete or archive the handoff once absorbed — a stale HANDOFF.md at repo root
   actively misleads every future session that reads it.

## Pitfalls

- **The transcript dump.** Pasting session history is not a handoff; the next
  agent drowns. Distill or don't bother.
- **Optimistic state.** Listing in-progress work under "Done" is the most common
  and most expensive handoff bug. When unsure, downgrade.
- **Handoff as diary.** Nobody needs the journey ("first I looked at..."). State,
  next action, landmines.
- **Orphaned artifacts.** Handoffs left behind after the work ships become
  landmines themselves. Absorbing session deletes it.
