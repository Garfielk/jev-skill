---
name: jev-triage
description: Use for user-defined inbox, support-ticket, feedback or record classification and prioritization. Produces labels and review queues, not replies or automatic mailbox changes.
---

# Sort messages and records by custom criteria

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

1. Agree on categories with short inclusions/exclusions. Use independent Nouls when records can have several labels; use Choice for one queue.
2. Preserve original record IDs. For multiple records, name the exact record ID in every question or send one request per record; one Choice over an entire inbox is not per-message classification.
3. Collect text only from files or accounts the user authorized. Classify before writing tags, moving messages or sending replies.
4. Return a reviewable table: record ID, category, urgency, uncertainty and intended next consumer. Keep other/missing-evidence records visible.
5. Test near-miss categories and user-labeled examples before applying a rule in bulk. Change labels and urgency anchors, not just the sample text.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://github.com/sharziki/semdecide). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
