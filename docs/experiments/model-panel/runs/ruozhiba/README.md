# Ruozhiba MC · everyday misconceptions

20 adapted four-choice items. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 20/20 | 20/20 | 0 | 0 | 0.358 | $0.000404 |
| `deepseek/deepseek-v4-flash` | 20/20 | 20/20 | 0 | — | 1.299 | $0.000289 |
| `qwen/qwen3.5-35b-a3b` | 20/20 | 20/20 | 0 | — | 0.652 | $0.000605 |
| `qwen/qwen3.5-9b` | 20/20 | 20/20 | 0 | — | 0.842 | $0.000339 |
| `meta-llama/llama-3.1-8b-instruct` | 17/20 | 20/20 | 0 | — | 0.363 | $0.000957 |

Easy authored adaptation, independently Agent-reviewed before calls; not official COIG or hard reasoning. Gold longest with ties in 15/20; residual style cues.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `ruozhiba:12`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `D` | `D` |
| `deepseek/deepseek-v4-flash` | `D` | `D` |
| `qwen/qwen3.5-35b-a3b` | `D` | `D` |
| `qwen/qwen3.5-9b` | `D` | `D` |
| `meta-llama/llama-3.1-8b-instruct` | `D` | `D` |

**Try your own data:** ask your Agent: “Use jev on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
