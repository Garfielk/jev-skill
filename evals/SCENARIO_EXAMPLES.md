# Scenario example smoke calls — September 20, 2026

Nine synthetic requests covering the eight focused skills and the conversation
example were sent once each through the real OpenRouter Decisions endpoint.
All nine returned protocol-valid responses: **16 questions, no retries**.

This checks that the examples can be called and interpreted. It is **not** a
held-out accuracy test, agent before/after comparison, calibration estimate or
execution of the host actions. No mailbox, browser, desktop app, code repository,
model router, context window, simulator or TTS engine was changed by these calls.

[Full requests, responses, distributions and policy](results/scenario-smoke-2026-09-20.json)

| Example | Observed answer | What was not tested |
|---|---|---|
| [Triage](../skills/jev-triage/assets/example.json) | Bug queue; urgency 1.29 on a 0–2 rubric | Per-message bulk accuracy or queue writes |
| [Documents](../skills/jev-documents/assets/example.json) | Select `s2`; supplied claim contradicted | OCR, retrieval coverage or arbitrary field extraction |
| [UI](../skills/jev-ui/assets/example.json) | `open_policy` | Clicking a real browser/desktop control or observing its result |
| [Routing](../skills/jev-route/assets/example.json) | `reasoning` | Selected model's task quality, cost or a host switch |
| [Context](../skills/jev-context/assets/example.json) | Need `b1`: 0.91; need `b2`: 0.03; work ongoing | Actual pruning/compaction and subsequent task success |
| [Code review](../skills/jev-code-review/assets/example.json) | Test weakened: 0.97; completion unsupported; priority 1.97/2 | Real test execution or vulnerability confirmation |
| [Find code](../skills/jev-find-code/assets/example.json) | Inspect path `p1` | Reading actual source or finding a symbol |
| [Simulation](../skills/jev-simulation/assets/example.json) | `inspect_warehouse` | State transition, long-horizon reward or video rendering |
| [Conversation](../skills/jev/assets/voice-style.json) | Analyst speaks next; calm delivery | Dialogue generation or TTS output |

Numbers after binary propositions are yes-probabilities, not correctness
certificates. Rubric outputs are expected scores, not class probabilities.
The contexts were deliberately simple and author-written. There was no predeclared
accuracy gold set: reporting “100% accuracy” from these outcomes would be misleading.

## Cost and model

- Requested `typesafe/jev-1.13`; all responses resolved to `typesafe/jev-1.13-20260917`.
- Provider-reported combined cost: **$0.000188034**.
- Observed sequential per-request wall time: **0.297–0.363 seconds**.
- Small single-run measurements, not a latency benchmark or a comparison to LLMs.

## Repeat an example

After the [shared CLI setup](../docs/installation.md), inspect/edit the JSON:

```bash
jev-decide decide skills/jev-documents/assets/example.json --dry-run
jev-decide decide skills/jev-documents/assets/example.json > document-receipt.json
```

The first command is free/offline. The second sends the synthetic input to
OpenRouter and incurs usage; keep its JSON response even if the CLI exits 2 for
review. Do not rerun until it gives a preferred answer. For all eight scenarios,
repeat this command with each `skills/jev-*/assets/example.json`; the conversation
request is `skills/jev/assets/voice-style.json`.

For actual outcome evaluation, define success outside Jev, keep matched inputs
and budgets, and test the host loop with and without the decision layer.
[Agent pilot](RESULTS.md) · [Calibration pilot](CALIBRATION_RESULTS.md).
