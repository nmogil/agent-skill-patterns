---
name: goal-contract
description: Use when a work request is vague, open-ended, or bigger than one sitting — before any implementation. Converts "improve X" / "add support for Y" into a bounded contract with scope, non-goals, done-when conditions, and stop conditions.
---

# Goal contract

A goal contract turns "make it better" into something an agent can finish.
Write it before touching code. If you can't fill in "done when", you don't
understand the task yet — and neither will the agent.

## When this applies

- The request uses words like improve, clean up, modernize, support, robust.
- The request is concrete but large ("migrate the API to v2") — contract per slice.
- You're about to hand work to another agent or a fresh session.
- Skip it when the request is already a contract ("rename function X to Y in file Z").

## The contract

```
Goal: <one sentence, outcome not activity>
Context: <2-3 lines: why now, what exists, links to prior art>
In scope: <files, dirs, behaviors that may change>
Out of scope: <the tempting adjacent work that must NOT happen>
Done when:
  - <observable condition — a command that passes, a behavior demonstrable in the app>
  - <...max ~5. More means split it.>
Verify with:
  - <exact commands, or manual steps with expected output>
Stop conditions:
  - Blocked on a decision only the requester can make
  - Done-when met
  - <budget: e.g. "2 correction rounds" or "stop if this requires schema changes">
```

## How to fill it in

1. **Goal as outcome.** "Users can reset passwords via email" not "add password
   reset logic". If the goal names an activity, keep asking "so that what?"

2. **Done-when must be observable.** Each condition is checkable by someone who
   didn't do the work: a command with expected output, a URL that renders, a test
   that passes. "Code is cleaner" is not a condition; "pylint score ≥ previous"
   is.

3. **Out of scope is the load-bearing section.** Write down the adjacent work the
   agent will be tempted to do: the refactor next to the fix, the dependency
   upgrade, the "while I'm here" test cleanup. Naming it is what prevents it.

4. **Stop conditions cap the downside.** The failure mode of agent work isn't
   wrong code — it's an agent burning hours past the point where a human should
   have been consulted. Always include a blocked-on-decision stop and a budget.

5. **Size check.** A contract should be completable in one focused session and
   reviewable in one sitting. If done-when has >5 items or in-scope spans >~10
   files, split into multiple contracts and sequence them.

## Example

Request: "the CLI error handling is bad, improve it"

```
Goal: CLI failures print a one-line actionable error instead of a traceback.
Context: users see raw stack traces on config/network errors; tracebacks should
  remain available behind --debug.
In scope: cli/main.py, cli/errors.py (new), tests/test_cli_errors.py
Out of scope: library-internal exception hierarchy, logging format, retry logic.
Done when:
  - `mycli --config missing.toml` prints "config not found: missing.toml" and exits 2
  - `mycli --debug --config missing.toml` prints the full traceback
  - existing test suite passes
Verify with:
  - python -m pytest tests/ -x
  - the two commands above, output eyeballed
Stop conditions: blocked, done, or if fixing this requires changing >2 call sites
  outside cli/.
```

## Pitfalls

- **Contract as ceremony.** If writing it takes longer than the task, the task
  didn't need one. This is for vague or delegated work, not every edit.
- **Done-when written after the fact.** Conditions invented to match what was
  built verify nothing. Write them first, then implement.
- **No non-goals.** A contract without an out-of-scope section is a wish, not a
  contract — scope drift is the default, not the exception.
- **Vague verification.** "Tests pass" — which tests, run how? Paste exact commands.
