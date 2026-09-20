---
name: jev-code-review
description: Use for targeted review of a supplied code change and associated test receipts against custom review criteria. Returns evidence-backed review leads, not merge approval or a replacement for tests.
---

# Review a diff and its completion evidence

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

1. Collect the actual diff, relevant source and tests, acceptance criteria and real command receipts. Mark unavailable evidence as missing.
2. Separate concerns such as correctness, compatibility and test coverage. Select concrete hunks before attaching severity to a finding.
3. Use test receipts to check completion claims; a passing altered test is not evidence for the original behavior.
4. Return each lead with its hunk/source ID, concern, uncertainty and a concrete verification step. A Jev label alone is not proof of a defect.
5. Keep compilers, static analysis and original tests. Do not merge, publish, change review protections or edit tests merely because the judgment suggests approval.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/devagrawal09/jev-review). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
