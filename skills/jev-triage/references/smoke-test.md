# Smoke-test the labels before scaling

`smoke_test` is a parameter of the existing **jev-triage** skill, not a new skill
or a Jev API field. The agent reads the parameters and invokes the bundled runner.

**Release status:** this addition is not included in the pinned v0.2.0 install.
Use the reviewed source revision for preview; normal installers must not silently
replace their release pin. Publish updated skill archives after maintainer merge.

## Invoke with parameters

Claude Code:

```text
/jev-triage smoke_test=true sample_size=50 input=job.json
```

Codex:

```text
$jev-triage smoke_test=true sample_size=50 input=job.json
```

OpenCode / portable prompt:

```text
Use jev-triage with smoke_test=true, sample_size=50 and input=job.json.
Show the plan, then run only the approved paired sample. Do not start the full job.
```

Claude Code documents argument substitution and appending the supplied argument
text when no placeholder is used. Codex documents explicit `$skill` invocation;
we interpret the following named values in the skill instructions, not an asserted
Codex-native argument schema. OpenCode's skill tool loads by name; pass the values
in the user message. Its `$ARGUMENTS` substitution belongs to custom commands,
not automatically to every skill. Do not install a command wrapper just for this.

## Parameters

| Skill parameter | Default | Runner flag / meaning |
|---|---|---|
| `smoke_test` | `true` for bulk labeling | `--smoke-test true`; `false` requires an explicit user waiver and reports skipped, never passed |
| `input` | required | Positional job JSON path; agent prepares it from authorized records |
| `sample_size` | `50` | `--sample-size`; integer 1–100, capped to available records |
| `timeout` | `30` seconds | `--timeout`; per-request limit, 0.1–300 seconds, never an automatic retry |
| `seed` | `0` | `--seed`; reproducible sampling and saved record IDs |
| `provider` | user's selected Jev route | `--provider openrouter` or `typesafe`; never switch silently |
| `reference_model` | `deepseek/deepseek-v4-flash` | `--reference-model`; OpenRouter model ID, independently invoked |
| `min_accuracy` | `0.90` | `--min-accuracy`; example acceptance threshold, agree before running |
| `max_accuracy_gap` | `0.05` | `--max-accuracy-gap`; maximum allowed Jev shortfall vs reference on gold labels |

These thresholds are starting policy settings, not proof of statistical equivalence
or universal quality. Small samples cannot certify rare failures. If the user asks
for a different sample size/model, honor it within the runner's bounds; don't
silently spend more. Parse Boolean `false` as false, not as a truthy string.

## Input and execution

The [20-record synthetic fixture](../assets/smoke-job.json) is a format and transport
test, **not a production benchmark**. It contains maintainer-authored labels.
A job has described `criteria`, optional shared `context`, and `records` with
unique `id`, `text`, optional per-record `context`, optional `gold` and `stratum`.
Only evidence/context and criteria go to the two models; `gold` and `stratum` stay
out of their requests. Do not bury answer keys in text or shared context.

The runner takes seeded random samples within supplied strata in round-robin
order. This intentionally balances those strata, not necessarily the population;
its aggregate accuracy is **sample accuracy**, not a population-weighted estimate.
Without strata it uses a seeded random sample. The agent should prepare meaningful
strata (such as source, language, length or edge-case group) before approval.

The installing agent supplies the existing shared `jev` Python module from
`jev-skill`, or copies the complete skill collection. The runner also works from a
source checkout. Resolve `<skill-dir>` to the installed **jev-triage** folder.

```bash
# No network: inspect the selected records before sending anything.
python <skill-dir>/scripts/smoke_test.py job.json --smoke-test true --sample-size 50
# After approval of both destinations, sample and usage; directory must be new:
python <skill-dir>/scripts/smoke_test.py job.json --smoke-test true --sample-size 50 \
  --provider openrouter --live --output smoke-run
```

Native Jev uses `--provider typesafe` and `TYPESAFE_API_KEY`; the reference still
needs `OPENROUTER_API_KEY`. Check both first. Without the reference key, ask the user
whether to configure it or explicitly skip the paired pilot; never manufacture a
comparison using current-agent simulation. Follow the existing setup A/B policy.

Every selected record gets one Jev request and one reference request with the same
context, criteria and classification question. Calls are sequential and stop on
the first error; **at most 2 × sample_size requests**, no retries or full-job branch.
Reference output is bounded to 512 tokens with reasoning disabled; truncation is a
failed comparison, not a label. Larger inputs still cost more: review the input,
current model prices and intended request budget before `--live`.

## Read the result, then decide

- `manifest.json`: frozen input hash, sampled IDs/evidence, labels, parameters and models.
- `receipts.jsonl`: actual requests/responses, elapsed time and sanitized errors,
  flushed after each call. Keep these local for private datasets.
- `report.json`: each pair of labels, disagreements, valid-pair coverage, sample
  accuracy/per-class counts on valid labeled responses, explicit scored counts and
  reported model costs. Incomplete coverage cannot pass even when valid-pair agreement is 100%. Unknown
  billing is null, not zero. Raw receipts retain token usage and returned model IDs.

**No gold → agreement only → `needs_review`.** DeepSeek is a comparator, not ground
truth. Inspect disagreement cases **and some agreement cases**, obtain labels or
explicit human review before approving the population. Missing/invalid answers
and Jev uncertainty also require review. Don't drop failures from the job silently.

`sample_check_passed` requires complete valid pairs and gold labels, no Jev review
flags, and the configured accuracy/gap checks. Even then `bulk_authorized` is always
false: the host must show the report and obtain the user's scope/budget approval.
Exit 0 means a completed passing sample; 2 means review/skipped; 1 means setup/input
failure. A dry run also exits 0 but is explicitly `mode: dry_run`, never a pass.

Once approved, the **existing** host-controlled bulk workflow continues; there is
no second skill or automatic bulk executor. Freeze the tested rubric/context and
retest after material changes. Compare the intended multi-record batch shape too
before increasing records per request: this runner checks **one record per call**,
not cross-record batch contamination or concurrent throughput.

## Sources and test scope

Checked September 21, 2026:

- [Claude Code: skill arguments](https://code.claude.com/docs/en/skills#pass-arguments-to-skills)
- [Codex: skills](https://developers.openai.com/codex/skills/)
- [OpenCode: skills](https://opencode.ai/docs/skills/) and [command arguments](https://opencode.ai/docs/commands/#arguments)
- [DeepSeek V4 Flash on OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash)

Parser/unit/copied-file tests and API receipts establish different things. Do not
claim native slash-command execution in all three hosts without separate host runs.

[Actual pilot results and preserved failure](../../../evals/TRIAGE_SMOKE_TEST.md).
