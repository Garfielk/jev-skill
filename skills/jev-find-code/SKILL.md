---
name: jev-find-code
description: Use for natural-language repository navigation or choosing which observed files to inspect next. Works with supplied paths and summaries; not a replacement for required graph search or exact symbol lookup.
---

# Find likely code locations from observed candidates

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

1. Use the project-required graph/index tools first; use exact lookup for known symbols. Use semantic selection when a natural-language question leaves several plausible observed candidates.
2. Build candidates from real paths and observed summaries. State clearly when only path names, rather than file contents, were available.
3. For large trees, select a local branch and then inspect its contents; bound traversal and retain alternate branches rather than treating the first choice as proof.
4. Open the selected source with the appropriate code tool and verify relevance. Update state or backtrack when the file is unrelated.
5. Return inspected paths and concrete evidence separately from uninspected leads. Walker shares, relevance scores and probability of containing a bug are different quantities.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/ellipsis-dev/blink). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
