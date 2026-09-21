# Agent-authored pilot and six-skill checks — 2026-09-21

This is a small synthetic integration check, not a production benchmark. The user
approved real OpenRouter calls for this follow-up. No private user dataset,
external UI actions, automated full-batch labeling or model fallback was used.

## What happened

| Check | Observed result |
|---|---|
| Original S20 failed request, exact replay | `billing`, 0.321 s, same 30 s timeout |
| Original S10 control | `bug`, 0.329 s |
| Six skills plus merged workflow modes | 10/10 actual CLI/API examples returned valid typed reports; all exit 0 |
| Paired synthetic tickets | 24/24 complete pairs, Jev 24/24 vs reference 23/24 preassigned labels |
| Agreement | 23/24 (95.8%); disagreement S11 |
| Review gate | `needs_review`; S21–S24 correctly selected `unknown`, which policy always reviews |
| Pilot usage reported | Jev $0.000536214; DeepSeek $0.000585049788; no unknown cost in this run |
| Pilot elapsed | 27.549 s, global concurrency 4 across both arms, max 48 requests, no retries |
| Per-call median | Jev 0.379 s, reference 1.504 s; this run only, not a general speed guarantee |

Requested Jev `typesafe/jev-1.13` resolved to `typesafe/jev-1.13-20260917`.
Comparator `deepseek/deepseek-v4-flash` was checked in the live catalog. Jev was
not listed by that chat-model catalog endpoint; the decisions endpoint itself
successfully resolved it. Do not infer Jev availability from a chat-only catalog.

The fixture preserves the earlier 20 ticket records and adds four missing/outside
cases before the new run. These labels were authored with the synthetic fixture,
not independently collected production outcomes. They are never sent to either
model. The pilot covers all 24 records, so it does not demonstrate representative
sampling of an unseen large population. Calibration requires held-out domain data;
24 easy authored labels and nominal probabilities are insufficient.

## Actual IO with shared context

Input S11: `How do I download an invoice? I can sign in and the charge is correct.`
Both arms received the same category definitions and the same policy: classify the
current unresolved request; a how-to question reports no product failure; billing
covers payment/refund/invoice correctness, not every incidental invoice keyword.

| Preassigned label | Jev | DeepSeek |
|---|---|---|
| `howto` | `howto`, no review | `billing` |

- [Frozen input fixture](fixtures/triage-job.json)
- [Sample, criteria, limits and acceptance manifest](results/followups-2026-09-21/pilot/manifest.json)
- [Every actual request and raw response](results/followups-2026-09-21/pilot/receipts.jsonl)
- [Full report with per-class counts and denominators](results/followups-2026-09-21/pilot/report.json)
- [Exact source used for the first live pilot](results/followups-2026-09-21/pilot/source.py)
- [All ten skill/mode requests and CLI reports](results/followups-2026-09-21/skill-examples.jsonl)

## Generated code was NOT trusted as-is

One DeepSeek V4 Flash generation used the pilot guide, task constraints and
prewritten behavioral tests. It was a code-generation call, not an autonomous
native Codex/Claude/OpenCode installation test. No generated code ran live before
host inspection and correction.

The extracted source normalizes trailing whitespace only; the raw response is
unchanged. The original **576-line draft failed two of five initial behavioral tests** even
though three passed. Inspection found an invented `(state, questions)` helper
call and unsupported `choices` field, missing full receipts, failure to retain
all in-flight calls, incomplete type/cost checks and an incorrect gate. Network
was blocked at urllib during this first-draft test, so it made no provider calls.

The host rewrote the task-specific artifact using the actual public helpers and
simpler bounded waves. Current [pilot code](agent_pilot.py) is a tested illustrative
artifact under `evals`, **not a mandatory installed runner**. The skill now tells
agents to inspect actual helper signatures/CLI help and validate the entire typed
report instead of guessing fields or extracting only a label.

- [Generation input](results/followups-2026-09-21/generation/request.json)
- [Raw generation response](results/followups-2026-09-21/generation/response.json)
- [Uncorrected generated source, do not use as a runner](results/followups-2026-09-21/generation/generated.py)
- [Behavioral tests](../tests/test_agent_pilot.py)

The current source additionally hardens cost accounting after review: booleans,
nonfinite/negative values, oversized integers and additions that overflow the
subtotal are treated as unknown costs. Raw representable JSON remains in receipts.
The exact original live source is retained; the tests and mypy were rerun after
these changes. This is not evidence that a skill alone guarantees correct generated
code; the failed draft is the reason code review and offline tests are required.

## Validation boundaries

Offline cases cover ID pairing despite completion order, global concurrency
(including 1), identical context/criteria, label exclusion from prompts, invalid or
truncated JSON, timeout metadata, unknown costs, partial coverage, no-gold reports,
missing keys, duplicate IDs, no overwrite, no network in dry runs and no implicit
bulk authorization. The runtime also gained safe truncated-body handling and
rejection of duplicate JSON fields. See [transport diagnostics](../docs/transport-diagnostics.md).

The six-entry copied-layout tests still cover Codex, Claude Code and OpenCode
resources, ten request examples each, and transcript-builder execution. Actual
API examples verify decision contracts, **not** native host invocation, browser
success, code-review truth, calibrated confidence or game outcomes. Direct
TypeSafe remains covered by offline endpoint/key tests; no native key was present,
so no real TypeSafe call or silent provider substitution was performed.

The earlier [incomplete run](TRIAGE_SMOKE_TEST.md) and raw receipts remain intact.
Successful replays do not recover its lost cause. The socket timeout is not a
whole-job deadline; this artifact records timeout and request/concurrency caps,
not a hard money limit or cancellation guarantee for an already-running request.

## Deliberately reproduce

```bash
# No API calls; choose a NEW directory each time.
python3 evals/agent_pilot.py evals/fixtures/triage-job.json --sample-size 24 --output /tmp/jev-pilot-dry
# Explicit live opt-in; this synthetic pilot's thresholds are not skill defaults.
python3 evals/agent_pilot.py evals/fixtures/triage-job.json --sample-size 24 --concurrency 4 --timeout 30 --live --output /tmp/jev-pilot-live
```

Exit 2 for this live fixture is expected: its unknown cases require review. Inspect
the report instead of treating any nonzero exit as a transport failure. Future
agents should adapt the code to their own app, not reuse these sampling/acceptance
rules blindly. [Release and review plan](../docs/next-steps.md).

## Review follow-up: overflow numeric fields

The Spec review reproduced a P2 defect: JSON `1e999` became Python infinity,
which made strict receipt serialization fail and lose the report. The runtime
now rejects overflow floats at the JSON parse boundary, before either provider
response can enter the ledger. A fake HTTP response regression covers both arms,
retains both in-flight error receipts with unknown costs, and writes a review
report. Literal NaN/Infinity and duplicate object fields are also rejected.
The bad provider body is not logged; the safe error receipt is preserved.

A second Spec-review pass caught huge integer costs bypassing float parsing.
The current pilot treats unrepresentable integer costs and overflowing subtotals
as unknown instead of crashing. Runtime bounded-number validation checks bounds
before conversion so oversized decision values also produce a normal error.
