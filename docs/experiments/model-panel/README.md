# Jev × four chat models

Same items, real calls, failures retained. **2026-09-22 · small pilots, not a universal leaderboard.**

| Experiment | N | Jev | DeepSeek V4 Flash | Qwen35B A3B | Qwen9B | Llama3.1 8B |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [BBH · bounded reasoning](runs/bbh/README.md) | 160 | 138/160 | 108/160 | 114/160 | 102/160 | 88/160 |
| [LogiQA 2.0 · Chinese logic](runs/logiqa/README.md) | 20 | 16/20 | 19/20 | 18/20 | 16/20 | 13/20 |
| [OCNLI · Chinese inference](runs/ocnli/README.md) | 20 | 18/20 | 16/20 | 18/20 | 19/20 | 9/20 |
| [Ruozhiba MC · everyday misconceptions](runs/ruozhiba/README.md) | 20 | 20/20 | 20/20 | 20/20 | 20/20 | 17/20 |
| [Context · evidence present versus missing](runs/context/README.md) | 40 | 39/40 | 40/40 | 38/40 | 38/40 | 30/40 |
| [Public PRs · intended value agreement](runs/pr/README.md) | 40 | 38/40 | 36/40 | 33/40 | 37/40 | 29/40 |
| [Banking77 · ticket routing](runs/banking/README.md) | 20 | 16/20 | 16/20 | 17/20 | 15/20 | 13/20 |
| [BoolQ · passage-supported answers](runs/boolq/README.md) | 20 | 19/20 | 18/20 | 19/20 | 20/20 | 15/20 |
| [BFCL · tool name selection](runs/bfcl/README.md) | 20 | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 |
| [Prompt injection · narrow dataset labels](runs/injection/README.md) | 20 | 17/20 | 17/20 | 18/20 | 19/20 | 16/20 |

## Agent before / after

Same `deepseek/deepseek-v4-flash`, tools, initial states and 10-turn cap; Jev advice at steps 3/6/9. Four synthetic pairs, one repeat. Final states replayed from actual actions.

| Arm | Verified success | Unsafe attempts | API calls | Failed calls | USD | Mean API seconds / episode |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 3/4 | 0 | 35 | 0 | $0.000855 | 14.07 |
| jev | 4/4 | 0 | 44 | 0 | $0.001585 | 16.35 |

[Full requests, responses and final states](../../../evals/results/agent-v4-panel-2026-09-22) · [Offline summary](agent-summary.json)

## Main results / 主要结果

- Jev leads this BBH subset, but not every task: DeepSeek leads LogiQA; Qwen9B leads OCNLI, BoolQ and injection in these samples.
- The Agent pilot improves 3/4 → 4/4 with extra calls; the [earlier 12-pair negative result](../../../evals/RESULTS.md) remains 12/12 → 10/12. Neither proves a general integration benefit.
- Tool-name and easy Ruozhiba subsets mostly saturate. Use harder, held-out data from your workload before choosing a model.

Full model IDs, actual costs, latency, errors and review flags are in each linked table. No cross-task aggregate ranking. Chat probability metrics are **N/A**; Jev option probabilities and distribution-shape confidence are separate in the offline metrics.

**复现 / Reproduce:** [protocol, licenses, commands, limits and failed preflights](REPRODUCE.md). Reports are source-free where redistribution is unclear; raw records are retained locally, not silently discarded.
