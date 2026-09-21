# Review and release readiness

This is the historical six-entry check. See [five-skill validation](validation-five-skills.md) for the current source update.

This source is not a published release. Oscar delegated PR merging after review
and passing checks; the agent handles integration and tracker cleanup. No tags
or releases are created by that merge operation.
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

## Observed results

- **123 tests passed** after review fixes; no paid calls are made by the suite.
- **mypy passed** for the changed runtime and current pilot with
  `--follow-imports=silent --ignore-missing-imports --check-untyped-defs`.
  This checks untyped bodies; it is not a fully annotated strict-type proof.
- All six skill metadata validators passed; **1,488 local link occurrences**
  checked without missing targets/anchors in the active collection and new docs.
- Three copied host layouts validated resources, ten dry-run examples each and
  the relocated transcript builder. Existing 108-scenario/45-project/14-IO
  preservation tests passed. Ten real CLI/API examples also succeeded.
- Temporary migration from eleven to six entries passed backup/rollback checks;
  customized edits and symlinks stopped replacement without changing their targets.
- Both READMEs were GitHub-Markdown-rendered and inspected in-browser: Chinese
  light and English dark usage prompts, actual IO table and six-skill navigation.
- Wheel and source archive built, six skills enumerated in the source archive;
  a fresh temporary environment installed the wheel offline and ran the CLI dry
  run. Complete tracked-source ZIP and SHA256 checksums were rehearsed locally.
  These local v0.2.0-metadata artifacts are **unpublished**, not the public release.
- Final-code recomputation of stored pilot receipts preserved labels, gate,
  denominators and coverage. Cost aggregation differs only at floating-point
  roundoff (checked at relative 1e-12 / absolute 1e-15 tolerance).
- No configured API key value appears in tracked files. The original checkout's
  five uncommitted diagnostic/runner files were left unchanged.

## Standards review

Independent review against pinned main `892dba8`: **0 actionable findings**.
The reviewer found no documented-standard violation or justified Fowler-smell
finding; task-specific artifacts and preserved failed generation are intentional.

## Spec review

Independent review initially found two **P2 numeric-field bugs**: exponent
`1e999` caused receipt serialization failure, and oversized integer costs could
crash report construction. Both were reproduced before fixes. Parsing now rejects
exponent overflow; cost accounting retains unknown values without overflowing its
subtotal. The reviewer independently rechecked both fixes and all eleven pilot
tests: **0 remaining Spec findings**.

Review baseline: `git diff 892dba8...HEAD`, covering the six-entry consolidation
and this follow-up. This is bounded review evidence, not a promise of no possible
bugs. [Actual API/pilot evidence](../evals/FOLLOWUP_VALIDATION.md).

## Publication checklist after merge

1. Select a new version (do not overwrite v0.2.0). Bump metadata and every install
   pin together at a reviewed commit; keep the legacy guide labeled and pinned.
2. Build wheel, source archive and complete source ZIP at that commit. Inspect
   six SKILL entries, references/assets and the CLI; run clean installation checks.
3. Generate and verify SHA256 checksums of those exact artifacts. Create the tag
   only after checks and publish the matching artifacts with migration notes.
4. Verify download URLs and rerun the copy-to-agent installation guide from the
   published artifacts. Remove source-preview notices only when those assets exist.

No direct TypeSafe live test was performed without its key. API success is not
native host slash-command validation, nor browser/game execution or calibration.
