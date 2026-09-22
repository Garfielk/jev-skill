# BFCL · tool name selection

20 multiple-tool examples, function name only. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 20/20 | 20/20 | 0 | 0 | 0.351 | $0.000633 |
| `deepseek/deepseek-v4-flash` | 20/20 | 20/20 | 0 | — | 1.590 | $0.000957 |
| `qwen/qwen3.5-35b-a3b` | 20/20 | 20/20 | 0 | — | 0.901 | $0.001695 |
| `qwen/qwen3.5-9b` | 20/20 | 20/20 | 0 | — | 1.124 | $0.001049 |
| `meta-llama/llama-3.1-8b-instruct` | 20/20 | 20/20 | 0 | — | 0.386 | $0.002340 |

Not official BFCL score: arguments, execution and final task success are NOT scored. Every model saturated this subset.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `multiple_0`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `triangle_properties.get` | `triangle_properties.get` |
| `deepseek/deepseek-v4-flash` | `triangle_properties.get` | `triangle_properties.get` |
| `qwen/qwen3.5-35b-a3b` | `triangle_properties.get` | `triangle_properties.get` |
| `qwen/qwen3.5-9b` | `triangle_properties.get` | `triangle_properties.get` |
| `meta-llama/llama-3.1-8b-instruct` | `triangle_properties.get` | `triangle_properties.get` |

**Try your own data:** ask your Agent: “Use jev-act on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
