# Context · evidence present versus missing

20 synthetic pairs / 40 decisions. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

### Evidence condition

| Model | Context | Correct | Valid responses | Unknown answers | Errors |
| --- | --- | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | short | 20/20 | 20/20 | 15/20 | 0 |
| `typesafe/jev-1.13` | full | 19/20 | 20/20 | 4/20 | 0 |
| `deepseek/deepseek-v4-flash` | short | 20/20 | 20/20 | 15/20 | 0 |
| `deepseek/deepseek-v4-flash` | full | 20/20 | 20/20 | 5/20 | 0 |
| `qwen/qwen3.5-35b-a3b` | short | 20/20 | 20/20 | 15/20 | 0 |
| `qwen/qwen3.5-35b-a3b` | full | 18/20 | 20/20 | 5/20 | 0 |
| `qwen/qwen3.5-9b` | short | 20/20 | 20/20 | 15/20 | 0 |
| `qwen/qwen3.5-9b` | full | 18/20 | 20/20 | 3/20 | 0 |
| `meta-llama/llama-3.1-8b-instruct` | short | 14/20 | 20/20 | 9/20 | 0 |
| `meta-llama/llama-3.1-8b-instruct` | full | 16/20 | 20/20 | 3/20 | 0 |

Unknown is a valid classification, not an executed decision or a failure. No missing-evidence case receives hypothetical review credit.

### Combined cost and latency

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 39/40 | 40/40 | 0 | 19 | 0.355 | $0.000745 |
| `deepseek/deepseek-v4-flash` | 40/40 | 40/40 | 0 | — | 1.263 | $0.000573 |
| `qwen/qwen3.5-35b-a3b` | 38/40 | 40/40 | 0 | — | 0.843 | $0.001450 |
| `qwen/qwen3.5-9b` | 38/40 | 40/40 | 0 | — | 0.902 | $0.000771 |
| `meta-llama/llama-3.1-8b-instruct` | 30/40 | 40/40 | 0 | — | 0.363 | $0.001766 |

Score each condition against its own gold. Unknown is correct when evidence is missing; more words alone do not guarantee improvement.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `routing-incomplete-short`. The exact question/context/options were identical across models (typed versus chat transport).

```json
{
  "input": {
    "claim": "This ticket should go to the security incident team.",
    "policy": "Route confirmed unauthorized account access to security; ordinary invoice questions go to billing. Ambiguous access reports require investigation.",
    "evidence": "The relevant detailed receipt has not been supplied."
  },
  "options": {
    "supported": "The supplied evidence establishes the claim under the policy.",
    "contradicted": "The supplied evidence establishes that the claim is false under the policy.",
    "unknown": "The supplied evidence does not establish either the claim or its negation."
  }
}
```

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `unknown` | `unknown` |
| `deepseek/deepseek-v4-flash` | `unknown` | `unknown` |
| `qwen/qwen3.5-35b-a3b` | `unknown` | `unknown` |
| `qwen/qwen3.5-9b` | `unknown` | `unknown` |
| `meta-llama/llama-3.1-8b-instruct` | `contradicted` | `unknown` |

**Try your own data:** ask your Agent: “Use jev on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
