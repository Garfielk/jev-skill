# BBH · bounded reasoning

160 native questions / 4 tasks. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.

| Model | Correct | Valid | Errors | Review flags | Median seconds | Reported USD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `typesafe/jev-1.13` | 138/160 | 160/160 | 0 | 30 | 0.354 | $0.003099 |
| `deepseek/deepseek-v4-flash` | 108/160 | 160/160 | 0 | — | 1.336 | $0.002951 |
| `qwen/qwen3.5-35b-a3b` | 114/160 | 160/160 | 0 | — | 0.905 | $0.006179 |
| `qwen/qwen3.5-9b` | 102/160 | 160/160 | 0 | — | 1.032 | $0.003583 |
| `meta-llama/llama-3.1-8b-instruct` | 88/160 | 157/160 | 3 | — | 0.366 | unknown (3 missing) |

Native BBH subset, not the full benchmark. Reasoning disabled for the three reasoning-capable chat baselines; not equal-compute comparison.

**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.

## Actual input → output

Frozen input ID: `disambiguation_qa:0`. The exact question/context/options were identical across models (typed versus chat transport).

```json
{
  "input": "In the following sentences, explain the antecedent of the pronoun (which thing the pronoun refers to), or state that it is ambiguous.\nSentence: The patient was referred to the specialist because he had a rare skin condition.\nOptions:\n(A) The patient had a skin condition\n(B) The specialist had a skin condition\n(C) Ambiguous",
  "options": {
    "(A)": "The patient had a skin condition",
    "(B)": "The specialist had a skin condition",
    "(C)": "Ambiguous"
  }
}
```

| Model | Observed choice | Frozen label |
| --- | --- | --- |
| `typesafe/jev-1.13` | `(A)` | `(A)` |
| `deepseek/deepseek-v4-flash` | `(A)` | `(A)` |
| `qwen/qwen3.5-35b-a3b` | `(A)` | `(A)` |
| `qwen/qwen3.5-9b` | `(C)` | `(A)` |
| `meta-llama/llama-3.1-8b-instruct` | `(A)` | `(A)` |

**Try your own data:** ask your Agent: “Use jev on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”

[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)
