# Jev on 20 real public pull requests

**September 22, 2026 (Melbourne):** 20 real Jev requests using public descriptions,
technical discussion and complete diffs from Requests and Flask. This is an
example of PR value triage, **not an automatic merge reviewer**.

## Collect → annotate → classify

1. Through Agent Reach's GitHub CLI backend, take the first ten results from each:
   `gh pr list -R psf/requests --state merged --limit 10` and the same command for
   `pallets/flask`. Keep every result, including repetitive dependency updates.
   This is a convenience sample in the CLI's returned order, not a random sample
   or a claim that these were the last ten chronologically merged PRs.
2. Read PR descriptions, full diffs and available top-level discussion/review
   bodies. Preserve URLs, head/base commits, merge dates and diff hashes in the
   [manifest](manifest.json). Do not clone/install/execute their code.
3. Before Jev calls, annotate intended value from that material using the fixed
   [rubric](criteria.json). These are **host-agent annotations**, not human gold.
   The host knew these were merged, so this is not a blinded human evaluation.
4. Send the project name, title, description, technical discussion and **complete
   diff** to Jev, but no expected label/rationale, merge date/state, review state,
   votes or acceptance messages. Strip Dependabot control commands and compatibility
   badges. Discard generic acceptance/thanks comments and review summaries. Other
   content is preserved; changed tests are source evidence, not test-run receipts.
5. One call per PR, up to roughly 41 KB of description plus full diff,
   four workers, no retries, no post-result prompt tuning. Public PR text is
   explicitly marked untrusted, not instructions. No action execution is allowed.

Input limits: no linked issue bodies, full repository files outside the diff,
inline review threads or CI logs. Missing linked evidence is not claimed as read.
Identity/title references may still permit model recognition: metadata removal
reduces shortcutting but cannot prove training-data independence or zero leakage.

## What counts as value?

- `substantive`: an evidenced concrete functional, security, documentation
  correctness or test-quality benefit beyond routine upkeep. A version bump
  fixing a specifically reported project failure qualifies.
- `routine_maintenance`: useful dependency/release upkeep without that specific
  project fix. **This does not mean meaningless.**
- `no_clear_value`: evidence shows redundancy, ineffectiveness or pure churn.
- `insufficient_evidence`: not enough consistent material to assess even intent.

This asks whether the change has a useful purpose, **not** whether it is correct,
safe, well implemented or ready to merge. The fixed expected labels happened to
be 10 substantive and 10 maintenance. No negative examples were added or fabricated.

## Results

| Measure | Observed |
|---|---:|
| Agreement with prewritten host labels | 20/20 |
| Substantive | 10 |
| Routine maintenance | 10 |
| CLI selected | 19 |
| CLI needs review | 1 |
| Request errors / retries | 0 / 0 |
| Provider-reported input tokens | 63,268 |
| Provider-reported total cost | $0.002657256 |
| Median local subprocess wall time | 0.481 s |

All calls resolved to `typesafe/jev-1.13-20260917` through OpenRouter / TypeSafe.
Local timing includes Python startup/network under concurrency, not provider-only
latency. [All scores](scores.json), [requests](requests/) and [receipts](receipts/)
are included, with matching request SHA-256 values.

**20/20 is agreement, not a general accuracy estimate.** All PRs were merged and
all were host-labeled useful in one of two ways. An always-useful binary classifier
would also succeed on this sample. It says nothing about detecting bad PRs, false
positives, calibration or whether full context beats a title-only baseline (not
run here). Nine similar Requests dependency bumps reduce effective diversity.

## Actual I/O examples

### A dependency update that fixes a concrete failure

