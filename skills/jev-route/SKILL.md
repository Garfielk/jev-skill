---
name: jev-route
description: Use to route a bounded task among available models, tools or specialists using explicit capability descriptions. Returns advice; does not switch a host primary model or install a router.
---

# Choose a tool, model or specialist

## Missing key: ask before choosing a mode

Before making a decision, check **only the presence** of `OPENROUTER_API_KEY` in
this agent's execution environment; never print its value. If the key is missing,
warn the user and ask in their language:

> No OpenRouter key was found, so I cannot call Jev. Which option do you prefer?
> **A — Get a key:** create one at https://openrouter.ai/settings/keys and configure
> `OPENROUTER_API_KEY` locally to use the real Jev API.
> **B — Use your current agent:** I simulate the classification using the same
> evidence and criteria, without calling Jev or requiring an OpenRouter key.

**Wait for an explicit A or B choice. Never silently simulate.** For A, help with
local setup without collecting the secret in chat; resume Jev calls only when
configured and authorized. For B, remember consent for the current task, not as a
permanent default. Do not ask again for every record in that approved task. A key
appearing later does not authorize silently switching an approved B task to A.
API errors are not consent to simulate; report them instead of switching modes.

In **B / agent simulation**, the current host agent does the judgment itself:
- Use the same goal, sufficient context, question IDs and candidate definitions.
  For `choice`, select a supplied label; for `noul`, return a boolean; for
  `score`, choose an anchored rubric level, not a claimed Jev probability-weighted
  score. If evidence is insufficient or no option fits, use `value: null` and
  `needs_review: true`; never invent a new candidate. Keep ambiguity visible.
- Mark every output `mode: agent_simulation` and `jev_called: false`. For each
  question return `value`, `needs_review` and a short evidence-based `reason`;
  set `probability` and `confidence` to `null`. Never invent Jev distributions,
  provider receipts or calibrated certainty, or apply probability-threshold
  automation to these judgments. Keep them separate from real Jev benchmarks.
- Skip the CLI, API/key requirements and API-specific steps below. Do not install
  another model/provider to simulate. Existing permissions and outcome checks
  still apply; the host agent's normal costs and privacy terms still apply too.
  B is not a promise of free, local, offline or Jev-speed execution.

Explicit dry-run validation is separate: it checks input, not classification.
It needs neither a key nor simulated answers.

## Jev API prerequisite and first example

In Jev API mode, use the shared `jev-decide` CLI (Python 3.10+), installed from the reviewed
`jev-skill` package. If unavailable, explain the missing dependency rather than
silently installing software. The agent process must inherit
`OPENROUTER_API_KEY`; never place the key in a prompt or request file.
No sibling skill or third-party integration is required for this judgment.
Actual UI, file, mailbox or simulation actions require the host's own tools.

Resolve `<skill-dir>` to this installed folder. Copy and edit
[assets/example.json](assets/example.json) for the user's task; it is synthetic
input, not a captured successful result. Validate it without a key or API call:

```bash
jev-decide decide <skill-dir>/assets/example.json --dry-run
# After reviewing the input and authorization to send it to OpenRouter:
jev-decide decide /path/to/edited-request.json
```

Normal calls send the supplied evidence to OpenRouter and its provider and incur
usage. Read relevant answers, not only the exit code: `0` means selected/scored,
`2` means review, `1` means error. A confidently false Noul is still false;
selection is not permission. Unknown, missing or conflicting evidence needs a
fallback. Test thresholds on the user's task rather than assuming 0.9 is safe.

## Workflow

1. Inventory actual available capabilities, allowed spending and task constraints. Do not infer access from a model name or prestige tier.
2. Describe each candidate by what it can and cannot do. Supply the current subtask and relevant preceding state, not an entire unrelated transcript.
3. Separate selection from invocation. Show a recommendation unless the user already authorized the handoff and the host has an invocation tool.
4. Preserve fallback routes for unavailable, uncertain or failed candidates. A recommendation does not authorize sharing data with another provider.
5. Evaluate routing regret and completed work along with total cost, cache loss and retries. This skill is not the upstream Codex Router service.

## Context and parallelism

Jev does not inherit the agent's history. Give every request sufficient context:
the subtask and goal, relevant prior attempts, data constraints, budget, and real
candidate capability/availability descriptions. Model names alone are not enough;
omit unrelated conversation and secrets, not facts needed to choose a useful route.

Batch independent routing and suitability questions over shared state instead of
serial LLM calls. Route independent queued tasks with bounded concurrency, stable
task/question IDs, rate limits and a cost/time budget. The host schedules calls;
the CLI has no parallel scheduler. Questions cannot read other answers in the same
request: wait for a delegated result before deciding its dependent next route.
Use Jev's low latency for selection; retain a reasoning model for open-ended work.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/0xNatoshi/jev-codex-router). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
