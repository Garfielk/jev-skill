# Next steps — one review at a time

This is a proposed sequence for Oscar to review, not authorization to run paid
models, merge PRs, publish releases or start every item in parallel.

| Order | Work | Deliverable and acceptance | Depends on |
|---|---|---|---|
| 1 | Six skill entry points | [Spec #3](https://github.com/wuyoscar/jev-skill/issues/3), focused PR, copied-installation and migration checks; retain all 108 scenarios and 14 real IO pairs | Oscar reviews and merges |
| 2 | Transport diagnostics | Separate small PR for the already-local error-category/phase fix. Retain safe diagnostics through CLI and receipts; local timeout/DNS/TLS tests pass; do not claim the old online failure is solved | Rebase the local fix onto merged main; no live replay without approval |
| 3 | Agent-authored smoke test | Revise [PR #2](https://github.com/wuyoscar/jev-skill/pull/2), whose mandatory fixed runner no longer matches the request. Keep `smoke_test` inside the existing workflow; instruct the host to write task-specific sampling, bounded scheduling, paired calls and comparison code | Six-entry organization merged; agree the comparison models |
| 4 | Behavioral validation | Test an agent using the revised skill to produce runnable comparison code. First use synthetic data and local fake endpoints; check record pairing, identical evidence, missing/error outputs, budget and no silent full-batch execution. Preserve generated code and actual test receipts | Smoke-test guidance ready for review; any paid calls separately approved |
| 5 | Release and installation | After approved changes are merged, choose a new version, build and inspect artifacts, verify fresh installation and legacy migration, then update release pins and remove the preview notice | Explicit release approval; never publish a tag before its artifacts exist |
| Later | Community intake and presentation | Add only verified, useful new workflows or a justified visual/navigation improvement; keep attribution, actual IO and negative results | Separate small PR when there is a substantive increment, not a daily change quota |

## Decisions still to settle for smoke testing

- The original comparator was **Jev + DeepSeek V4 Flash**. A later explanation
  mentioned **DeepSeek-VL + GPT**. Treat that as unresolved, not permission to
  silently choose a different provider/model pair.
- The skill should express the desired behavior, not prescribe an experiment
  framework: the agent writes code suited to the user's dataset and existing app.
- Compare identical evidence and criteria. Without independent labels, report
  agreement and disagreements, not accuracy. Let the task determine sampling and
  acceptance criteria rather than baking a universal threshold into the skill.
- Preserve both the original incomplete live attempt and subsequent debugging
  evidence. Do not erase a failure when replacing the runner's role in the product.

## Work intentionally left untouched by the six-entry PR

The original checkout still holds the local timeout-diagnostic changes. The
six-entry branch starts from main and does not include PR #2's runner, paid
comparison receipts or parameter policy. Review each concern separately; the old
PR should not be merged as if its fixed-runner design were the approved final plan.
