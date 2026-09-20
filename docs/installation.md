# Installation and host compatibility

## Skill installation

From a project where you want the skill available:

```bash
npx skills add wuyoscar/jev-skill --skill jev
```

The installer asks which agents to target. It installs a filesystem skill, not an
MCP server or a new primary model. Review the downloaded instructions and code
before use. For a reviewed release, manually clone its tag instead of tracking main.

```bash
git clone --branch v0.1.0 https://github.com/wuyoscar/jev-skill.git
```

Copy the **whole** `skills/jev` folder, including scripts, assets, and references,
to the destination for your host. Do not overwrite an existing skill without
reviewing it. Project-local locations:

| Host | Destination |
|---|---|
| Codex | `.agents/skills/jev/` |
| Claude Code | `.claude/skills/jev/` |
| OpenCode | `.opencode/skills/jev/` |

See the current [Codex skill docs](https://developers.openai.com/codex/skills/),
[Claude Code skill docs](https://code.claude.com/docs/en/skills),
[OpenCode skill docs](https://opencode.ai/docs/skills/), and
[installer documentation](https://github.com/vercel-labs/skills).

Skill discovery does not prove that a host invokes it appropriately. Restart or
reload the host as needed and explicitly ask it to use Jev for a synthetic example.
The reference format follows the [Agent Skills specification](https://agentskills.io/specification).

## Credentials and execution

Export `OPENROUTER_API_KEY` in the environment that **launches the host**. Desktop
apps may not inherit a terminal export. Follow your host's documented environment
setup; do not put keys in `SKILL.md`, chat, a request JSON, or version control.

The default model is `typesafe/jev-1.13`. The API is alpha, so upgrades should be
tested, not silently applied. `--model` overrides the request's `model`, which
overrides `JEV_MODEL`, which overrides the default. No TypeSafe-specific key is needed.

The installed skill works without installing the CLI:

```bash
python3 /actual/skill/path/scripts/jev.py decide request.json --dry-run
python3 /actual/skill/path/scripts/jev.py decide request.json
```

Resolve paths relative to the loaded skill, not the host's current project.
Normal decisions send the supplied state/questions to OpenRouter and incur usage.
Dry runs do neither. Logs and traces may contain the supplied text; keep real data
out of public benchmark artifacts.

## Standalone CLI

```bash
uv tool install git+https://github.com/wuyoscar/jev-skill.git@v0.1.0
# Or use pipx install with the same git+ URL.
jev-decide --help
```

CLI installation installs the command, not the host skill. Install each surface
you want. Local development: `python3 -m pip install .` then
`python3 -m unittest discover -s tests -v`.

`decide FILE` accepts native request JSON. Use `-` for stdin. `classify` accepts
`--text` or `--text-file` and a JSON `--criteria` file mapping labels to descriptions.
Use stdin/files rather than shell interpolation for private or untrusted text.

Thresholds: `--min-probability 0.8`, `--min-margin 0.15`. These are uncalibrated
starting points. Reserved labels `other`, `unknown`, `abstain`, `review`, `ask_user`,
`wait`, `none`, `defer`, and `insufficient_evidence` always produce review status; add task-specific fallback labels with
`--review-label`. Scores are returned, not converted into approvals. HTTP failures
are not retried automatically. Exit codes: 0 valid selected/scored result, 2 review,
1 error. None of these grants execution permission.
