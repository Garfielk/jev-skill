# Decision recipe index

Two ways to use the same primitive: **a checkpoint inside an agent loop**, or
**a tool a person invokes on records and alternatives**. Most recipes can cross
between the two. Nothing here requires giving Jev execution privileges.

## Pick a slice

| Situation | Reference | Useful judgment |
|---|---|---|
| Agent lost the goal or repeats a failed step | [Agent recipes](agent-recipes.md) | Continue, gather evidence, replan, recover, or pause |
| Too many tools, models, skills, or specialists | [Agent recipes](agent-recipes.md) | Select from real capabilities, with an escape hatch |
| Browser or interactive application | [Agent recipes](agent-recipes.md) | Classify observed page state or choose a permitted element |
| Tests, jobs, completion claims, evaluator gaming | [Agent recipes](agent-recipes.md) | Is the claimed outcome supported by receipts? |
| Memory, context, retrieval, evidence selection | [Agent recipes](agent-recipes.md) | Keep/drop, relevance, conflict, sufficiency |
| Support, inbox, CRM, logs, operations | [Human recipes](human-recipes.md) | Queue, severity, urgency, escalation |
| Papers, qualitative coding, datasets, review | [Human recipes](human-recipes.md) | Inclusion criteria, themes, ambiguity, rubric levels |
| Product ideas, design, content, games, simulation | [Human recipes](human-recipes.md) | Score descriptive dimensions or choose a next branch |
| Compliance, abuse, cheating, sensitive decisions | Both recipe files | Flag evidence for review, never issue an automatic verdict |

## Evidence legend

The recipe files distinguish **official examples**, **community-reported use**,
**maintainer evaluations**, and **proposed adaptations**. A Reddit anecdote is not
a reproduced benchmark; a GitHub README is not an execution receipt. Follow the
source IDs to [community evidence](community.md), including failures and limitations.

The full catalog belongs here, not in the main skill prompt or README. Do not
load every recipe for a single decision. A good recipe names the observation,
the question, the output, the next consumer, and the failure condition.

## Boundaries shared by all recipes

- Jev supplies judgments, not facts it has never observed.
- Text-only input: host browser/OCR/vision tooling must produce usable text first.
- Use code for counts, dates, account ownership, budgets, permissions, and exact rules.
- Narrow questions and explicit fallback labels reduce forced decisions; they do
  not eliminate prompt injection, ambiguity, or distribution shift.
- Existing model/tool/skill routers may be sufficient. This project contributes a
  curated cross-domain skill and CLI, not a claim to have invented Jev integration.
