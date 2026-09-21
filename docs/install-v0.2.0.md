# Install the published v0.2.0 collection (11 skills)

This is the legacy release guide, not the reviewed-source six-skill preview.
For the new structure, return to [the current guide](install.md).

## For people

Copy this into Codex, Claude Code or OpenCode:

```text
Install Jev Skills for this coding agent, including all scenario skills:
https://raw.githubusercontent.com/wuyoscar/jev-skill/v0.2.0/docs/install.md
Check my environment and handle the installation. Use jev-setup to confirm with me:
A: real Jev via my OpenRouter or official TypeSafe account; B: simulation with this agent.
Wait for my choice. Guide any key entry through local secret settings, never this chat.
Verify offline first; ask before sending data or making a paid call.
```

中文：

```text
帮我给当前 coding Agent 安装 Jev Skills，包括全部场景技能：
https://raw.githubusercontent.com/wuyoscar/jev-skill/v0.2.0/docs/install.md
你来检查环境并完成安装，用 jev-setup 跟我确认：
A：用我的 OpenRouter 或官方 TypeSafe 账号调用真实 Jev；B：由你模拟。
等我选择；需要 key 时指导我在本地安全配置，不要让我发到聊天里。
先完成离线验证，发送数据或付费调用前再征得我同意。
```

Use your own coding agent for this conversation; this repository does not supply
a hosted agent or chat service. You do not need to run terminal commands yourself.
The agent needs file access
and permission to run installation commands. It may need your help with a missing
runtime or a permission prompt. If there is no key, it must first ask you to
choose **A: get a key** or **B: simulate with your current agent or another explicitly approved available model**.
Never paste a key into chat.

## For the installing agent

### Outcome and defaults

Install all eleven skill folders from **v0.2.0** for the current host. Install the
runtime for Jev API mode; it is not needed for agent simulation. Verify the copied
files and run applicable offline checks. Default to **project-local** installation in the
current project. Say which host and destination you selected before writing.
If the host/project cannot be determined, ask one short question rather than
installing into every detected client or a random working directory. Honor an
explicitly requested subset or installation scope.

This is an installation task, not permission to change the agent's main model,
MCP servers, hooks, security settings or unrelated skills. Do not install any
linked community project. No Vercel account, gateway or Node/npm is needed for
the direct-copy route below. Existing host approval requirements still apply.

### 1. Check the environment and confirm with the user

You are the installer. Inspect the current host, carry out the technical steps,
and explain the next choice in plain language. Do not hand the user a terminal
checklist as the default workflow. Ask them only for information you cannot
inspect, route/scope choices, private credential entry and required approvals.
Key entry belongs in the host's local secret settings, not this conversation.

- Identify the current host from the session, not merely from installed binaries.
- Locate the actual project root and read any applicable local instructions.
- Follow the included `jev-setup` route selection. Check only presence of
  `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY`, never values. Prefer the user's
  existing OpenRouter account; otherwise offer official TypeSafe. Explain and
  obtain a choice before changing providers or sending data.
- If neither route is configured, warn and ask, then **wait**:
  **A:** configure a real Jev key (OpenRouter if the user uses it, otherwise
  TypeSafe); **B:** simulate with the current agent or a specifically approved
  available model such as DeepSeek. B outputs say `jev_called: false`, identify
  `agent_simulation` or `model_simulation`, and keep probability/confidence null.
  Never silently simulate or install another model. Keys stay outside chat.
  A can finish offline installation before key setup; installation is not
  permission to make paid calls. B needs no Jev key or Jev Python CLI.
- Check for Git; if unavailable, download the release source archive with an
  available tool instead. **For API mode**, also check for Python **3.10+** and
  an existing `uv` or `pipx`. Explain missing prerequisites and obtain any required
  approval to install them. Do not use `sudo`, modify system Python or silently
  switch products. **B needs none of these Python/CLI dependencies**; do not
  require or install them just for agent simulation.
- Inspect existing `jev-decide` and destination skill folders. Leave identical
  installations alone. For different versions, local edits or symlinks, explain
  the conflict and get confirmation before replacing them; never merge blindly.

### 2. Download and inspect the pinned source

Use a fresh temporary directory. For example, in a POSIX shell:

```bash
work=$(mktemp -d)
git clone --depth 1 --branch v0.2.0 https://github.com/wuyoscar/jev-skill.git "$work/source"
git -C "$work/source" rev-parse HEAD
git -C "$work/source" describe --tags --exact-match HEAD
```

