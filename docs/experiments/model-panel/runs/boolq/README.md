# BoolQ · passage-supported answers

20 native validation yes/no questions. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 19/20 | 20/20 | 0 | 1 | 0.369 | $0.000406 |
| `deepseek/deepseek-v4-flash` | 18/20 | 20/20 | 0 | — | 1.251 | $0.000400 |
| `qwen/qwen3.5-35b-a3b` | 19/20 | 20/20 | 0 | — | 0.884 | $0.000746 |
| `qwen/qwen3.5-9b` | 20/20 | 20/20 | 0 | — | 1.065 | $0.000484 |
| `meta-llama/llama-3.1-8b-instruct` | 15/20 | 20/20 | 0 | — | 0.356 | $0.001083 |

Passage supplied directly; no retrieval pipeline was tested.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `boolq:1364`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `No` | `No` |
| `deepseek/deepseek-v4-flash` | `No` | `No` |
| `qwen/qwen3.5-35b-a3b` | `No` | `No` |
| `qwen/qwen3.5-9b` | `No` | `No` |
| `meta-llama/llama-3.1-8b-instruct` | `No` | `No` |

**Try your own data:** ask your Agent: “Use jev-documents on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
