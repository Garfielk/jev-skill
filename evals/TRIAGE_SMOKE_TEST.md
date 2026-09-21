# Triage smoke-test validation — September 21, 2026

## What was actually tested

The existing `jev-triage` skill now accepts `smoke_test` and sample parameters.
The bundled Python runner was tested with real OpenRouter calls as well as offline
tests. This is not a new skill and is not a production-accuracy benchmark.

**First live attempt: incomplete; correctly stopped for review.**

| Item | Observed result |
|---|---|
| Input | 20 maintainer-authored synthetic support records, five category definitions |
| Planned requests | 20 Jev + 20 DeepSeek; no automatic retries |
| Actually attempted | 2 Jev + 1 DeepSeek |
| Complete pairs | **1 / 20** |
| That pair | S10: Jev `bug`, DeepSeek `bug`, authored gold `bug` |
| Next item | S20: Jev connection/timeout failure after 30.056 seconds; no HTTP status returned |
| Gate | **`needs_review`**, `bulk_authorized: false` |
| Usage | Known subtotal **$0.000027314**; failed request cost unknown, not zero |

One agreeing pair is **not** evidence that the classifiers have comparable accuracy.
No full-dataset labeling was started. The first error stopped the runner before
reference call two, demonstrating the fail-closed path with real service behavior.

Requested/resolved Jev: `typesafe/jev-1.13` → `typesafe/jev-1.13-20260917`.
Reference: `deepseek/deepseek-v4-flash` (not v4.1).

## Inspect the actual input and output

Input evidence for completed record **S10**:

```json
{"id":"S10","text":"The export worked yesterday; today all exports produce empty files."}
```

The complete shared policy, descriptions and question are preserved in the
[actual requests and raw responses](results/triage-smoke-2026-09-21/attempt-1/receipts.jsonl).
Gold labels and sampling strata were not sent to either model.

Observed label pair, not an illustrative output:

```json
{"id":"S10","gold":"bug","jev_label":"bug","jev_review":false,"reference_label":"bug"}
```

- [Frozen sample manifest](results/triage-smoke-2026-09-21/attempt-1/manifest.json)
- [Original run report](results/triage-smoke-2026-09-21/attempt-1/report.json)
- [Recomputed summary](results/triage-smoke-2026-09-21/attempt-1/summary-recomputed.json)
- [Reference model catalog snapshot](results/triage-smoke-2026-09-21/reference-catalog.json)

The first report counted missing answers against attempted-record accuracy. Review
of the incomplete run exposed that ambiguous denominator. The current report uses
valid labeled answers with explicit scored counts and coverage; incomplete runs
still cannot pass. The corrected summary was computed **offline** from the original
rows; the original report/receipts remain unchanged. Neither 1/1 valid accuracy nor
1/2 attempted-record success estimates quality on the planned 20 records.

## Offline validation

Tests cover parameter parsing, deterministic sampling and strata, invalid input,
gold exclusion from both requests, identical evidence/criteria, dry run/skip with
no network, explicit key requirements, copied skill files, invalid/truncated
reference output, complete raw receipts, missing costs, no overwrites and stopping
on errors without retries. Gate tests cover no-gold agreement, accuracy failures,
missing pairs, uncertainty and the fact that a passing sample never authorizes bulk.

These tests do **not** establish native command execution in Claude Code, Codex and
OpenCode individually. Invocation guidance follows their official documentation;
parser execution and API execution were tested separately. No host was switched,
no new agent was spawned, and no user/private dataset was sent.

## Reproduce deliberately

```bash
python skills/jev-triage/scripts/smoke_test.py \
  skills/jev-triage/assets/smoke-job.json --smoke-test true --sample-size 20
# Only after approving both services, records and API usage:
python skills/jev-triage/scripts/smoke_test.py \
  skills/jev-triage/assets/smoke-job.json --smoke-test true --sample-size 20 \
  --live --output /path/to/new-run
```

A new run must preserve the failure above, use a new output directory, and not be
presented as the original attempt succeeding. A larger timeout is an explicit
parameter change (`--timeout 60`), not an automatic retry.
