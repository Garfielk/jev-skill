# Pilot results — September 20, 2026

**Fixed checkpoint advice did not improve this small agent benchmark.** The baseline
completed all 12 episodes; the Jev-assisted arm completed 10. Both had zero forbidden
action attempts. The additional advice increased observed cost and latency.

This is a transparent pilot result, not a general conclusion about Jev, every
recipe, automatic skill selection, or long-running production agents.

## Protocol and receipts

- Four authored synthetic tasks × three repeats × two arms = **24 episodes / 12 pairs**.
- Same `deepseek/deepseek-v4.1-flash`, reasoning `none`, tool catalog, simulator,
  step budget and base prompt. Jev advice was added before turns 3, 6 and 9.
- Maximum ten action turns. Success required the correct final state, explicit
  `finish`, and no forbidden-action attempts, as declared before the run.
- Jev requested `typesafe/jev-1.13`; returned IDs and actual routed providers are
  preserved per call. No episode was dropped, selectively rerun, or retuned.
- [Frozen manifest and source snapshots](results/deepseek-pilot-2026-09-20/manifest.json),
  [all episode results](results/deepseek-pilot-2026-09-20/results.json),
  [paired outcomes](results/deepseek-pilot-2026-09-20/paired.json),
  [aggregate](results/deepseek-pilot-2026-09-20/aggregate.json).
  Each episode directory also contains the full API request/response and action trace.

## Outcomes

| Measure | Baseline | + Jev checkpoints |
|---|---:|---:|
| Verified completed episodes | 12 / 12 | 10 / 12 |
| Mean action turns | 8.33 | 8.58 |
| Forbidden-action attempts | 0 | 0 |
| Tool errors, including the expected exporter failure | 9 | 13 |
| Invalid model actions | 0 | 0 |
| API failures | 0 | 0 |
| API calls, including helper | 100 | 133 |
| Reported input tokens, all models | 54,780 | 123,695 |
| Reported output tokens, all models | 2,133 | 5,243 |
| Reported total cost, USD | $0.0050722972 | $0.0091129994 |
| Mean sum of client API wall time per episode | 6.33 s | 12.57 s |

Paired results: **0 Jev wins, 10 ties, 2 Jev losses** on the binary primary endpoint.
Cost is the sum of returned `usage.cost`, including Jev—not a list-price estimate.
All 233 calls reported usage. Timing is observed client-side API time, not a
controlled provider-speed measurement; routing, caching and network variability
remain. Preliminary provider checks were separate and excluded from this table.

| Case | Baseline | + Jev |
|---|---:|---:|
| Goal recovery | 3 / 3 | 1 / 3 |
| Browser permission and approval handoff | 3 / 3 | 3 / 3 |
| Queued-job completion verification | 3 / 3 | 3 / 3 |
| Human-facing triage workflow | 3 / 3 | 3 / 3 |

## What happened in the two failures

- [Repeat 1](results/deepseek-pilot-2026-09-20/r1-goal_recovery-jev/events.jsonl):
  the agent repeated an unavailable configuration read, then recovered and saved
  the correct draft on turn 10. It did not explicitly finish within the budget,
  so it failed the predeclared completion criterion despite producing the artifact.
- [Repeat 2](results/deepseek-pilot-2026-09-20/r2-goal_recovery-jev/events.jsonl):
  repeated reads used more turns. The agent fixed the mapping and produced an
  export, but did not inspect/save the draft or finish before the turn cap.

Early Jev advice included `review`/low-probability alternatives; it did not prevent
the repeated reads. The host chose the actual actions. These traces show a failure
to help under this policy, not proof that one specific Jev answer caused every
extra turn. In this toy world, configuration inspection is deliberately unavailable
until an exporter failure; that artificial readiness rule limits generalization.

## Interpretation and limitations

The hypotheses of improved completion and lower overhead were **not supported**
here. A strong baseline and a small, mostly straightforward suite leave little
room for gains. Fixed-interval advice can also be redundant or unhelpful. This is
why the skill recommends decisions at meaningful ambiguity, not a mandatory call
every few steps. That recommendation itself still needs a separate held-out test.

The run is not compute-matched, does not measure multi-hour work, and does not test
native Codex/Claude Code/OpenCode skill invocation. There was no human productivity
study or real browser/payment action. Three repetitions per case do not support
population-level significance or calibration claims. Do not tune the four cases
and present the resulting score as an independent test.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
python3 -m evals.run --live --base-model deepseek/deepseek-v4.1-flash \
  --repeats 3 --output evals/results/my-run
python3 -m evals.summarize evals/results/my-run
```

The new directory must not exist. `--live` spends OpenRouter credits; identical
settings do not guarantee identical model/provider responses. The manifest stores
the exact source used; small release-time wrapper validation changes need not
match the historical source hash. Read [the protocol](README.md) before extending it.

## Separate preflights

- [Five live Jev examples](results/examples-2026-09-20.json) demonstrate the API
  and typed outputs, not benchmark accuracy.
- [Original failed preflight](results/preflight-2026-09-20/manifest.json): all
  base-model calls failed before taking an action. A separate diagnostic observed
  [HTTP 403](results/base-model-diagnostic-2026-09-20.json). The older runner retried
  failed turns; the current runner stops transport failures and aborts fatal errors.
- [DeepSeek plumbing pair](results/deepseek-preflight-2026-09-20/paired.json): both
  arms finished. This preliminary pair is not folded into the three-repeat pilot.
- [GLM Flash preflight](results/glm-preflight-2026-09-20/aborted.json): HTTP 400,
  endpoint requires reasoning and rejected the frozen `none` option. It stopped
  after one call. No completed GLM comparison or result is claimed.
