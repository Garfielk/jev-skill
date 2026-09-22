"""Regenerate the compact overview and per-experiment result pages, offline."""

def main():
    from pathlib import Path
    import json
    from evals.summarize import summarize
    root = Path('docs/experiments/model-panel')
    info = {'bbh': ('BBH · bounded reasoning', '160 native questions / 4 tasks', 'jev', 'Native BBH subset, not the full benchmark. Reasoning disabled for the three reasoning-capable chat baselines; not equal-compute comparison.'), 'logiqa': ('LogiQA 2.0 · Chinese logic', '20 native four-choice test items', 'jev', 'Small unstratified Chinese pilot; do not generalize 20 items to the full benchmark.'), 'ocnli': ('OCNLI · Chinese inference', '20 native three-way dev items', 'jev-documents', '50 no-consensus records excluded before sampling. Entailment of a hypothesis is not fact-checking the world.'), 'ruozhiba': ('Ruozhiba MC · everyday misconceptions', '20 adapted four-choice items', 'jev', 'Easy authored adaptation, independently Agent-reviewed before calls; not official COIG or hard reasoning. Gold longest with ties in 15/20; residual style cues.'), 'context': ('Context · evidence present versus missing', '20 synthetic pairs / 40 decisions', 'jev', 'Score each condition against its own gold. Unknown is correct when evidence is missing; more words alone do not guarantee improvement.'), 'pr': ('Public PRs · intended value agreement', '40 PRs: 30 merged / 10 closed unmerged', 'jev-eval', 'Agreement with pre-call host-Agent labels, not independent accuracy or merge eligibility. No no_clear_value/insufficient_evidence gold: bad-PR rejection remains untested.'), 'banking': ('Banking77 · ticket routing', '20 test items / all 77 label options', 'jev-triage', 'Intent classification only, not customer-service resolution. Small sample does not cover all 77 gold classes.'), 'boolq': ('BoolQ · passage-supported answers', '20 native validation yes/no questions', 'jev-documents', 'Passage supplied directly; no retrieval pipeline was tested.'), 'bfcl': ('BFCL · tool name selection', '20 multiple-tool examples, function name only', 'jev-act', 'Not official BFCL score: arguments, execution and final task success are NOT scored. Every model saturated this subset.'), 'injection': ('Prompt injection · narrow dataset labels', '20 deepset test items', 'jev-eval', 'Role-changing instructions count as INJECTION under this dataset convention, even benign role-play. Not real-world maliciousness or jailbreak success.')}
    models = list(json.load(open(root / 'runs/bbh/summary.json')))
    lines = ['# Jev × four chat models', '', 'Same items, real calls, failures retained. **2026-09-22 · small pilots, not a universal leaderboard.**', '', '| Experiment | N | Jev | DeepSeek V4 Flash | Qwen35B A3B | Qwen9B | Llama3.1 8B |', '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for name, (title, n, skill, limit) in info.items():
        d = json.load(open(root / 'runs' / name / 'summary.json'))
        count = d[models[0]]['attempted']
        lines.append(f'| [{title}](runs/{name}/README.md) | {count} | ' + ' | '.join((f"{d[m]['correct']}/{count}" for m in models)) + ' |')
        run = root / 'runs' / name
        index = json.load(open(run / 'index.json'))
        records = json.load(open(run / 'records.json'))
        first = index['sample_ids'][0]
        example = [r for r in records if r['id'] == first]
        text = [f'# {title}', '', n + '. **Correct / all attempts**; PR rows mean annotation agreement. Failures count wrong.', '', (run / 'table.md').read_text().strip(), '', limit, '', '**Read the result:** review flags are not executed review; no accuracy credit is given for hypothetical escalation. Costs are observed provider billing; unknown costs are never zero. Latency is client wall time including network, with at most 4 requests in flight per campaign.', '', '## Actual input → output', '', f'Frozen input ID: `{first}`. The exact question/context/options were identical across models (typed versus chat transport).', '']
        if name == 'context':
            condition_table = ['### Evidence condition', '', '| Model | Context | Correct | Valid responses | Unknown answers | Errors |', '| --- | --- | ---: | ---: | ---: | ---: |']
            for model in models:
                for condition in ('context_short', 'context_full'):
                    row = d[model]['by_task'][condition]
                    condition_table.append(f"| `{model}` | {condition.removeprefix('context_')} | {row['correct']}/{row['attempted']} | {row['valid']}/{row['attempted']} | {row['unknown_predictions']}/{row['attempted']} | {row['errors']} |")
            condition_table += ['', 'Unknown is a valid classification, not an executed decision or a failure. No missing-evidence case receives hypothetical review credit.', '', '### Combined cost and latency', '']
            text[4:4] = condition_table
        if name in ('context', 'bbh'):
            source = Path('evals/results') / ('panel-context-network-2026-09-22' if name == 'context' else 'panel-bbh-2026-09-22') / 'samples.json'
            sample = next((s for s in json.load(open(source)) if s['id'] == first))
            text += ['```json', json.dumps({'input': sample['input'], 'options': sample['criteria']}, ensure_ascii=False, indent=2), '```', '']
        else:
            text += ['Source-bearing input is intentionally not republished here. [Reconstruct the exact input locally](../../REPRODUCE.md), then open `samples.json` at this ID; source revision and hashes are in [the index](index.json).', '']
        text += ['| Model | Observed choice | Frozen label |', '| --- | --- | --- |']
        text += [f"| `{r['model']}` | `{r.get('prediction', 'ERROR')}` | `{r['target']}` |" for r in example]
        text += ['', f'**Try your own data:** ask your Agent: “Use {skill} on a small labeled holdout, keep the full relevant context and legal options, compare against my chosen baseline, and show correctness, failures, cost and latency before scaling.”', '', '[Protocol and sources](../../REPRODUCE.md) · [Derived records](records.json) · [Per-task/per-label metrics and calibration](summary.json) · [Run index](index.json)', '']
        (run / 'README.md').write_text('\n'.join(text))
    agent = summarize('evals/results/agent-v4-panel-2026-09-22')
    json.dump(agent, open(root / 'agent-summary.json', 'w'), indent=2)
    lines += ['', '## Agent before / after', '', 'Same `deepseek/deepseek-v4-flash`, tools, initial states and 10-turn cap; Jev advice at steps 3/6/9. Four synthetic pairs, one repeat. Final states replayed from actual actions.', '', '| Arm | Verified success | Unsafe attempts | API calls | Failed calls | USD | Mean API seconds / episode |', '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for arm, r in agent['arms'].items():
        lines.append(f"| {arm} | {r['successes']}/{r['episodes']} | {r['unsafe_attempts']} | {r['api_calls']} | {r['failed_api_calls']} | ${r['reported_cost_usd']:.6f} | {r['mean_api_seconds']:.2f} |")
    lines += ['', '[Full requests, responses and final states](../../../evals/results/agent-v4-panel-2026-09-22) · [Offline summary](agent-summary.json)', '', '## Main results / 主要结果', '', '- Jev leads this BBH subset, but not every task: DeepSeek leads LogiQA; Qwen9B leads OCNLI, BoolQ and injection in these samples.', '- The Agent pilot improves 3/4 → 4/4 with extra calls; the [earlier 12-pair negative result](../../../evals/RESULTS.md) remains 12/12 → 10/12. Neither proves a general integration benefit.', '- Tool-name and easy Ruozhiba subsets mostly saturate. Use harder, held-out data from your workload before choosing a model.', '', 'Full model IDs, actual costs, latency, errors and review flags are in each linked table. No cross-task aggregate ranking. Chat probability metrics are **N/A**; Jev option probabilities and distribution-shape confidence are separate in the offline metrics.', '', '**复现 / Reproduce:** [protocol, licenses, commands, limits and failed preflights](REPRODUCE.md). Reports are source-free where redistribution is unclear; raw records are retained locally, not silently discarded.', '']
    (root / 'README.md').write_text('\n'.join(lines))
if __name__ == '__main__':
    main()
