# LogiQA 2.0 · Chinese logic

20 native four-choice test items. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 16/20 | 20/20 | 0 | 6 | 0.350 | $0.000506 |
| `deepseek/deepseek-v4-flash` | 19/20 | 20/20 | 0 | — | 1.141 | $0.000405 |
| `qwen/qwen3.5-35b-a3b` | 18/20 | 20/20 | 0 | — | 0.866 | $0.000866 |
| `qwen/qwen3.5-9b` | 16/20 | 20/20 | 0 | — | 1.150 | $0.000506 |
| `meta-llama/llama-3.1-8b-instruct` | 13/20 | 19/20 | 1 | — | 0.356 | unknown (1 missing) |

Small unstratified Chinese pilot; do not generalize 20 items to the full benchmark.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `logiqa:11084`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `A` | `B` |
| `deepseek/deepseek-v4-flash` | `B` | `B` |
| `qwen/qwen3.5-35b-a3b` | `B` | `B` |
| `qwen/qwen3.5-9b` | `B` | `B` |
| `meta-llama/llama-3.1-8b-instruct` | `B` | `B` |

**Try your own data:** ask your Agent: “Use jev on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
