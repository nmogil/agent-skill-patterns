---
name: critical-thinking-review
description: Use before committing to a recommendation, plan, product idea, PR direction, or operating decision with meaningful cost or risk; skip small reversible choices. Challenges assumptions and failure modes so weak ideas are improved or killed early.
---

# Critical-thinking review

This is the "grill the idea" step. Use it after brainstorming and before a decision, plan, or implementation contract.

## Trigger

Use when:

- a plan sounds plausible but has not been challenged,
- the user asks for critique, red-team, second-order thinking, or "what are we missing?",
- an agent is about to recommend a direction with meaningful cost/risk,
- a product/workflow idea needs refinement before implementation.

## Review loop

1. **State the proposal neutrally.** Do not defend it yet.
2. **List key assumptions.** Separate facts, assumptions, and guesses.
3. **Attack the weak points.** Ask:
   - What has to be true for this to work?
   - Where could this fail despite good execution?
   - What incentives, users, or systems might resist it?
   - What are we underestimating?
   - What would make this not worth doing?
4. **Argue the opposite.** Write the strongest case against the proposal.
5. **Compare alternatives.** Include the do-nothing/default path when relevant.
6. **Classify the decision.** Reversible vs irreversible, cheap vs expensive, urgent vs optional.
7. **Improve or kill.** Recommend one of:
   - proceed as-is,
   - proceed with changes,
   - run a test first,
   - defer,
   - kill.
8. **Move forward deliberately.** If the verdict is proceed or test, move to `idea-to-implementation-plan` rather than jumping straight into implementation.

## Output shape

```markdown
## Proposal under review
<neutral summary>

## Assumptions
| Type | Assumption | Confidence | How to test |
|---|---|---:|---|
| Fact / assumption / guess | ... | High/Med/Low | ... |

## Strongest objections
1. <objection>
2. <objection>
3. <objection>

## Alternatives
| Alternative | Tradeoff |
|---|---|
| Do nothing / wait | ... |
| Smaller test | ... |
| Different approach | ... |

## Verdict
<proceed / revise / test / defer / kill>

## Changes before implementation
- <change>
- <change>
```

## Quality bar

- Be direct without being performatively negative.
- Do not bury a weak verdict under balanced prose.
- Convert criticism into a sharper next step when possible.
- If the decision requires the user, say exactly what choice is needed.

## Pitfalls

- **Rubber-stamp review:** only listing minor caveats.
- **Abstract skepticism:** objections that do not change the plan.
- **Over-analysis:** forcing a heavy review for small reversible actions.
- **Preference laundering:** presenting personal taste as objective risk.
