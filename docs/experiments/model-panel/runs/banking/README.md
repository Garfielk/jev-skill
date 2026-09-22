# Banking77 · ticket routing

20 test items / all 77 label options. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 16/20 | 20/20 | 0 | 3 | 0.368 | $0.001437 |
| `deepseek/deepseek-v4-flash` | 16/20 | 20/20 | 0 | — | 1.752 | $0.002009 |
| `qwen/qwen3.5-35b-a3b` | 17/20 | 20/20 | 0 | — | 1.377 | $0.003515 |
| `qwen/qwen3.5-9b` | 15/20 | 20/20 | 0 | — | 1.313 | $0.002061 |
| `meta-llama/llama-3.1-8b-instruct` | 13/20 | 20/20 | 0 | — | 0.386 | $0.004378 |

Intent classification only, not customer-service resolution. Small sample does not cover all 77 gold classes.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `banking:1180`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `why_verify_identity` | `why_verify_identity` |
| `deepseek/deepseek-v4-flash` | `why_verify_identity` | `why_verify_identity` |
| `qwen/qwen3.5-35b-a3b` | `why_verify_identity` | `why_verify_identity` |
| `qwen/qwen3.5-9b` | `why_verify_identity` | `why_verify_identity` |
| `meta-llama/llama-3.1-8b-instruct` | `why_verify_identity` | `why_verify_identity` |

**Try your own data:** ask your Agent: “Use jev-triage on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