[Requests #7609](https://github.com/psf/requests/pull/7609) describes issue-locking
failures following longer GitHub tokens. The diff moves the pinned lock action
from 6.0.0 to 6.0.2; the description links that change to removal of token-length
validation. We did not independently run the action or read the linked issue.

- Input: [description + complete workflow diff](requests/psf-requests-7609.json).
- Actual output: `substantive`, option probability **0.83**, CLI `selected`.
- [Raw response](receipts/psf-requests-7609.json).

By contrast, [Requests #7616](https://github.com/psf/requests/pull/7616) updates a
Ruff hook version without a specific project regression in the supplied material:
`routine_maintenance`, probability **1.0**. That is not a 100% correctness guarantee.
[Input](requests/psf-requests-7616.json) · [output](receipts/psf-requests-7616.json).

### Useful security work still sent to review

[Flask #5945](https://github.com/pallets/flask/pull/5945) adds workflow security
scanning and changes permissions, credential persistence and variable handling.

- Input: [description + complete workflow diffs](requests/pallets-flask-5945.json).
- Actual output: `substantive`, option probability **0.79**, CLI `needs_review`.
- [Raw response](receipts/pallets-flask-5945.json).

The CLI's existing minimum probability is 0.8, margin 0.15. This is a routing
threshold, not a measured safety guarantee. Correct top-choice agreement does
not remove the review requirement.

## Use the pattern with your agent

> Use jev-eval to triage the intended value of these public PRs. Collect the
> descriptions, relevant technical discussion and full diffs. Keep source URLs
> and revisions. Separate substantive improvement from routine maintenance,
> no clear value and insufficient evidence; small maintenance is not worthless.
> Give Jev the evidence and rubric, not approval status or desired answers.
> Return a table with the source, category, probability and review status. Keep
> ambiguous cases for review. Do not execute PR code, infer passing tests or merge.

Start with [one actual request](requests/psf-requests-7609.json), replace its
source evidence, and use the installed Jev CLI after agreeing on data scope and
paid calls. Expected labels belong in a separate evaluation file, never in the
request. For production assessment, add an independently annotated mixture of
merged, rejected and unresolved changes; do not treat rejected as automatically bad.

## Reproduce

```bash
# Offline; does not call Jev.
python3 docs/experiments/public-pr-pilot/run.py
python3 -m unittest discover -s docs/experiments/public-pr-pilot -p 'test_*.py' -v

# Optional: refetch the fixed manifest into a NEW directory using authenticated gh.
python3 docs/experiments/public-pr-pilot/collect.py /tmp/jev-pr-refetch-new

# Paid: in a separate copy without existing receipts, with OPENROUTER_API_KEY set.
python3 docs/experiments/public-pr-pilot/run.py --live
```

The runner refuses existing receipts and changed request hashes. Refetched PR
bodies can change; use frozen requests for exact replay and compare manifest
revisions/hashes before substituting new data. Upstream requests may resolve to
a newer service version later; record it rather than claiming exact reproduction.

## Sources and attribution

PRs belong to their respective contributors. Embedded diffs retain upstream
licensing: [Requests Apache-2.0](licenses/psf-requests.txt) and
[Flask BSD-3-Clause](licenses/pallets-flask.txt), retrieved at manifest head commits.
PR discussions and upstream release-note excerpts remain attributed to their
linked sources; this collection does not relicense them as original Jev material.
The table below records every selected PR and the host's pre-call rationale.

| PR | Pre-call rationale | Jev category | Status |
|---|---|---|---|
| [psf-requests-7628](https://github.com/psf/requests/pull/7628) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7616](https://github.com/psf/requests/pull/7616) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7609](https://github.com/psf/requests/pull/7609) | Updates an action specifically to remove a token-length validation failure described in the PR. | `substantive` | `selected` |
| [psf-requests-7608](https://github.com/psf/requests/pull/7608) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7606](https://github.com/psf/requests/pull/7606) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7603](https://github.com/psf/requests/pull/7603) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7598](https://github.com/psf/requests/pull/7598) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7597](https://github.com/psf/requests/pull/7597) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7596](https://github.com/psf/requests/pull/7596) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [psf-requests-7591](https://github.com/psf/requests/pull/7591) | Updates existing tool/action version pins without a specific project regression being fixed. | `routine_maintenance` | `selected` |
| [pallets-flask-6133](https://github.com/pallets/flask/pull/6133) | Adds a QUERY decorator and method coverage, beyond a version bump. | `substantive` | `selected` |
| [pallets-flask-6096](https://github.com/pallets/flask/pull/6096) | Replaces colon splitting with URL parsing and adds IPv6 regression cases. | `substantive` | `selected` |
| [pallets-flask-6095](https://github.com/pallets/flask/pull/6095) | Removes private pytest internals and resets environment independently per test. | `substantive` | `selected` |
| [pallets-flask-6013](https://github.com/pallets/flask/pull/6013) | Makes autoescaping extension matching case-insensitive. | `substantive` | `selected` |
| [pallets-flask-5962](https://github.com/pallets/flask/pull/5962) | Removes an invalid Unicode Host case, with discussion identifying the valid neighboring test. | `substantive` | `selected` |
| [pallets-flask-5945](https://github.com/pallets/flask/pull/5945) | Adds workflow security scanning and directly hardens permissions and credentials. | `substantive` | `needs_review` |
| [pallets-flask-5928](https://github.com/pallets/flask/pull/5928) | Collects teardown errors so remaining callbacks and cleanup still run; adds regression coverage. | `substantive` | `selected` |
| [pallets-flask-5924](https://github.com/pallets/flask/pull/5924) | Coordinates package version and release metadata without implementing the changelog features. | `routine_maintenance` | `selected` |
| [pallets-flask-5917](https://github.com/pallets/flask/pull/5917) | Fixes enabling automatic OPTIONS overrides and adds focused tests. | `substantive` | `selected` |
| [pallets-flask-5903](https://github.com/pallets/flask/pull/5903) | Stops swallowing directory permission failures in tutorial and example code. | `substantive` | `selected` |
