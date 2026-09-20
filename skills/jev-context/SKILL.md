---
name: jev-context
description: Use when large tool results need relevance review or a user wants advice about a compaction checkpoint. Starts with a keep/drop proposal; does not install hooks or automatically rewrite agent memory.
---

# Review context relevance without losing the original

## Prerequisite and first example

Use the shared `jev-decide` CLI (Python 3.10+), installed from the reviewed
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

1. Keep the original tool output retrievable before proposing reduction. Preserve source paths, IDs, errors, open tasks and user constraints independently.
2. Ask one relevance question per named block; leave uncertain and unjudged blocks visible. An apparent duplicate may contain a changed identifier or error.
3. Start in advisory/shadow use: report what would be hidden, where it can be recalled and why it matters to the current task. Do not modify transcript files.
4. Treat compaction timing as a separate question from what to retain. A completed phase does not prove future turns no longer need earlier details.
5. Only a supported native host operation can compact, and only with the required authorization. Pressure-dependent thresholds are policy choices to test on later continuations.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/GhalebDweikat/winnow). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
