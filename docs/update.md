# Update Jev Skills with your agent

## Copy this to your coding agent

```text
Update my installed Jev Skills:
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/update.md
```

中文：

```text
帮我更新已安装的 Jev Skills：
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/update.md
```

Your agent checks what you installed, updates it and verifies it offline. Keep
using the same provider, keys and simulation choice. No new account is needed.
If you pinned a version, have local edits or want to switch to main, the agent
asks before changing that choice. **Updating the CLI alone does not update skills.**

## For the updating agent

### 1. Identify the installation and target

- Inspect the current coding agent's actual skill directories and installation
  records. Keep the existing host, project/global scope and selected skill subset;
  do not install into every detected client. No installation? Use [install](install.md).
- Record the installed source URL, tag/commit, skill names and CLI location/install
  method, if present. Never infer the commit from the package version alone.
  Inspect symlinks without following them for writes. Treat unknown provenance or
  local differences as user work, not disposable files.
- Preserve the update channel: an explicit version/commit pin stays pinned unless
  the user approves changing it; a release-tracking install checks the latest
  published release; an explicitly chosen main-tracking install checks main.
  If the channel is unknown, show the choices and ask once. Do not silently switch
  from a release to main or downgrade to a release because its version matches.
- Fetch from **https://github.com/wuyoscar/jev-skill** into a temporary directory
  outside skill discovery. Resolve the selected target to an exact commit, inspect
  the diff and relevant instructions, and check its CI/release evidence before
  executing anything from it. Do not pull/reset the user's working checkout.
  If validation is failing or evidence is unavailable, report that and stop before
  replacement; do not call the target verified.

**Current release boundary:** published **v0.2.0 has eleven entry points**; the
five-entry collection on main is a source preview, not a newer published release.
For a deliberate eleven-to-five update, use [the migration map](skill-migration.md).
For a pinned v0.2.0 install, “already at your selected version” is a valid outcome.
After future releases, use the actual target's catalog and instructions rather than
assuming a fixed number of skills. Do not reintroduce retired aliases.

### 2. Stage and protect the existing installation

- Compare the installed files against their known original source and the selected
  target. If commit and file contents already match, verify and report a no-op.
- Resolve local edits, unknown files, symlinks and overlapping installations before
  mutation. Show the conflicts and get approval; do not overwrite them, use a
  blanket force option or delete them. Preserve unrelated skills and user data.
- Stage complete target skill folders, including references, scripts and assets.
  Verify local links and examples there first. Preserve the installed subset;
  map retired names only with the approved migration. Do not copy just `SKILL.md`.
- Save a backup **outside all host skill-discovery directories** and record its
  path. Record the old CLI's exact source, installer and restoration command;
  ensure that source is available before replacing it. If recovery cannot be
  established, stop. Preserve provider choice, environment/secret settings and
  simulation mode. Never print keys or copy secrets into an update log.

### 3. Update skills and, when present, the CLI

Replace only the resolved, approved skill folders with their staged counterparts;
do not merge trees and leave obsolete files discoverable. Do not add a new CLI
installation for simulation-only users or for users running the bundled script.

If a separately installed CLI exists, update it from the **same reviewed source**
using its existing installer/environment. Check that installer's local help first.
For an existing `uv tool` installation, after resolving conflicts and recording
rollback, an explicit source reinstall handles even unchanged package versions:

```bash
uv tool install --reinstall /absolute/path/to/reviewed/source
```

For pipx, a venv or a skills installer, use that tool's documented update procedure
with the selected source; do not switch installers or install an unrelated PyPI
package. A skill-only installer does not update the CLI, and a CLI wheel does not
refresh skill folders. There is no `jev-decide update` command.

Record the before/after destination inventory. If replacement or verification
fails, move only the folders written by this update out of discovery, including
target-only names such as `jev-eval` that had no predecessor. Stop if they changed
since replacement; do not overwrite concurrent user work. Restore the backed-up
skill folders and previous CLI source using its recorded installer, then verify
the original discoverable names, file contents and CLI source.
Do not report success for a partial update; report any rollback failure explicitly.
Keep backups until the new installation has been verified.

### 4. Verify the installed result and report

Run the selected target's offline installation checks **against the installed
copies**, not just the checkout. For the five-entry collection, follow
[installation verification](install.md#5-verify-installed-copies-not-only-the-source):
check discoverable names/subset, local references, bundled examples with
`--dry-run`, and the installed CLI's help/setup when applicable. Use the chosen
provider explicitly on dry runs. In simulation mode, skip CLI-dependent checks
if no runtime is installed and report that limitation. No API calls are needed.

Check for stale aliases or duplicates in the selected host scope; ask before
changing another scope. Reload skill discovery as required by the host. File-copy
and dry-run checks are not proof of a native slash-command invocation or API auth.

Report the before/after tag or commit, actual installed paths and skill names,
CLI source/location (or not installed), notable changes, offline checks and backup
location. If already current, say so without rewriting files. Do not change keys,
providers, host model, hooks, permissions or unrelated plugins as part of an update.

Pattern inspired by [Agent Reach's agent-led update guide](https://github.com/Panniantong/agent-reach/blob/main/docs/update.md).
