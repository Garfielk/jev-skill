---
name: jev-simulation
description: Use for game, NPC, interactive-story or training-simulation decisions from explicit world state and legal actions. Humans or a planner define objectives; a simulator applies actions and verifies outcomes.
---

# Choose actions inside an authored world

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

1. Define the world, objective, legal actions, turn budget and authoritative state. Keep fictional simulation actions separate from real-world tool execution.
2. Let a person or reasoning model supply strategy when needed. Ask Jev only for a bounded local choice using visible state; keep unknown and replan outcomes available.
3. Have the simulator validate and apply the chosen transition. Reject stale decisions and update observations before dependent actions.
4. Replan on completed subgoals, violated assumptions or stalled progress. Log state/action/outcome IDs; stop on turn budget or deadlock.
5. Render text, UI or video from the resulting state as an optional separate consumer. Compare objectives across the same seeds; visual appeal is not decision quality.

## Make it yours

Replace the example's evidence, candidate IDs and criteria together. Preserve a
no-match route when the real task can fall outside the labels. Agree on how the
host or person consumes each answer before enabling any automatic effect.

## Precedent

[Related project or author example](https://x.com/gokayfem/status/2101022590722810271). Our workflow is an adaptation,
not that project's code, an automatic installer, or a reproduced benchmark.
[OpenRouter request contract](https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request).
