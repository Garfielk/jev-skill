# Does the evidence change the judgment?

**Real Jev pilot, September 22, 2026 (Melbourne).** Twenty synthetic cases,
40 independent requests via OpenRouter, no retries or discarded outputs.
This tests the [context advice](../../../skills/jev/references/pitfalls.md#evidence-freshness),
not a new skill or the dbt-assay author's private workload.

## Fixed design

Five domains × four variants: CI readiness, refunds, SQL claim verification,
access eligibility and ticket routing. Each domain has a supported claim, a
contradicted claim, an unresolved claim and an identical-evidence control.

The host authored both conditions and expected labels **before calling Jev**:
[cases.json](cases.json). Each request includes the same goal, claim, policy and
three choices (`supported`, `contradicted`, `unknown`). Only its evidence changes.
The short condition withholds the detailed receipt in 15 cases; the full condition
supplies the relevant receipt, which still leaves five cases unresolved. Five
controls have identical inputs across conditions. This is a deliberate evidence
ablation, **not** a representative task sample or a test of context-window size.

No expected labels, other cases, earlier answers or private data were sent to
Jev. These are standalone judgments, not running software tests or executing
refunds/access changes. An actual coding agent must run the real checks first.

- Requested model: `typesafe/jev-1.13`; all responses resolved to
  `typesafe/jev-1.13-20260917`, provider TypeSafe through OpenRouter.
- One request per case/condition; fixed shuffled order (seed 22), four workers.
- Existing CLI policy: minimum option probability 0.8, margin 0.15; `unknown`
  always needs review. Exit 2 means review, not transport failure.
- Primary metric: top-choice agreement with the **condition-specific** expected
  label. Abstention is correct when evidence is absent; it is not an error.
- Also report unknown count, selected count, selected correctness, errors, cost
  and local wall time. No post-hoc prompt tuning or repeated votes.

## Results

| Metric | Short evidence | Full evidence |
|---|---:|---:|
| Expected-label agreement | 20/20 (100%) | 19/20 (95%) |
| `unknown` answers | 15/20 | 4/20 |
| CLI `selected` | 5/20 | 15/20 |
| Correct among selected | 5/5 | 14/15 |
| Request errors | 0 | 0 |
| Median subprocess wall time | 0.464 s | 0.450 s |

All ten cases receiving decisive new evidence moved from `unknown` to the
expected supported/contradicted answer; the SQL contradiction still needed review
at option probability 0.76. All five identical-evidence controls kept their labels.
Of the five cases still lacking decisive evidence, four stayed unknown and one
became a contradiction. Thus more evidence enabled more decisions; **it did not
improve measured accuracy**, and the CLI's selection threshold did not catch the
one disagreement. Selection is not correctness or permission.

Total provider-reported cost: **$0.000784056**, 18,668 input tokens. Wall times
include Python startup and network latency under concurrency; this is not a
provider latency benchmark. No calibration conclusion is justified by 20 cases.

## Actual input and output

### A resolved case: refund eligibility

Shared claim: “This order qualifies for a refund.”
Shared policy: refunds require delivery within 30 days and an unused product;
both must be documented.

| Evidence sent | Jev label | Expected label |
|---|---|---|
| “The relevant detailed receipt has not been supplied.” | `unknown` | `unknown` |
| “Delivered 12 days ago; inspection confirms unused.” | `supported` | `supported` |

[Short request](requests/refund-support-short.json) ·
[short receipt](receipts/refund-support-short.json) ·
[full request](requests/refund-support-full.json) ·
[full receipt](receipts/refund-support-full.json).

### The disagreement: current CI readiness

Claim: “The patch is ready for technical review.”
Policy: current commit must pass unit and integration tests; this does not
authorize merging.
Full evidence: “Previous commit a16 passed; current commit a17 has no integration receipt.”

Prewritten expected label: `unknown`. Actual Jev label: `contradicted`, option
probability **0.82**, separate response `confidence` **0.73**, CLI `selected`.
[Exact input](requests/ci-incomplete-full.json) ·
[unaltered model response inside receipt](receipts/ci-incomplete-full.json).

This counts as a disagreement under our fixed labels; it is not hidden or retried.
However, “ready” can mean documented eligibility rather than an unknown underlying
test outcome. Under that interpretation, rejecting readiness is defensible. This
is a **rubric ambiguity**, not conclusive proof of a reasoning defect. A follow-up
should separate “did the tests pass?” from “is documented readiness established?”
with independently reviewed labels; this pilot does not silently relabel the case.

## Reproduce and audit

```bash
# Offline: regenerate identical fixtures/requests and rescore saved receipts.
python3 docs/experiments/context-pilot/run.py
python3 -m unittest discover -s docs/experiments/context-pilot -p 'test_*.py' -v

# Paid: in a separate copy without an existing receipts directory,
# after setting OPENROUTER_API_KEY in the environment:
python3 docs/experiments/context-pilot/run.py --live
```

The live runner refuses to overwrite existing receipts and never retries.
Every receipt includes its request SHA-256, exit status, elapsed time and raw CLI
JSON (including provider response, usage and actual model). [Scores](scores.json)
include all 40 runs. API keys are not in any artifact. Fixtures are deliberately
small and templated, host-labeled and not externally reviewed; percentage points
here must not be generalized to production or interpreted as statistical evidence
that a larger context is better.

**Not tested:** stored-result invalidation, cache read guards, actual CI execution,
agent end-to-end performance, dbt-assay reproduction, long/noisy context, or a
comparison against another model. Cache advice in the reference remains an
engineering adaptation of the cited author report, not a result of this pilot.
