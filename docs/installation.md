# Manual installation and host compatibility

**Prefer to let your agent install it?** Copy the prompt from the
[agent installation guide](install.md). The direct-copy route needs no Node/npm.
The commands below are optional manual alternatives, not steps every user must run.

## No key: ask first, then choose a mode

Use [jev-setup](../skills/jev-setup/SKILL.md) to check key presence without printing
values. Prefer an existing OpenRouter account; otherwise offer official TypeSafe.
If no route is configured, explain the choices and **wait**:

- **A — Real Jev:** [OpenRouter key](https://openrouter.ai/settings/keys) if you
  use OpenRouter, otherwise [TypeSafe key](https://console.typesafe.ai).
- **B — Simulation:** the current agent or an explicitly approved available model
  such as DeepSeek uses the same evidence, questions and criteria. Install the
  skill folders; no Jev CLI or Jev key is needed. See the
  [copyable simulation prompt](../skills/jev-setup/references/simulation.md).

B outputs are marked `mode: agent_simulation` (host) or `mode: model_simulation` (another approved model), `jev_called: false` and carry no
Jev probabilities (`probability` and `confidence` are `null`). They are not API
results or calibration evidence. The host agent's usual costs/privacy terms still
apply. Never switch to B silently, including after API errors.

The runtime and credentials instructions below apply to **API mode**, not B.

## Pick the surface you need

- **One focused skill:** install the shared CLI, then a scenario skill. The nine scenario
  skills need no sibling skill and do not duplicate the runtime.
- **General toolbox:** install `jev`. It includes its own stdlib script and the
  full reference library; a separate CLI installation is optional.
- **Manual use:** install only the CLI and edit request JSON yourself.
- **MCP/browser/desktop integrations:** choose a separately maintained upstream
  project from the [ecosystem guide](../skills/jev/references/ecosystem.md).
  Installing our skills does not install those projects or their tools.

## Optional package-tool and skills-installer route

```bash
uv tool install git+https://github.com/wuyoscar/jev-skill.git@v0.2.0
npx skills add wuyoscar/jev-skill --skill jev-triage
export OPENROUTER_API_KEY="your-key"
```

Select Codex, Claude Code or OpenCode in the installer; replace the skill name
with any entry below. The CLI is pinned to the release; the short skills command
tracks the repository's default branch. For a fully pinned skill installation,
clone the tag and use the local installer commands below.

[Release downloads](https://github.com/wuyoscar/jev-skill/releases/tag/v0.2.0)
include the CLI wheel, source distribution and complete source ZIP. No PyPI
account is needed. Use the key for your selected provider.

## From a reviewed checkout

```bash
git clone --branch v0.2.0 https://github.com/wuyoscar/jev-skill.git
cd jev-skill
```

In the root of that checkout:

```bash
uv tool install .
npx skills add . --list
npx skills add . --skill jev-triage
```

Python 3.10+ is required. This route also needs uv and Node/npm for the installer;
`pipx install .` is an alternative to `uv tool install .`. Select Codex, Claude Code
or OpenCode in the skills installer. Install only the entries you need:

| Skill | Use it for | Jev API runtime |
|---|---|---|
| `jev` | General custom decisions and the full reference library | Bundled Python script; CLI optional |
| `jev-triage` | Message/record classification and prioritization | Shared `jev-decide` CLI |
| `jev-documents` | Source-span selection and evidence checks | Shared CLI |
| `jev-ui` | Browser/desktop action selection | Shared CLI + host UI tools for actions |
| `jev-route` | Tool, specialist or model recommendations | Shared CLI |
| `jev-context` | Relevance and compaction advice | Shared CLI |
| `jev-code-review` | Diff risks and review priorities | Shared CLI |
| `jev-find-code` | Choose locations to inspect | Shared CLI + host code-reading tools |
| `jev-simulation` | Legal actions in a simulated world | Shared CLI + your simulator for transitions |
| `jev-redteam` | Authorized batch, multi-turn and team safety evaluations | Shared CLI for judgments; offline Python request builder |
| `jev-setup` | Choose a real provider or explicit simulation | No runtime required to guide setup |

To install from a different project directory, replace `.` in the installer
command with the absolute path to this checkout. Review downloaded instructions
and code before use. No helper needs to change the host's primary model.

## Manual skill installation

Copy the **whole** chosen `skills/<name>` folder, including its assets and any
scripts/references. Do not overwrite an existing skill without review.
Project-local destinations:

| Host | Destination |
|---|---|
| Codex | `.agents/skills/<name>/` |
| Claude Code | `.claude/skills/<name>/` |
| OpenCode | `.opencode/skills/<name>/` (also supports shared `.agents/skills/`) |

See the [Codex docs](https://developers.openai.com/codex/skills/),
[Claude Code docs](https://code.claude.com/docs/en/skills),
[OpenCode docs](https://opencode.ai/docs/skills/) and
[installer documentation](https://github.com/vercel-labs/skills).
Discovery through the installer does not prove native invocation in every host.
Restart/reload as needed and explicitly ask the agent to use the selected skill.
The reference format follows the [Agent Skills specification](https://agentskills.io/specification).

## Credentials and first run

For **A / Jev API mode** only; B skips these calls and uses the selected existing model interface.

Export `OPENROUTER_API_KEY` or `TYPESAFE_API_KEY` for the selected provider in the
environment that **launches the host**. Desktop
apps may not inherit a terminal export. Use the host's documented environment
setup; never put keys in `SKILL.md`, chat, request JSON or version control.

```bash
export OPENROUTER_API_KEY="your-key"
# From the checkout; validation needs no key or network:
jev-decide decide skills/jev-triage/assets/example.json --dry-run
# After editing the synthetic example and reviewing the data to be sent:
jev-decide decide /path/to/edited-request.json
```

### Official native key (no OpenRouter account required)

Obtain a key at the [TypeSafe console](https://console.typesafe.ai) and set it
locally in the host's launch environment. The placeholder below is not a valid
credential. Keep real values out of chat, version control and shell history.

```bash
export TYPESAFE_API_KEY="<your-TypeSafe-key>"
jev-decide setup
jev-decide decide skills/jev-triage/assets/example.json --provider typesafe --dry-run
# Only after approving the data and paid call:
jev-decide decide /path/to/edited-request.json --provider typesafe > result.json
```

The CLI still defaults to OpenRouter, even when only the native key is present;
select `--provider typesafe` explicitly. Neither key works at the other endpoint.
There is no automatic `.env` loading. Configure the actual host process and
restart it when needed; `setup` checks presence, not authentication or credits.
[Setup skill](../skills/jev-setup/SKILL.md#local-key-setup) ·
[Common pitfalls](../skills/jev/references/pitfalls.md#native-key).

The general `jev` skill also works without installing the CLI:

```bash
python3 /actual/skill/path/scripts/jev.py decide request.json --dry-run
python3 /actual/skill/path/scripts/jev.py decide request.json
```

Resolve installed paths relative to the loaded skill, not the host project.
Normal decisions send supplied state/questions to the selected provider and incur usage;
dry runs do neither. Logs may contain supplied text: keep private data out of
public benchmark artifacts. Use `--provider openrouter` (default) or
`--provider typesafe` explicitly; the CLI never switches providers after an error.
The official route uses `https://api.typesafe.ai/v1/systemone` and `TYPESAFE_API_KEY`.
`jev-decide setup` only reports presence and choices; it does not test credentials.

Default OpenRouter model: `typesafe/jev-1.13`; official: `jev-1.13.0`.
Explicit TypeSafe selection maps the bundled OpenRouter ID to the official ID.
The OpenRouter API is alpha; test upgrades deliberately.
`--model` overrides request `model`, then `JEV_MODEL`, then the default.

## CLI behavior

The **skill**, not the CLI, handles the A/B conversation. The CLI has no simulation
flag: without a key, a live request returns an error instead of invented decisions.
`--dry-run` still works without a key and validates input only.

CLI installation adds the command, not a host skill. `decide FILE` accepts native
request JSON; use `-` for stdin. `classify` accepts `--text` or `--text-file` and a
JSON `--criteria` file mapping labels to descriptions. Use files/stdin instead
of interpolating untrusted text into shell commands. `jev-decide --help` lists options.

Thresholds default to `--min-probability 0.8` and `--min-margin 0.15`: uncalibrated
starting points, not deployment recommendations. Reserved labels `other`, `unknown`,
`abstain`, `review`, `ask_user`, `wait`, `none`, `defer` and `insufficient_evidence`
produce review status; add task-specific fallback labels with `--review-label`.
Scores are returned, not converted into approvals. HTTP failures are not retried
automatically. Exit codes: **0** selected/scored, **2** review, **1** error.
None grants permission to execute an action.

## Validate or build locally

```bash
python3 -m unittest discover -s tests -v
uv build
```

The wheel installs the shared CLI. The source distribution includes all eleven
skill folders, docs and evaluation materials. A skill folder copied on its own
needs its documented runtime **for API calls**: bundled Python for `jev`, shared
CLI for the focused skills. Agent simulation needs neither. [Validation scope](validation.md).
