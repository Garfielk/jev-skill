# Install Jev Skills with your agent

## For people

Copy this into your own Codex, Claude Code or OpenCode agent:

```text
Install Jev Skills for this coding agent:
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/install.md
Check the current release versus the six-entry source preview. Confirm which source
I want before installing; record its exact commit. Handle installation yourself.
Use jev for setup: A: real Jev via my OpenRouter or official TypeSafe account;
B: simulation with this agent. Wait for my choice and keep keys out of chat.
Verify offline first. Ask before replacing existing skills or making paid calls.
```

中文：

```text
帮我给当前 coding Agent 安装 Jev Skills：
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/install.md
先说明当前发布版和六入口源码预览的区别，跟我确认安装来源并记录准确 commit。
你来完成安装，用 jev 跟我确认：A：OpenRouter 或官方 TypeSafe 真实调用；B：由你模拟。
等我选择，key 只在本地安全配置，不要让我发到聊天里。
先离线验证；替换已有技能或付费调用前先确认。
```

## For the installing agent

### 1. Confirm host, source and mode

Identify the current host and project from this session; ask if they cannot be
established. Default to project-local installation, not every detected client.
Use the user's own coding agent; do not hand over a terminal checklist by default.

**The six-entry collection is not yet released.** The actual published tag
**v0.2.0 contains eleven skills**, not six. Offer the source choice explicitly:

- **Published release:** follow [the pinned v0.2.0 guide](install-v0.2.0.md).
  This keeps its eleven entry points. Do not apply the six-skill copy list below.
- **Six-entry preview:** only use a source checkout/commit that the user has
  explicitly selected and reviewed. Record its exact commit, check that it contains
  the six names below, and inspect its instructions and runtime before execution.
  Do not silently substitute `main`, a PR branch or a made-up release tag.

The remaining steps apply to that **reviewed six-entry checkout**. Call it
`<source>`. No Vercel account, gateway, MCP server or Node/npm is required for the
whole-folder copy route.

Use the general skill's [setup mode](../skills/jev/references/setup.md). Check only
presence of `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY`, never print their values.
Preserve an already selected route. Otherwise ask and wait:

- **A:** real Jev through the user's existing OpenRouter account, or native TypeSafe.
- **B:** explicitly selected host-agent or available-model simulation. No Jev key
  or Python CLI is required. Mark `agent_simulation` or `model_simulation`,
  `jev_called: false`, and null probability/confidence. Do not silently substitute
  a model or invent provider receipts.

Let the user enter credentials in local secret settings, not chat or tracked files.
Setup does not authorize account creation, provider changes, paid calls or changes
to the host's main model, hooks, permissions or unrelated plugins.

### 2. Preflight the entire installation

Inspect all six destination folders, retired names, symlinks and any existing
`jev-decide`. Leave identical installations alone. Follow the
[upgrade procedure](skill-migration.md) for an older collection. Explain conflicts
and get approval before moving or replacing locally edited files or symlinks.
Do not begin a partial replacement before every destination has been checked.

For API mode, check Python 3.10+ and an existing `uv` or `pipx`; explain missing
prerequisites rather than installing them silently. Simulation mode needs neither.
Do not use sudo or modify system Python or shell profiles.

### 3. Install the API runtime, if needed

Skip this step for simulation. For the collection's API workflows, use one existing
package tool to install from the same reviewed checkout:

```bash
uv tool install /absolute/path/to/reviewed/source
# Or, if pipx is the selected existing tool:
# pipx install /absolute/path/to/reviewed/source
```

Do not force an overwrite without resolving the conflict. Verify `jev-decide --help`
from the host environment; report PATH or restart requirements instead of editing
startup files. A preview build is not a newly published version, even if its package
metadata still reports v0.2.0. Always include the source commit in the report.

For an explicitly requested **general `jev` only** installation, its bundled
stdlib script is sufficient for API calls; a shared CLI install is optional.
Focused skills use the shared CLI, not an undeclared sibling skill runtime.

### 4. Copy the six complete folders

| Current host | Project-local destination |
|---|---|
| Codex | `.agents/skills/` |
| Claude Code | `.claude/skills/` |
| OpenCode | `.opencode/skills/` |

Copy complete folders from the reviewed source, not just entry-point Markdown:

| Skill | Includes |
|---|---|
| `jev` | Custom decisions, setup, routing, context checks and the reference library |
| `jev-triage` | Record classification and prioritization |
| `jev-documents` | Document evidence and code-location selection |
| `jev-eval` | Output/code review and authorized safety-evaluation protocols |
| `jev-ui` | Real browser/desktop action selection |
| `jev-simulation` | Authored-world, game and NPC action selection |

Use filesystem operations that refuse overwrite, such as `shutil.copytree` without
merge options, after preflight. Keep downloads and backups outside all discoverable
skill directories. Do not copy the entire repository or create retired-name aliases.
For a requested subset, copy each whole selected folder. For user-wide installation,
resolve the current host's supported directory instead of guessing from this table.

### 5. Verify installed copies, not only the source

In both modes, enumerate installed `SKILL.md` files and confirm exactly the six
names above for a complete installation (or the explicitly requested subset).
Check each entry point's local reference and asset links. Retired names may remain
only when migration was explicitly deferred; report that as incomplete migration.

In API mode, run offline checks from the copied locations with no keys or network:

```bash
python3 <installed-jev>/scripts/jev.py decide <installed-jev>/assets/checkpoint.json --dry-run
jev-decide setup
jev-decide decide <installed-scenario>/assets/example.json --dry-run
```

Run the final command for each of the five focused skills. Also validate the merged
mode examples: general `routing.json` and `context.json`, documents `find-code.json`,
and evaluation `code-review.json`. Run the copied evaluation request builder on its
synthetic transcripts into a new temporary output directory, then dry-run the
resulting requests. Its output must say no Jev or target was called.

For native TypeSafe validation, add `--provider typesafe --dry-run` to a prepared
example; this checks input mapping, not credentials or credits. Simulation-only
users need not install Python to run optional CLI checks; report them as skipped.

A dry run exits 0 and prints a validated request. Refresh host skill discovery or
explain the required restart. Copied files and layout tests do **not** prove native
slash-command invocation. If actual host invocation is tested, record it separately.

### 6. Report readiness and finish approved migration

Report source commit, host, destination, installed names, chosen mode, credential
presence (never values), CLI version/location and checks passed/skipped. Distinguish
installed, offline-verified and successfully authenticated. Follow the migration
procedure to retire approved obsolete folders, then enumerate discovery again.
Never report six entries while old aliases still show up.

No API spending is needed for installation. For subsequent work, let the user say:

> Use jev-triage to classify these messages. Show the inputs, labels and uncertain
> cases before changing anything.

[Manual options and troubleshooting](installation.md) · [Six-entry migration](skill-migration.md)
