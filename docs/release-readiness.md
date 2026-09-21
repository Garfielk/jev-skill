# Review and release readiness

This source branch is not a published release. PR #4 and the follow-up require
Oscar's review/merge first; no tags, releases or automatic merges are created.
The actual published v0.2.0 remains the eleven-entry version. Building artifacts
with the existing metadata is an isolated packaging rehearsal, not permission to
replace those public assets.

## Required checks

- Public CLI, copied skill resources, metadata validators and documentation links.
- Typecheck the changed runtime/pilot; exercise fake transport, malformed fields,
  partial receipts, bounded concurrency, safe errors and no implicit full batch.
- Build wheel/source archive; install the wheel offline into a fresh temporary
  environment. The wheel is the CLI; the source archive carries the six skills.
- Rehearse legacy migration and rollback in temporary directories; preserve
  customized folders/symlink targets and do not touch user installations.
- Review separately for documented standards and spec compliance against main.

Final observed results and remaining limits are recorded below after verification.

## Publication checklist after merge

1. Agree a new version (do not overwrite v0.2.0). Bump metadata and every install
   pin together at a reviewed commit; keep the legacy guide labeled and pinned.
2. Build wheel, source archive and complete source ZIP at that commit. Inspect
   six SKILL entries, references/assets and the CLI; run clean installation checks.
3. Generate and verify SHA256 checksums of those exact artifacts. Create the tag
   only after checks and publish the matching artifacts with migration notes.
4. Verify download URLs and rerun the copy-to-agent installation guide from the
   published artifacts. Remove source-preview notices only when those assets exist.

No direct TypeSafe live test was performed without its key. API success is not
native host slash-command validation, nor browser/game execution or calibration.
