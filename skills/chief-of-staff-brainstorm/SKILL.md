---
name: chief-of-staff-brainstorm
description: Use when a user brings a rough goal, opportunity, product idea, or "what should we do?" prompt and needs high-quality options before choosing a direction. Expands the solution space without committing to implementation.
---

# Chief-of-staff brainstorm

Use this before planning or implementation when the request is still exploratory. The goal is not to produce a giant idea list; it is to create a useful option set that can be challenged, narrowed, and acted on.

## Trigger

Use when the user asks to:

- brainstorm, explore, ideate, or think through possibilities,
- decide what to build next,
- find opportunities, growth loops, product ideas, or workflow improvements,
- turn a vague ambition into concrete candidate paths.

Do not use for already-scoped implementation work; use `goal-contract` or an implementation lane instead.

## Process

1. **Restate the aim.** One sentence: what outcome are we optimizing for?
2. **Name the constraints.** Time, budget, audience, distribution, technical access, risk, and anything the user explicitly ruled out.
3. **Generate across lanes, not one blob.** Produce 3–6 buckets such as:
   - fast/manual,
   - productized/self-serve,
   - engineering/system,
   - distribution/growth,
   - operational/process,
   - wild-card/high-upside.
4. **Make each idea actionable.** For every candidate include:
   - what it is,
   - why it could work,
   - what makes it hard,
   - first test or next action,
   - what evidence would kill it.
5. **Rank by fit.** Score or sort by expected upside, effort, confidence, and reversibility.
6. **Recommend a short list.** Pick 1–3 to move into `critical-thinking-review` or `idea-to-implementation-plan`.

## Output shape

```markdown
## Aim
<one sentence>

## Constraints / assumptions
- <constraint>
- <assumption>

## Options
| Option | Why it might work | Risk / friction | First test | Kill signal |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Recommendation
1. <best next option> — why
2. <backup option> — why

## Next action
<the smallest useful next step>
```

## Quality bar

- Include at least one boring/practical option and one non-obvious option.
- Do not invent fake evidence, customer demand, or financial projections.
- Avoid premature implementation detail until the option is selected.
- Prefer ideas the requester can actually execute or delegate.

## Pitfalls

- **Idea confetti:** too many options with no ranking or next step.
- **Single-track thinking:** only improving the user's first idea instead of widening the field.
- **False certainty:** presenting speculative ideas as validated facts.
- **Hidden dependency:** suggesting options that require access, data, or authority the team does not have.
