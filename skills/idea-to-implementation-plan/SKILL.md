---
name: idea-to-implementation-plan
description: Use after an idea has survived brainstorming and critical review, when it needs to become an executable plan, experiment, PR sequence, or delegation contract. Bridges strategy into implementation without overbuilding.
---

# Idea to implementation plan

This is the bridge from thinking to doing. Use it to convert a selected idea into a concrete first slice, not a grand roadmap.

## Trigger

Use when:

- the user picks an idea and wants to move toward execution,
- a brainstorm needs a concrete next step,
- a critique produced changes that must be incorporated,
- a product/workflow opportunity should become a PR, experiment, or operating task.

## Process

1. **Define the outcome.** What will be different when this works?
2. **Pick the smallest valuable slice.** Prefer a reversible proof, thin vertical PR, or manual test over a platform rewrite.
3. **Set non-goals.** Explicitly exclude tempting adjacent work.
4. **Choose the execution mode.** One of:
   - manual/operator test,
   - document or decision memo,
   - single PR,
   - multi-PR sequence,
   - scheduled/recurring workflow,
   - user decision needed first.
5. **Write acceptance criteria.** Observable done-when bullets, not vibes.
6. **Define verification.** Commands, checks, screenshots, metrics, review gates, or real-world evidence.
7. **Identify ownership.** What the orchestrator owns, what the implementer owns, and what the user must decide.
8. **Hand off to the next skill.** Use:
   - `goal-contract` for vague/multi-step implementation,
   - `herdr-claude-pr-lane` for visible PR-sized Claude Code work,
   - `agent-verification-contracts` before claiming done,
   - `agent-handoff` if stopping midstream.

When execution mode is a PR, the acceptance criteria and verification here become the `goal-contract` done-when and verify-with sections. Transfer them; do not rewrite a second competing contract.

## Output shape

```markdown
## Selected idea
<one sentence>

## First slice
<smallest valuable implementation or experiment>

## Non-goals
- <not doing>
- <not doing>

## Execution mode
<manual test / doc / PR / multi-PR / scheduled workflow / decision needed>

## Acceptance criteria
- [ ] <observable outcome>
- [ ] <observable outcome>

## Verification
- <command/check/evidence>

## Owner split
- Orchestrator: <scope>
- Implementer: <scope>
- User decision: <if any>

## Next action
<exact next step or contract to write>
```

## Quality bar

- The first slice should be small enough to verify in one sitting when possible.
- Do not turn every idea into software; sometimes the next step is a memo, call, landing page, or manual test.
- Preserve decision context so implementers do not rebuild rejected alternatives.
- Prefer evidence-generating work over polish when uncertainty is high.

## Pitfalls

- **Roadmap inflation:** converting one idea into a quarter-long plan before proof.
- **Implementation leap:** skipping assumptions and acceptance criteria.
- **No kill criteria:** experiments that cannot fail are not experiments.
- **Ownership blur:** letting a child agent decide product or business tradeoffs that require the user.
