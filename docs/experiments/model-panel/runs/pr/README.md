# Public PRs · intended value agreement

40 PRs: 30 merged / 10 closed unmerged. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 38/40 | 40/40 | 0 | 4 | 0.374 | $0.005519 |
| `deepseek/deepseek-v4-flash` | 36/40 | 40/40 | 0 | — | 1.697 | $0.009875 |
| `qwen/qwen3.5-35b-a3b` | 33/40 | 40/40 | 0 | — | 1.376 | $0.016887 |
| `qwen/qwen3.5-9b` | 37/40 | 40/40 | 0 | — | 1.127 | $0.012285 |
| `meta-llama/llama-3.1-8b-instruct` | 29/40 | 39/40 | 1 | — | 0.409 | unknown (1 missing) |

Agreement with pre-call host-Agent labels, not independent accuracy or merge eligibility. No no_clear_value/insufficient_evidence gold: bad-PR rejection remains untested.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `psf-requests-7628`. The exact question/context/options were identical across models (typed versus chat transport).

Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `routine_maintenance` | `routine_maintenance` |
| `deepseek/deepseek-v4-flash` | `routine_maintenance` | `routine_maintenance` |
| `qwen/qwen3.5-35b-a3b` | `routine_maintenance` | `routine_maintenance` |
| `qwen/qwen3.5-9b` | `routine_maintenance` | `routine_maintenance` |
| `meta-llama/llama-3.1-8b-instruct` | `substantive` | `routine_maintenance` |

**Try your own data:** ask your Agent: “Use jev-eval on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
