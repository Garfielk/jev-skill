# OCNLI · Chinese inference

20 native three-way dev items. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 18/20 | 20/20 | 0 | 3 | 0.364 | $0.000362 |
| `deepseek/deepseek-v4-flash` | 16/20 | 20/20 | 0 | — | 1.302 | $0.000241 |
| `qwen/qwen3.5-35b-a3b` | 18/20 | 20/20 | 0 | — | 0.911 | $0.000578 |
| `qwen/qwen3.5-9b` | 19/20 | 20/20 | 0 | — | 0.989 | $0.000312 |
| `meta-llama/llama-3.1-8b-instruct` | 9/20 | 20/20 | 0 | — | 0.366 | $0.000825 |

50 no-consensus records excluded before sampling. Entailment of a hypothesis is not fact-checking the world.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `ocnli:1160`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `neutral` | `neutral` |
| `deepseek/deepseek-v4-flash` | `neutral` | `neutral` |
| `qwen/qwen3.5-35b-a3b` | `neutral` | `neutral` |
| `qwen/qwen3.5-9b` | `neutral` | `neutral` |
| `meta-llama/llama-3.1-8b-instruct` | `contradiction` | `neutral` |

**Try your own data:** ask your Agent: “Use jev-documents on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
