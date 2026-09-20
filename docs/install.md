# Install Jev Skills with your agent

## For people

Copy this into Codex, Claude Code or OpenCode:

```text
Install Jev Skills for my current agent, including the general skill and all scenario skills. Read and follow this installation guide, then verify the installation:
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/install.md
```

中文：

```text
帮我给当前 Agent 安装 Jev Skills，包括通用技能和全部场景技能。请读取并按照这份安装指南操作，完成后验证安装是否成功：
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/install.md
```

You do not need to run terminal commands yourself. The agent needs file access
and permission to run installation commands. It may need your help with a missing
runtime, a permission prompt or your OpenRouter key. Never paste the key into chat.

## For the installing agent

### Outcome and defaults

Install the released **v0.1.1** runtime and all nine skill folders for the current
host, then run offline checks. Default to **project-local** installation in the
current project. Say which host and destination you selected before writing.
If the host/project cannot be determined, ask one short question rather than
installing into every detected client or a random working directory. Honor an
explicitly requested subset or installation scope.

This is an installation task, not permission to change the agent's main model,
MCP servers, hooks, security settings or unrelated skills. Do not install any
linked community project. No Vercel account, gateway or Node/npm is needed for
the direct-copy route below. Existing host approval requirements still apply.

### 1. Check the environment

- Identify the current host from the session, not merely from installed binaries.
- Locate the actual project root and read any applicable local instructions.
- Check for Python **3.10+**, Git and an existing `uv` or `pipx` command.
  If Git is unavailable, download the release source archive with an available
  tool instead. If Python or both package tools are missing, explain the missing
  prerequisite and obtain any required approval to install it. Do not use `sudo`,
  modify system Python or silently switch to another product.
- Check `OPENROUTER_API_KEY` **presence only**, without printing its value. A missing
  key does not block installation or offline validation.
- Inspect existing `jev-decide` and destination skill folders. Leave identical
  installations alone. For different versions, local edits or symlinks, explain
  the conflict and get confirmation before replacing them; never merge blindly.

### 2. Download and inspect the pinned source

Use a fresh temporary directory. For example, in a POSIX shell:

```bash
work=$(mktemp -d)
git clone --depth 1 --branch v0.1.1 https://github.com/wuyoscar/jev-skill.git "$work/source"
git -C "$work/source" rev-parse HEAD
git -C "$work/source" describe --tags --exact-match HEAD
```

The exact tag must be `v0.1.1`; stop if it differs and record the resolved commit
in your installation report. Do not substitute `main` for the versioned source.
With an archive instead of Git, use the
[release source ZIP and checksums](https://github.com/wuyoscar/jev-skill/releases/tag/v0.1.1)
and verify its checksum before installation. Inspect `pyproject.toml`, the skill
entrypoints and `skills/jev/scripts/jev.py` before running downloaded code.
On Windows, use equivalent temporary-directory and file operations in the host's shell.

### 3. Install the shared CLI

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

Preflight **all** destinations for conflicts before writing any folder. Use the
host's filesystem tools or `shutil.copytree` without overwrite/merge options.
Keep the download outside the target skills directory, and do not copy `.git`,
the entire repository or just the nine `SKILL.md` files. The focused skills need
the shared CLI; the general skill includes its own script.

For explicitly requested user-wide installation, resolve the current host's
supported user skill directory from its documentation first. Do not infer a
user-level path by prepending `~` to the project-local table.

### 5. Verify from the installed copies, without a key or API call

Resolve `<installed-jev>` to the copied general-skill directory:

```bash
python3 <installed-jev>/scripts/jev.py decide <installed-jev>/assets/checkpoint.json --dry-run
```

Then run the installed shared CLI on **each of the eight** copied scenario assets:

```bash
jev-decide decide <installed-scenario>/assets/example.json --dry-run
```

These commands must exit 0 and print the validated request. Use absolute paths
if needed; a source-checkout test is not a copied-installation test. Confirm every
copied `SKILL.md` and its linked local assets/references exist. Ask the host to
refresh skill discovery if it supports that; otherwise explain whether a restart
or new session is needed. Do not claim native invocation was tested merely because
files were copied.

### 6. Explain what is ready

Report a short checklist: host and destination, installed skill names, CLI version
and executable location, offline checks passed, and key present/missing. Separate
**installed and verified offline** from **ready for paid API calls**. A true claim
that the key works requires a real successful API response, not an environment check.

If the key is missing, show the user how to configure `OPENROUTER_API_KEY` in the
local environment that launches their host. Do not ask them to send it in chat,
store it in the repository or copy credentials from other apps. The agent can
finish installation while the user handles this one secret-setting step.

Do not spend API credits just to install. Once the user requests a real example,
use a small synthetic input and the selected skill; preserve the receipt.

A first-use prompt to offer:

> Use jev-triage to classify these messages into billing, bugs, how-to and other.
> Show the labels and uncertain cases before changing anything.

## Manual installation and troubleshooting

[CLI options, provider setup, manual paths and compatibility](installation.md).
The optional `npx skills` route there is just another way to copy skills; it is
not a Vercel runtime dependency.
