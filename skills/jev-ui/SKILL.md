---
name: jev-ui
description: Use when a browser or desktop task needs a bounded next-action choice from a fresh text or accessibility observation. Requires a host UI tool; does not install a controller or handle screenshots itself.
---

# Choose a grounded browser or desktop step

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

1. Use an available connector/browser/computer-use tool for observation. Follow its native instructions; Jev receives a minimal text state, not hidden UI or fabricated element IDs.
2. Build candidates only from fresh observed controls and operations actually supported by the host. Prefer an exact known action without Jev when no judgment is needed.
3. Keep known typing values in the host. If text generation is needed, do it separately and validate it before choosing the target.
4. Interpret the selected action, recheck snapshot freshness, execute only a permitted step, and read the result. Do not treat a DONE choice as completion evidence.
5. Return to the host for sensitive actions, consent, stale state or unsupported controls. This skill does not grant browser, desktop or OS permissions.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/browser-use/jev-ultrafast). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
