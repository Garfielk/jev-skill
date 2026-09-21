# From eleven entry points to five

This is an entry-point reorganization, not removal of use cases. The five-entry
source preview is not included in the published v0.2.0 release.

| Old entry point | New entry point | Mode / resource |
|---|---|---|
| `jev` | `jev` | Custom decisions and checkpoints |
| `jev-setup` | `jev` | [Setup](../skills/jev/references/setup.md) |
| `jev-route` | `jev` | [Routing](../skills/jev/references/routing.md) |
| `jev-context` | `jev` | [Context](../skills/jev/references/context.md) |
| `jev-triage` | `jev-triage` | Bulk classification and prioritization |
| `jev-documents` | `jev-documents` | Document evidence |
| `jev-find-code` | `jev-documents` | [Code locations](../skills/jev-documents/references/find-code.md) |
| `jev-code-review` | `jev-eval` | [Code review](../skills/jev-eval/references/code-review.md) |
| `jev-redteam` | `jev-eval` | [Batch, multi-turn and team safety evaluation](../skills/jev-eval/references/workflows.md) |
| `jev-ui` | `jev-act` | Real browser and desktop actions |
| `jev-simulation` | `jev-act` | Authored worlds, games and NPCs |

For an existing six-entry source installation, the four unchanged names stay put;
`jev-ui` and `jev-simulation` move into the two modes of `jev-act`. The table
also covers the published eleven-entry v0.2.0 installation.

The same tasks can be expressed in natural language. For example, ask `jev` to
recommend a tool, `jev-documents` to find the relevant code, or `jev-eval` to judge
an authorized transcript. Setup is a mode, not another service. There are no
installed aliases for retired names: aliases would put the clutter back.

## Reviewed upgrade, performed by your agent

This is an agent-guided procedure, not a new automatic migration tool.

1. Confirm the exact reviewed five-entry source commit and current host/scope.
   Inventory both retained and retired destinations across that host's actual
   discovery directories. Stop on unresolved local edits, unrecognized folders or
   symlinks; do not follow a symlink and overwrite its target.
2. Compare existing files with their known installed source/version. If that
   provenance is unknown, treat them as potentially customized. Show the proposed
   replacements and moves, and get approval. An instruction to install is not
   permission to discard customizations.
3. Prepare and verify the new collection in a temporary directory. Keep a backup
   location **outside all of the host's discoverable skill directories**. A folder
   named `old-jev` inside a scanned directory can still expose a `SKILL.md`.
4. After approval, move the old collection into that backup without deleting it;
   copy all five complete new folders into their intended destinations without
   merging or overwriting. If verification fails, restore the backup rather than
   leaving a partially migrated collection. Preserve the backup for the user.
5. Verify the installed copies using the current install guide, including all
   moved mode examples and references. Enumerate entry points again: a complete
   migrated collection must expose exactly `jev`, `jev-triage`, `jev-documents`,
   `jev-eval`, `jev-act`. If other scopes still expose obsolete
   entries, report them and ask before changing those scopes.
6. Refresh host discovery or explain a restart/new-session requirement. Report
   what was actually tested; file layout alone does not prove native invocation.

Existing project prompts referring to retired names need review using the table.
Do not rewrite unrelated project instructions automatically. Historical evaluation
receipts keep their original file identifiers, model outputs and timing; the
mapping explains where to find the corresponding templates now.
