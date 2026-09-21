---
name: jev-triage
description: Use for user-defined inbox, support-ticket, feedback or record classification and prioritization, especially bulk parallel judgments with sufficient per-record context. Accepts smoke_test and sample_size parameters to compare a small sample with DeepSeek before scaling. Produces labels and review queues, not replies or automatic mailbox changes.
---

# Sort messages and records by custom criteria

## 🚦 Parameters: smoke_test before bulk labeling

Accept named invocation values from the user: `smoke_test=true`, `sample_size=50`,
`input=job.json`, plus `seed`, `provider`, `reference_model`, `min_accuracy` and
`max_accuracy_gap` and `timeout`. These are skill/workflow parameters, not Jev request fields.
Default bulk labeling to `smoke_test=true`; do not start full-dataset calls first.
In simulation mode, report the paired API test as unavailable; ask whether to
configure real access or explicitly waive it. Never fabricate a comparison.
Claude Code receives invocation arguments automatically; in other hosts read the
same values from the user's message. Never shell-evaluate raw argument text.

For a bulk labeling task, read [the parameter contract and runner](references/smoke-test.md).
Prepare a representative sample with full relevant context. After approving the
sample and both providers, run `scripts/smoke_test.py` with those parameters to
compare Jev and the selected reference model. Show complete input/output pairs,
coverage, disagreements, gold-label accuracy when available, and cost. Agreement
alone is not accuracy. Stop for review on errors, missing evidence or failed checks.
Even a passing sample does not authorize full-scale execution: obtain scope/budget
approval, then use the existing bulk workflow. `smoke_test=false` requires an
explicit user waiver; record it as skipped, never as a successful test.

## Setup: choose the service or simulation

Check only the presence of `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY`; never
print credentials. Respect the user's already chosen mode. For a new setup,
prefer the user's existing OpenRouter account; otherwise offer official TypeSafe.
If OpenRouter is missing, explain that direct TypeSafe is also real Jev. Do not
silently change destination, send data, create an account or switch the host model.

If no route has been chosen, explain the available routes and ask:

> **A — Real Jev:** use/get an OpenRouter key at https://openrouter.ai/settings/keys
> if you use OpenRouter; otherwise use/get a TypeSafe key at
> https://console.typesafe.ai. Configure it locally, not in chat.
> **B — Simulate:** use the current agent, or an explicitly selected available
> model such as DeepSeek, with the same context, questions and criteria.

**Wait for an explicit choice.** Do not ask again for every record in the same
approved task. API errors do not authorize switching providers or simulation.
Missing both keys is not a dead end: offer B. It requires no Jev key but the
chosen agent/model's ordinary access, usage costs and privacy terms still apply.
Do not assume DeepSeek is installed, free or locally hosted.

In B, return `mode: agent_simulation` for the current host or
`mode: model_simulation` for another explicitly approved model, plus its actual
model identity when available and `jev_called: false`. Each question has `value`,
`needs_review`, a brief evidence-based `reason`, `probability: null` and
`confidence: null`. Choice values must be supplied labels, Noul values booleans,
and Score values integer rubric indices. Use null/review for missing evidence.
Never present this as Jev, calibrated probability or equivalent speed/accuracy.
Skip Jev CLI/API steps in B; use the approved model's existing interface and do
not install a substitute or send data elsewhere without consent.

In A, select the CLI destination explicitly: `--provider openrouter` or
`--provider typesafe`. The latter uses `TYPESAFE_API_KEY` and maps the bundled
OpenRouter model ID to `jev-1.13.0`. `--dry-run` only validates; it neither
classifies nor makes a network call. `jev-decide setup` reports presence only,
not key validity, credits or permission. For guided setup and a copyable
DeepSeek prompt, use `jev-setup` or the [setup guide](https://github.com/wuyoscar/jev-skill/blob/main/skills/jev-setup/SKILL.md).

## Jev API prerequisite and first example

In Jev API mode, use the shared `jev-decide` CLI (Python 3.10+), installed from the reviewed
`jev-skill` package. If unavailable, explain the missing dependency rather than
silently installing software. The agent process must inherit
`OPENROUTER_API_KEY` or `TYPESAFE_API_KEY` for the chosen provider; never place the key in a prompt or request file.
No sibling skill or third-party integration is required for this judgment.
Actual UI, file, mailbox or simulation actions require the host's own tools.

Resolve `<skill-dir>` to this installed folder. Copy and edit
[assets/example.json](assets/example.json) for the user's task; it is synthetic
input, not a captured successful result. Validate it without a key or API call:

The commands below default to OpenRouter. For the official route, append
`--provider typesafe` to both validation and live calls.

```bash
jev-decide decide <skill-dir>/assets/example.json --dry-run
# After reviewing the input and authorization to send it to the chosen provider:
jev-decide decide /path/to/edited-request.json
```

Normal calls send the supplied evidence to the selected Jev provider and incur
usage. Read relevant answers, not only the exit code: `0` means selected/scored,
`2` means review, `1` means error. A confidently false Noul is still false;
selection is not permission. Unknown, missing or conflicting evidence needs a
fallback. Test thresholds on the user's task rather than assuming 0.9 is safe.

## Workflow

1. Agree on categories with short inclusions/exclusions. Use independent Nouls when records can have several labels; use Choice for one queue.
2. Preserve original record IDs. For multiple records, name the exact record ID in every question or send one request per record; one Choice over an entire inbox is not per-message classification.
3. Collect text only from files or accounts the user authorized. Classify before writing tags, moving messages or sending replies.
4. Return a reviewable table: record ID, category, urgency, uncertainty and intended next consumer. Keep other/missing-evidence records visible.
5. Before bulk labeling, apply the `smoke_test` parameter contract above. Include near-miss categories and user-labeled examples; retest when label definitions or input organization change.

## Context and parallelism

Jev does not inherit the agent's history. Give every request sufficient context:
the user's categories and priority policy, each record's text and relevant thread,
product/account facts, and known missing evidence. A last-message fragment is not
enough when earlier messages change its meaning; omit unrelated history and secrets.

For bulk triage, batch independent category, escalation and urgency questions over
shared state instead of serial LLM calls. Name the record ID in every question.
Use bounded concurrency for independent requests, with stable IDs, rate limits and
a cost/time budget. The host schedules calls; the CLI has no parallel scheduler.
Questions cannot read other answers in the same request: gather any newly needed
account evidence before a dependent follow-up. Low latency is a reason to use Jev
for the judgment stage, not to skip quality checks or automate mailbox changes.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/sharziki/semdecide). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
