# Jev Skill

**A decision toolbox for agents and people.** Use [TypeSafe Jev](https://typesafe.ai/)
through OpenRouter to classify situations, choose bounded next steps, and score
evidence—not generate more prose.

[中文](README.zh.md) · [Recipes](skills/jev/references/index.md) · [Field reports](skills/jev/references/community.md) · [Evaluation](evals/README.md)

## Where it helps

| For agents | For people |
|---|---|
| Recover from loops and goal drift | Sort messages, logs, documents, and feedback |
| Route tools, skills, models, and specialists | Screen papers, label datasets, align entities |
| Select a next step from an observed browser page | Compare ideas, designs, and content with rubrics |
| Check completion claims against real evidence | Flag policy exceptions and ambiguous cases for review |

The [56-recipe catalog](skills/jev/references/index.md) separates observed community
uses from proposed adaptations, with concrete inputs, questions, and caveats.

## Install the skill

```bash
npx skills add wuyoscar/jev-skill --skill jev
export OPENROUTER_API_KEY="your-key"
```

Select **Codex**, **Claude Code**, or **OpenCode** in the installer. Python 3.10+
is required; the bundled script has no third-party runtime dependencies. Restart
your agent if needed. Its process must inherit the environment variable.

Try: “Use Jev to check why this task is stuck and choose a next step from the
available tools.” Or: “Use Jev to classify these support messages; flag ambiguous
ones for review.” See [manual installation](docs/installation.md).

## Use it yourself

```bash
uv tool install git+https://github.com/wuyoscar/jev-skill.git@v0.1.0
```

Create `labels.json` with descriptive categories:

```json
{"billing":"Charges, invoices or refunds","bug":"Broken software behavior","other":"Unclear or no matching category"}
```

```bash
jev-decide classify --text "I was charged twice" --criteria labels.json
jev-decide decide request.json --dry-run  # validate without spending
jev-decide decide request.json            # state + choice/noul/score questions
```

Returns JSON with selected labels, uncertainty status, raw answers, latency, and
provider-reported usage. Exit `0`: selected/scored; `2`: review needed; `1`: error.
[Request examples](skills/jev/assets) · [API reference](skills/jev/references/api.md)

## What it does not do

Jev does not execute tools or browse by itself. The host agent supplies observations
and performs authorized actions. A skill is **guidance, not an enforcement hook**.
Jev can be wrong or manipulated; it cannot grant consent, verify unseen outcomes,
or replace deterministic checks and human review. Text/JSON sent for judgment goes
to OpenRouter and its provider. This is an open-source integration, **not Jev model weights**.

## Uncertainty-aware decisions

Route easy cases, review uncertain ones, and defer when evidence is insufficient.
Jev’s `confidence` is not the probability of being correct: validate thresholds
on your own labels. [Calibration guide](skills/jev/references/calibration.md) ·
[Decision benchmark](evals/CALIBRATION.md)

## Evidence, not promises

The [paired evaluation](evals/README.md) compares the same agent with and without
Jev checkpoint advice using deterministic simulated outcomes. In [12 paired pilot
trials](evals/RESULTS.md), the baseline completed **12/12**, versus **10/12** with
fixed Jev checkpoints, at higher cost. Five live Jev examples also passed.
Use the toolbox selectively; this pilot does **not** show a general agent improvement.

In a separate [160-item decision test](evals/CALIBRATION_RESULTS.md), Jev matched
85% of benchmark labels. Its confidence ≥0.9 group still had 8/100 wrong answers;
validate each domain before trusting a routing threshold.

Inspired by the [official Jev skill](https://docs.typesafe.ai/agent-skill),
[JevRouter](https://github.com/BillionsBobby/JevRouter), and community experiments.
Our focus is a reusable recipe library, agent/human dual use, and transparent tests.
Independent project; not affiliated with TypeSafe or OpenRouter. [MIT](LICENSE).
