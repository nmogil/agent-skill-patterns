---
name: agent-verification-contracts
description: Use whenever an agent is about to claim work is done — code, docs, UI, or data changes. Defines the verification loop per change type - run the check, observe real output, and only then claim success. Evidence before assertions.
---

# Verification contracts

An agent's claim of "done" is a hypothesis. The verification contract is the
experiment that tests it. Every change type has a minimum loop; run it before
reporting success, and report the actual output, not a summary of confidence.

## The universal loop

1. **State the check before making the change.** "This is done when command C
   prints X." If you can't state it, the change isn't specified yet.
2. **Make the change.**
3. **Run the check — the real one.** Fresh process, clean state, the command a
   skeptical reviewer would run. Not "it should work because the code is right."
4. **Read the output.** Exit code AND content. A passing exit code with an error
   in stderr is a failure.
5. **Report with evidence.** Paste the command and the relevant output lines.
   If it failed, say it failed — a truthful failure report is a successful turn.

## Per change type

### Code

- Run the narrowest test that exercises the change, then the suite the repo's CI runs.
- If no test covers it, write the smallest one that fails without your change —
  then verify it fails on the old code and passes on the new (red/green).
- Type-check and lint if the repo does. `tsc`/`mypy` passing is necessary, never sufficient.
- For behavior changes: exercise the actual entry point (CLI invocation, HTTP
  request, function call in a REPL), not just the unit around it.

### Docs

- Every command in the doc: execute it, verbatim, in a directory state a reader
  would plausibly be in. Docs rot at the commands first.
- Every path, flag, and identifier: check it exists (`ls`, `--help`, grep the source).
- Links: resolve them (curl -sI, or open the file for relative links).
- Read the doc top-to-bottom once as the target reader; missing prerequisites
  hide from the author.

### UI

- Load the changed screen in the actual app (dev server, simulator, browser) and
  look at it — screenshot if the harness supports it. Rendering is the test.
- Exercise the interaction, not just the render: click the button, submit the
  form, trigger the error state.
- Check the browser/app console for new errors even when the screen looks right.
- Verify the states you didn't design for: empty data, long strings, loading, error.

### Data (migrations, backfills, ETL)

- Row counts before and after, and the expected delta stated in advance.
- Spot-check N concrete records end to end, including at least one edge case
  (nulls, oldest record, unicode).
- Run an aggregate invariant that must not change (sum of balances, count per
  status) — checksum the things the change must not touch.
- Dry-run against a copy first when the operation is destructive; verify the
  rollback path exists before you need it.

## Verifying another agent's work

Same loops, plus:

- Re-run the checks yourself; never accept the worker's transcript as evidence.
- Diff the full change surface (`git diff --stat`) against the stated scope —
  verify what was touched, not just what was reported.
- Pick the riskiest file and read it, even if all checks pass. Checks catch
  regressions; reading catches wrong-but-passing.

## Pitfalls

- **Verification theater.** Running a check that can't fail (linting a doc change,
  compiling after a comment edit) and presenting it as evidence.
- **Testing the mock.** The unit test passes because it mocks the exact thing you
  changed. Exercise one level above the change.
- **Stale state.** The old process/build/cache is still running and you verified
  that. Restart, rebuild, hard-reload before trusting output.
- **Summarizing instead of quoting.** "Tests pass" hides the two skips and one
  warning. Quote the summary line of the actual run.
- **Verifying only the happy path.** The change is judged by its worst state,
  not its demo state.
