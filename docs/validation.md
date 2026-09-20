# Validation snapshot — September 20, 2026

This separates package checks, live model calls, and agent-outcome evidence.
None substitutes for the others.

## Package and skill

- Python unit tests exercise input validation, probability/abstention handling,
  secret-safe errors, transport failures, CLI exit codes, and the independent
  simulator. Run `python3 -m unittest discover -s tests -v`.
- Skill frontmatter passed the bundled skill validator; `npx skills add . --list`
  discovered the `jev` skill.
- An isolated project-local installer test targeted Codex, Claude Code and
  OpenCode. The installer copied the shared `.agents/skills/jev` and Claude's
  `.claude/skills/jev`; OpenCode can discover the shared `.agents` location.
- The copied script successfully validated a bundled example without a key or
API call. No user's existing host configuration or global skill was overwritten.
- Built wheel and source distribution; installed the wheel in a fresh temporary
  Python environment and ran CLI help, `classify --dry-run`, and `decide --dry-run`.
- Checked local documentation links and scanned publication files for the active
  environment key; no broken file links or key occurrences were found.

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
