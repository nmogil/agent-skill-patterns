# Design principles

The reasoning behind the patterns in `skills/`. Short by intent.

## Progressive disclosure

A harness loads every skill's `description` every session, but a skill's body
only when it fires. So the description carries the *trigger* ("use when...")
and the body carries the *payload* (steps, templates, checks). Costs follow the
same split: a bloated description taxes every session; a bloated body taxes
every invocation. Keep descriptions to 1–2 sentences about *when*, and bodies
under ~160 lines. If a body needs more, move the bulk to a `references/` file
inside the skill folder and link it — read only when needed.

## Capability vs process primitives

Two kinds of skills, don't mix them in one file:

- **Capability**: how to operate a tool or system (drive Herdr, call an API).
  Bodies are commands, flags, and gotchas. They change when the tool changes.
- **Process**: how to structure work regardless of tooling (goal contracts,
  handoffs, verification loops). Bodies are steps and templates. They change
  when you learn something about how work fails.

A mixed skill rots on two independent clocks and fires at the wrong moments.
When a process skill needs a capability, it links to the other skill rather
than inlining it.

## State-checks before action

Agents act on assumptions about current state that are one session stale.
Every skill that mutates anything starts by observing: `git status` before
editing, `ls` before creating, check the running process before restarting.
The check costs seconds; acting on a wrong assumption costs the session.
Corollary: skills should prefer idempotent steps, so a re-run after a partial
failure converges instead of compounding.

## Verification loops

The unit of agent work is not "make the change" but "make the change and
demonstrate it landed". Every pattern here ends with a verification section
because an unverified claim from an agent is a hypothesis with good posture.
The loop is always the same shape: state the check before the change, run the
real check after, read actual output, report evidence. Separating who writes
from who verifies (the worker/supervisor split in `herdr-claude-pr-lane`)
exists because self-verification degrades under exactly the conditions —
long sessions, sunk cost — where it matters most.

## Idea lifecycle coverage

The full workflow is broader than implementation. A useful chief-of-staff style
skill set should cover:

1. **Options** — widen the solution space before choosing (`chief-of-staff-brainstorm`).
2. **Critique** — challenge assumptions, tradeoffs, and failure modes (`critical-thinking-review`).
3. **First slice** — turn a selected idea into an executable experiment or plan (`idea-to-implementation-plan`).
4. **Contract** — bound the work before delegation (`goal-contract`).
5. **Execution** — run an implementation lane when appropriate (`herdr-claude-pr-lane`).
6. **Verification** — prove the result with real evidence (`agent-verification-contracts`).
7. **Continuity** — preserve context when work crosses sessions (`agent-handoff`).

Keep each stage separate. A brainstorming skill that also writes implementation
commands will fire too early; an implementation skill that also critiques strategy
will fire too late.

## Portable skills

A skill is a folder with a `SKILL.md`; frontmatter has `name` and
`description`. That's the whole format, and staying inside it is what makes
these syncable to any harness with a copy command. Consequences:

- No harness-specific APIs in process skills. Shell commands and file
  conventions travel; tool-call syntax doesn't.
- No personal or machine-specific content in skill bodies. If a note only
  applies to one person's setup, it goes in a clearly-marked optional section
  or their user-level config — never baked into the shared pattern.
- One skill, one job. Portability isn't just across machines but across
  situations: a focused skill fires precisely; a mega-skill fires always or
  never.

## What gets left out

Deliberately absent from this repo: skill dependency graphs, versioning
schemes, templating engines, install frameworks. A copy script and a linter
cover the actual need. Add machinery when a real failure demands it, not
before.