The exact tag must be `v0.2.0`; stop if it differs and record the resolved commit
in your installation report. Do not substitute `main` for the versioned source.
With an archive instead of Git, use the
[release source ZIP and checksums](https://github.com/wuyoscar/jev-skill/releases/tag/v0.2.0)
and verify its checksum before installation. Inspect `pyproject.toml`, the skill
entrypoints and `skills/jev/scripts/jev.py` before running downloaded code.
On Windows, use equivalent temporary-directory and file operations in the host's shell.

### 3. Install the shared CLI

**Skip this step for B.** Use the selected existing agent/model interface.
For API mode:

Use **one existing** package tool, not both:

```bash
uv tool install "$work/source"
# Alternative when pipx is the available tool:
# pipx install "$work/source"
```

Do not use `--force` to replace an existing command without resolving the conflict.
Check that `jev-decide --help` works in the environment the host uses. If the
installation directory is not on PATH, locate it using the package tool and verify
the executable by its absolute path. Report the PATH/restart step still needed;
do not silently edit shell startup files. A new terminal or restarted host may be
needed to inherit PATH changes.

For a user who explicitly wants **only `jev`**, skip CLI installation: that skill
bundles `scripts/jev.py` and runs with Python alone. Do not silently substitute
this smaller installation for the full collection requested above.

### 4. Copy the complete skill folders

Choose only the current host's project-local destination:

| Current host | Destination under the project root |
|---|---|
| Codex | `.agents/skills/` |
| Claude Code | `.claude/skills/` |
| OpenCode | `.opencode/skills/` |

Copy each whole folder from `<source>/skills/`, including its assets and any
scripts/references, preserving the folder name:

- `jev`
- `jev-triage`
- `jev-documents`
- `jev-ui`
- `jev-route`
- `jev-context`
- `jev-code-review`
- `jev-find-code`
- `jev-simulation`
- `jev-setup`
- `jev-redteam`

Preflight **all** destinations for conflicts before writing any folder. Use the
host's filesystem tools or `shutil.copytree` without overwrite/merge options.
Keep the download outside the target skills directory, and do not copy `.git`,
the entire repository or just the eleven `SKILL.md` files. In API mode the focused
skills need the shared CLI; the general skill includes its own script.

For explicitly requested user-wide installation, resolve the current host's
supported user skill directory from its documentation first. Do not infer a
user-level path by prepending `~` to the project-local table.

### 5. Verify from the installed copies, without a key or API call

In **both modes**, confirm every copied `SKILL.md` and its linked local
assets/references exist. Check that each installed skill includes the A/B consent
instructions and explicit simulation labels.

In **API mode**, run the following checks. In B, they are optional if the runtimes
already exist; otherwise report them as skipped, not passed. Do not install
dependencies solely to run CLI checks for B.

Resolve `<installed-jev>` to the copied general-skill directory:

```bash
python3 <installed-jev>/scripts/jev.py decide <installed-jev>/assets/checkpoint.json --dry-run
```

Then run the installed shared CLI on **each of the nine** copied scenario assets:

```bash
jev-decide decide <installed-scenario>/assets/example.json --dry-run
```

The ninth scenario is `jev-redteam`. `jev-setup` has no classification asset: verify its
entrypoint and `references/simulation.md`, then run `jev-decide setup` if the CLI
is installed. Its report must not expose a key or make a network request.

These commands must exit 0 and print the validated request. Use absolute paths
if needed; a source-checkout test is not a copied-installation test. Ask the host to
refresh skill discovery if it supports that; otherwise explain whether a restart
or new session is needed. Do not claim native invocation was tested merely because
files were copied.

### 6. Explain what is ready

Report host/destination, installed skills, selected mode, key present/missing,
checks passed/skipped and CLI version/location if installed. Separate **installed**,
**verified offline**, **agent simulation selected** and **ready for API calls**.
A key-presence check does not prove that the key works; that requires a successful
API response. Copied skill files alone do not prove native agent behavior.

For A with a key still missing, explain local environment setup for the host.
Do not collect it in chat, store it in the repository or copy other apps' secrets.
For B, use the selected existing agent/model interface and mark all outputs as simulated, with
`probability` and `confidence` set to `null`. Do not send requests to Jev, require
a key, fabricate receipts or use probability thresholds to authorize actions.
Do not silently switch modes if a key later appears or an API call fails.

Do not spend API credits just to install. Once the user requests a real example,
use a small synthetic input and the selected skill; preserve the receipt.

A first-use prompt to offer:

> Use jev-triage to classify these messages into billing, bugs, how-to and other.
> Show the labels and uncertain cases before changing anything.

## Manual installation and troubleshooting

[CLI options, provider setup, manual paths and compatibility](https://github.com/wuyoscar/jev-skill/blob/v0.2.0/docs/installation.md).
The optional `npx skills` route there is just another way to copy skills; it is
not a Vercel runtime dependency.

## Verify the selected provider without spending

Run `jev-decide setup` for a read-only presence report, then dry-run a prepared
example with `--provider openrouter` or `--provider typesafe`. TypeSafe uses
`https://api.typesafe.ai/v1/systemone` and `TYPESAFE_API_KEY`; OpenRouter uses its
Decisions endpoint and `OPENROUTER_API_KEY`. Neither route auto-falls back.
The known bundled OpenRouter model ID maps to `jev-1.13.0` for an explicit
TypeSafe selection. A dry run does not authenticate the key or verify credits.
For simulation, use `jev-setup/references/simulation.md` with the selected existing
model, not the Jev CLI. See `jev-redteam` for offline batch/session examples.
