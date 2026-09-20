# Installation and host compatibility

## Pick the surface you need

- **One focused skill:** install the shared CLI, then a scenario skill. The eight
  skills need no sibling skill and do not duplicate the runtime.
- **General toolbox:** install `jev`. It includes its own stdlib script and the
  full reference library; a separate CLI installation is optional.
- **Manual use:** install only the CLI and edit request JSON yourself.
- **MCP/browser/desktop integrations:** choose a separately maintained upstream
  project from the [ecosystem guide](../skills/jev/references/ecosystem.md).
  Installing our skills does not install those projects or their tools.

## From a reviewed checkout

The public release is pending. No published tag or package-index release is
required for these local commands. In the root of this checkout:

```bash
uv tool install .
npx skills add . --list
npx skills add . --skill jev-triage
```

Python 3.10+ is required. This route also needs uv and Node/npm for the installer;
`pipx install .` is an alternative to `uv tool install .`. Select Codex, Claude Code
or OpenCode in the skills installer. Install only the entries you need:

| Skill | Use it for | Runtime |
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

Export `OPENROUTER_API_KEY` in the environment that **launches the host**. Desktop
apps may not inherit a terminal export. Use the host's documented environment
setup; never put keys in `SKILL.md`, chat, request JSON or version control.

```bash
export OPENROUTER_API_KEY="your-key"
# From the checkout; validation needs no key or network:
jev-decide decide skills/jev-triage/assets/example.json --dry-run
# After editing the synthetic example and reviewing the data to be sent:
jev-decide decide /path/to/edited-request.json
```

The general `jev` skill also works without installing the CLI:

```bash
python3 /actual/skill/path/scripts/jev.py decide request.json --dry-run
python3 /actual/skill/path/scripts/jev.py decide request.json
```

Resolve installed paths relative to the loaded skill, not the host project.
Normal decisions send supplied state/questions to OpenRouter and incur usage;
dry runs do neither. Logs may contain supplied text: keep private data out of
public benchmark artifacts. No TypeSafe-specific key is needed by our CLI.

Default model: `typesafe/jev-1.13`. The API is alpha; test upgrades deliberately.
`--model` overrides request `model`, then `JEV_MODEL`, then the default.

## CLI behavior

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

The wheel installs the shared CLI. The source distribution includes all nine
skill folders, docs and evaluation materials. A skill folder copied on its own
still needs its documented runtime: bundled Python for `jev`, shared CLI for the
focused skills. [Validation scope](validation.md).
