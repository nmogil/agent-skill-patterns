---
name: herdr-claude-pr-lane
description: Use when starting or supervising PR-sized implementation work that Claude Code should execute via Herdr, with a separate supervising agent owning verification and merge decisions. Covers lane setup, prompt shape, checkpoints, and the supervisor/worker split.
---

# Herdr + Claude Code PR lane

Run one PR-sized unit of work per lane: Claude Code implements, the supervising
agent verifies and decides. Never let the same context both write and approve
the change.

## When this applies

- The work fits in one PR: a feature slice, a bugfix, a refactor with a clear boundary.
- A supervisor (separate agent or human) will review before merge.
- Not for: exploratory spikes (no PR contract yet — write a goal contract first,
  see `goal-contract`), or multi-PR epics (split them first).

## Roles

| Role | Owns | Must not |
|------|------|----------|
| Worker (Claude Code in Herdr lane) | Implementation, tests, self-check, PR description | Merge, expand scope, touch unrelated files |
| Supervisor (separate agent or human) | Verification, scope enforcement, merge/abandon call | Rewrite the code itself in the same pass |

## Steps

1. **Write the contract before opening the lane.** Goal, in-scope files/areas,
   out-of-scope, done-when, and verification commands. Use the
   `goal-contract` template. A lane started without a contract
   drifts — this is the single highest-leverage step.

2. **Start the lane** with the contract as the opening prompt. If running from a Herdr-managed pane, prefer a background split and avoid stealing focus:

   ```sh
   echo "$HERDR_ENV" "$HERDR_PANE_ID"   # expect HERDR_ENV=1
   herdr agent start pr-lane --cwd "$PWD" --split right --no-focus -- claude
   herdr agent send pr-lane "Read /tmp/contract.md and follow it exactly."
   herdr agent wait pr-lane --status idle --timeout 900000
   herdr agent read pr-lane --source recent --lines 200
   ```

   If your team uses a wrapper, substitute that command for `claude`. Include:
   - the branch name to create (one lane = one branch),
   - the exact verification commands the supervisor will run,
   - the instruction: "Do not merge. Stop and report when done-when is met or blocked."

3. **Let the worker run.** Don't interleave new asks into a running lane; queue
   them for the next lane. Mid-lane scope additions are how one PR becomes three.

4. **Checkpoint on stop.** When the worker reports done or blocked, the supervisor:
   - pulls the branch and runs the verification commands from the contract
     (not the ones the worker says it ran — the same list, executed fresh),
   - diffs against the in-scope list: `git diff --stat main...<branch>` — any
     file outside scope needs an explanation or a revert,
   - checks the done-when conditions one by one.

5. **Handle stuck lanes.** If the lane stops producing output or remains non-idle past the timeout, read recent output first, then decide whether it is blocked, still legitimately working, or dead. If dead, stop the lane/process you created, preserve any partial diff, and restart with a tighter contract rather than continuing to poke a stale session.

6. **Decide:** merge, send back with a specific correction ("test X fails with Y,
   fix only that"), or abandon the lane and restart with a tighter contract.
   Two failed correction rounds usually means the contract was wrong, not the worker.

## Prompt template (lane opener)

```
Branch: <branch-name>
Goal: <one sentence>
In scope: <files / dirs / behaviors>
Out of scope: <explicitly excluded things>
Done when:
  - <observable condition 1>
  - <observable condition 2>
Verify with:
  - <command 1>
  - <command 2>
Do not merge or push to main. Stop and report when done-when is met,
or immediately if blocked on a decision.
```

## Verification (supervisor side)

- Run every `Verify with` command yourself; require actual output, not claims. Use `agent-verification-contracts` for the evidence standard.
- `git diff --stat main...<branch>` — every touched file maps to the scope list.
- Read the diff for the riskiest file, not just the summary.
- If the worker added a dependency, config file, or migration not in the contract,
  treat it as scope drift even if it "helps".

## Pitfalls

- **Trusting the worker's own test report.** Workers report what they ran, in the
  state they ran it. Verify in a clean checkout of the branch.
- **Fat lanes.** If the contract has more than ~5 done-when items, it's multiple PRs.
- **Supervisor fixing code inline.** The moment the supervisor edits the branch,
  nobody is verifying. Send corrections back as instructions instead; only hotfix
  directly when abandoning the lane is more expensive.
- **Reusing a lane for the follow-up.** Fresh lane, fresh contract, fresh context.
  Long-lived lanes accumulate stale assumptions.
