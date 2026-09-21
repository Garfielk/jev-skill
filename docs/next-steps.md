# Follow-up status and merge order

The user approved implementation, real OpenRouter calls and a final bug/code
review on September 21. Merge and release remain user-controlled. This follow-up
is stacked on the six-entry branch because PR #4 has not yet been merged.

| Work | Status and evidence |
|---|---|
| Six skill entry points | [PR #4](https://github.com/wuyoscar/jev-skill/pull/4), [spec #3](https://github.com/wuyoscar/jev-skill/issues/3); 108 scenarios and 14 original real IO pairs retained |
| Transport diagnosis | Safe phase/kind/status fields, truncated-body handling, duplicate JSON rejection; [replay and limitations](transport-diagnostics.md) |
| Agent-authored smoke test | Implemented inside `jev-triage`, not a new skill or mandatory runner; [workflow/parameters](../skills/jev-triage/references/smoke-test.md) |
| Generated-code validation | First draft failed; host-corrected artifact tested and then run on 24 synthetic records; [full evidence](../evals/FOLLOWUP_VALIDATION.md) |
| Skill/use-case connection | Six entry points, merged-mode examples, shared pilot guide and real API checks; no claim of native invocation across all hosts |
| Bug/code review and packaging | [Review and release readiness](release-readiness.md); no public release or user-install overwrite |

## Review and merge, one step at a time

1. Review and merge PR #4 first. This does not require accepting the follow-up.
2. Review this stacked follow-up independently; retarget it to main after #4 is
   merged and rerun CI. Do not merge the old fixed-runner [PR #2](https://github.com/wuyoscar/jev-skill/pull/2)
   on top: it has been superseded by agent-authored guidance. Close #2 when the
   replacement is accepted; its original failure evidence is retained here.
3. Once the reviewed code is on main, approve the release version. Build final
   artifacts at that exact commit, verify checksums and fresh installation, then
   update every release pin and publish. Until then, source-preview notices and
   the actual published v0.2.0 installation remain explicit and separate.

## Model choice and limits

This approved text pilot used the original **Jev + DeepSeek V4 Flash** pair, after
checking the live catalog and successful endpoint calls. No DeepSeek-VL + GPT
experiment was substituted. The skill leaves comparator selection to each task;
it does not force our text-only fixture, exact model, thresholds or scheduler.

Agreement is not accuracy. The 24 labels are preassigned synthetic expectations,
not production truth; the four unknown cases still require review. A passing
sample alone never grants bulk execution. No unsupported calibration conclusion
or automatic fallback is permitted.

The original checkout's uncommitted work remains untouched. Diagnostics were
ported and tested in isolation; the old runner was not copied into installed
skills. Fresh receipts supplement rather than overwrite the first failed run.
Community intake and visual changes remain separate, evidence-driven PRs rather
than a daily update quota; no new media was invented for this follow-up.
