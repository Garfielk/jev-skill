# BBH decision and calibration pilot — September 20, 2026

**Completed: 160 items × two models = 320 real API calls.** This is a sampled
zero-shot decision stress test, not a full BBH score or a deployment certificate.
[Protocol](CALIBRATION.md) · [Frozen inputs and receipts](results/calibration-bbh-2026-09-20)

## Main result

Jev matched **136/160 (85%)** reference labels. Its `confidence >= 0.90` band
matched **92/100 (92%)**, but still contained **eight wrong labels**. The
illustrative threshold is therefore a routing policy, not permission or a
certainty guarantee. Task composition matters much more than one aggregate.

| Task | Jev | DeepSeek strict interface | DeepSeek bracket-normalized* |
|---|---:|---:|---:|
| Pronoun disambiguation | 36/40 (90%) | 21/40 (52.5%) | 26/40 (65%) |
| Typical-person causal judgment | 22/40 (55%) | 25/40 (62.5%) | 25/40 (62.5%) |
| Three-object logical deduction | 40/40 (100%) | 37/40 (92.5%) | 39/40 (97.5%) |
| Sarcasm identification | 38/40 (95%) | 37/40 (92.5%) | 37/40 (92.5%) |
| **Total** | **136/160 (85%)** | **120/160 (75%)** | **127/160 (79.4%)** |

*The secondary bracket-only audit is post-hoc, not a preregistered headline
metric. DeepSeek returned nine native-label spelling violations such as `A`
instead of `(A)`. Strict receipts and results are unchanged; the separate audit
repairs only that format, without consulting the reference label or making new
calls. All Jev responses passed the interface checks. There were no transport
errors. DeepSeek used reasoning `none`; it is not established as a stronger
reviewer for these tasks. This is not a best-prompt or equal-compute comparison.

## Are the probabilities calibrated?

| Jev probability measure | Observed |
|---|---:|
| Mean maximum label probability | 0.9104 |
| Exact-match accuracy | 0.8500 |
| Multiclass Brier, sum-over-classes convention | 0.2560 |
| NLL, natural log, floor `1e-12` | 0.5974 |
| Top-label ECE, 10 equal-width bins | 0.0994 |
| Zero reported gold probabilities | 1 |
| Distributions requiring sum normalization | 0 |

The high-probability `[.9,1]` bin had **118 items**, mean probability **0.9814**,
and accuracy **105/118 = 0.8898**. That bin was overconfident relative to these
reference labels. A low ECE is not sufficient to certify an application, and
this small, mixed-domain sample is not sufficient to reject or verify RLCD's
general training claims. No probability recalibration was fitted.

| Top-probability bin | n | Mean probability | Observed accuracy |
|---|---:|---:|---:|
| `[.5,.6)` | 8 | .5463 | .6250 |
| `[.6,.7)` | 11 | .6236 | .7273 |
| `[.7,.8)` | 9 | .7389 | .8889 |
| `[.8,.9)` | 14 | .8557 | .7143 |
| `[.9,1]` | 118 | .9814 | .8898 |

Lower bins were empty. The one zero gold probability was API-rounded, not a
measurement of its unrounded internal belief; NLL depends on the stated floor.

## Your 0.9 / 0.7 confidence policy

These numbers describe **Jev's initial decisions in each API-confidence band**,
not decisions made by a reviewer or human:

| API confidence | Items / coverage | Jev correct | Wilson 95% interval |
|---|---:|---:|---:|
| `>= .90` | 100 / 62.5% | 92/100 (92.0%) | 85.0%–95.9% |
| `[.70,.90)` | 27 / 16.9% | 19/27 (70.4%) | 51.5%–84.1% |
| `< .70` | 33 / 20.6% | 25/33 (75.8%) | 59.0%–87.2% |

The middle and lower bands are **not monotonically ordered** in this sample.
A low score can reflect genuinely ambiguous text whose correct benchmark answer
is “Ambiguous”, rather than a wrong prediction. These small descriptive bins
should not be treated as universal mappings from confidence to correctness.

Most importantly, the same high-confidence cutoff gave very different task
results: **causal judgment 14/20 (70%)**, disambiguation 12/13, logic 40/40 and
sarcasm 26/27. Six of the eight high-confidence errors were in causal judgment.
Even the pooled 92% figure is not an appropriate promise for that task.

Using **top probability** instead of `confidence` changes the accepted set:
118/160 items and 105/118 (89.0%) correct at `>= .90`, versus 100 and 92/100
for API confidence. Do not silently exchange these two signals. The saved
confidence-score/ECE-style diagnostic is not presented as probability ECE.

## Simulated reviewer cascade

The confidence-based policy keeps 100 Jev labels, selects DeepSeek's independently
collected label for 27 medium-band items, and leaves 33 items for a human. In
strict mode, DeepSeek matches 16/27 selected labels, versus Jev's own 19/27 on
those same items. The chosen reviewer did **not** improve this band; model size
or name is not evidence that it is a better specialist.

Strict cascade result: **108/127 (85.0%) correct per attempted automatic
classification**, 79.4% attempted coverage, 78.8% valid-answer coverage, one
unresolved interface error, and **33 human items left unresolved**. Humans receive
no oracle credit. See the separate bracket-normalized diagnostic for format-only
changes. These are offline label replays, not an executed production cascade;
no human accuracy, cost savings, or latency savings were measured.

The [bracket-only diagnostic](results/calibration-bbh-2026-09-20/label-audit.json)
recovers all nine response formats, seven of which match gold. In the confidence
review band, normalized DeepSeek matches **17/27**, still below Jev’s own 19/27.
The normalized confidence cascade is **109/127 (85.8%)**, with 33 human items
still unresolved. For top-probability routing, strict/normalized automatic
accuracy is 120/141 (85.1%) / 121/141 (85.8%), leaving 19 human items unresolved.

## Cost, latency and provenance

| Observed API totals | Jev | DeepSeek V4.1 Flash |
|---|---:|---:|
| Calls | 160 | 160 |
| Reported input / output tokens | 74,898 / 6,080 | 34,645 / 1,192 |
| Reported cost, USD | $0.003145716 | $0.0084470118 |
| Sum of request wall times | 59.711 s | 246.694 s |
| Mean request wall time | 0.373 s | 1.542 s |

Combined reported cost: **$0.0115927278**. Latencies are local observations,
not model-only compute measurements. Models have different request framing and
output contracts. OpenRouter provider routing was not pinned: Jev resolved to
`typesafe/jev-1.13-20260917` / TypeSafe; DeepSeek returned
`deepseek/deepseek-v4.1-flash` across multiple providers. Full IDs, providers and
usage remain in the receipts.

The raw campaign, frozen code, sample hashes, prompts, sampling seed, gold labels
and source notices are included. After completion, the summary function gained
a read-only mode for the post-hoc audit; the originally executed source remains
in `manifest.json`. No model calls or test questions were replaced.

## Implication for the skill

Keep the three-way **act / review / defer** idea, but validate each question family
and reviewer, not a global numeric magic threshold. Preserve authorization and
verification separately. This sample gives useful evidence of inexpensive typed
decisions and domain-dependent uncertainty; it does not establish safe unattended
actions, a general long-horizon agent improvement, or calibrated probabilities
on a user's private workload. Ruozhiba/ComVE/FalseQA remain follow-up datasets,
not additional completed results.
