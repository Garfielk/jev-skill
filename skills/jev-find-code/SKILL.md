---
name: jev-find-code
description: Use for natural-language repository navigation or choosing which observed files to inspect next. Works with supplied paths and summaries; not a replacement for required graph search or exact symbol lookup.
---

# Find likely code locations from observed candidates

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

1. Use the project-required graph/index tools first; use exact lookup for known symbols. Use semantic selection when a natural-language question leaves several plausible observed candidates.
2. Build candidates from real paths and observed summaries. State clearly when only path names, rather than file contents, were available.
3. For large trees, select a local branch and then inspect its contents; bound traversal and retain alternate branches rather than treating the first choice as proof.
4. Open the selected source with the appropriate code tool and verify relevance. Update state or backtrack when the file is unrelated.
5. Return inspected paths and concrete evidence separately from uninspected leads. Walker shares, relevance scores and probability of containing a bug are different quantities.

## Context and parallelism

Jev does not inherit the agent's history. Give every request sufficient context:
the problem, observed behavior/errors, relevant prior reads, graph relationships
and real candidate paths with observed summaries or excerpts. Bare filenames alone
may not distinguish candidates; mark what has not been read and omit unrelated
files and secrets, not evidence necessary to rank the candidates.

Batch independent relevance questions over an observed candidate set instead of
serial LLM calls. Use bounded concurrency for independent searches, with stable
path/question IDs, rate limits and a cost/time budget. The host schedules calls;
the CLI has no parallel scheduler. Questions cannot read other answers in the same
request: inspect a chosen branch before asking about its unseen children. Jev's
low latency helps wide ranking; code tools still retrieve and verify actual source.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/ellipsis-dev/blink). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
