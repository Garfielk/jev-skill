# Validation snapshot — September 20, 2026

This separates package checks, live model calls, and agent-outcome evidence.
None substitutes for the others.

## Package and skill

- Python unit tests exercise input validation, probability/abstention handling,
  secret-safe errors, transport failures, CLI exit codes, and the independent
  simulator. Run `python3 -m unittest discover -s tests -v`.
- All **75 unit tests** passed, including eight isolated scenario-folder dry runs
  with the network patched out and no sibling `jev` skill present.
- All **nine skill entrypoints** passed the bundled skill validator;
  `npx skills add . --list` discovered all nine.
- An isolated project-local installer test targeted Codex, Claude Code and
  OpenCode. The installer copied all nine folders to shared `.agents/skills/` and
  Claude's `.claude/skills/`; OpenCode can discover the shared `.agents` location.
- The copied general-skill script validated the new voice example in both locations
  without a key or API call. No existing host configuration or global skill was overwritten.
- Built wheel and source distribution; installed the wheel in a fresh temporary
  Python environment. CLI help and all eight scenario examples passed in each
  copied location (**16 installed-example dry runs**). The source distribution
  was checked for all nine skills and eight scenario assets.
- Checked local documentation links and matching EN/ZH navigation anchors; both
  READMEs have 85 scenario/integration blocks covering all 56 recipe IDs,
  22 implementation patterns and seven X workflow leads. Tests verify that
  all 14 displayed API outputs match the saved receipts exactly (apart from
  omitted score-level descriptions). Publication text was scanned for the active
  environment key without displaying it; no occurrences were found.

These establish packaging and skill discovery through the installer, **not native
end-to-end execution inside all three clients**. An independent skill-following
review also prepared a valid dry-run request for a reading-only browser task and
a queued-job completion check. It did not execute a browser or use a model API.

## Live Jev examples

Five bundled synthetic requests were sent through the real OpenRouter Decisions
endpoint, resolving to `typesafe/jev-1.13-20260917`.

| Example | Observed answer |
|---|---|
| Agent checkpoint | Inspect the failing input; repeated-failure proposition 0.88 |
| Browser routing | Select the observed cancellation-policy link, not a purchase |
| Support triage | Billing, human evidence check, middle urgency level |
| Completion evidence | Claimed completion unsupported: yes-probability 0.02 |
| Idea rubric | Audience-fit score 1.98/2; demand remains untested |

[Full requests and responses](../evals/results/examples-2026-09-20.json) include
model identifiers, usage and latency. Reported combined cost was **$0.000105714**;
per-request wall time was approximately **0.31–0.52 seconds** in these calls.
These are small, hand-authored API smoke examples, not an accuracy or speed benchmark.

## New scenario API examples

The eight focused examples plus speaker/style selection were each called once
through OpenRouter: **nine protocol-valid responses, 16 questions, no retries**.
Provider-reported combined cost was **$0.000188034**, with observed per-call wall
time **0.297–0.363 seconds**. These use synthetic input and execute no host actions.
The [result table and reproduction commands](../evals/SCENARIO_EXAMPLES.md) link
to full request/response receipts. They are not scenario accuracy measurements.

## Agent comparison

See [the evaluation protocol](../evals/README.md) and the committed result receipts.
The initial OpenAI-model preflight failed before any task action; a separate
diagnostic returned HTTP 403. Those records are retained, not scored as a model
quality result. The user then explicitly selected other permitted model families.
The GLM Flash preflight returned HTTP 400 because that endpoint requires reasoning;
it was stopped without repeated failed requests. Neither failure is an agent-effect
comparison. The [completed DeepSeek pilot](../evals/RESULTS.md) contains 24 episodes:
baseline 12/12 completed versus fixed Jev checkpoints 10/12. It is a small negative
result for that integration policy, not a validation of all recipes.

## Decision calibration pilot

The [separate BBH pilot](../evals/CALIBRATION_RESULTS.md) completed 320 paid calls
on 160 original labeled questions. Jev matched 136/160 labels; its API-confidence
>=0.9 subset matched 92/100, but causal judgment within that band matched only
14/20. Full distributions, reliability bins, Brier/NLL, routing diagnostics,
provider usage and failed baseline label spellings are retained. This is not
a deployment threshold certificate. Strict baseline and post-hoc bracket-only
normalization are kept separate; no failed question was rerun.
