---
name: jev-documents
description: Use for selecting original source spans, reranking supplied passages or checking claims against documents. Keeps citations and no-match outcomes; does not invent missing facts.
---

# Find and verify information in documents

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

1. Read the authorized source and retain document/page/line identifiers. Have parsers or regex produce exact candidate spans when possible.
2. Define the requested role precisely: invoice destination is not any email address. Include none when no candidate fits.
3. Use independent relevance questions when ranking all passages; winning a relative Choice does not establish an answer exists.
4. Copy the original span selected by ID. Do not ask Jev to synthesize the extracted field or fabricate a quotation.
5. Check each claim against its cited evidence separately. Report unsupported/contradicted statements and preserve source links for human checking.

## Context and parallelism

Jev does not inherit the agent's history. Give every request sufficient context:
the user's information need, exact claim, source IDs, surrounding passages,
definitions and relevant exceptions. Supply the text, not just a URL or your own
summary verdict. Keep needed cross-references; omit unrelated material and secrets.

Batch independent claim checks or per-passage relevance scores over shared state
instead of serial LLM calls. For separate document groups, use bounded concurrency
with stable document/question IDs, rate limits and a cost/time budget. The host
schedules calls; the CLI has no parallel scheduler. Questions cannot read other
answers in the same request: fetch a selected source before asking about unseen
contents. Use Jev's low latency for repeated judgments, not document generation.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/jkudish/jev-mcp). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
