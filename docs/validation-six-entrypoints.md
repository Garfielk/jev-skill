# Six-entry collection validation

Scope: the source preview implementing [spec #3](https://github.com/wuyoscar/jev-skill/issues/3).
No model API calls, release, or changes to the user's installed skills were made.

## Public surface

Exactly six discoverable names: `jev`, `jev-triage`, `jev-documents`, `jev-eval`,
`jev-ui`, `jev-simulation`. All eleven former workflow destinations are represented
in [the migration map](skill-migration.md). The general skill owns setup, routing
and context references; documents owns code-location selection; evaluation owns
code-review and safety-test modes. Retired names do not have discoverable aliases.

## Checks performed

- **103 tests passed**, from a 100-test main-branch baseline. Tests were first
  changed to expect the new surface and failed before the reorganization.
- All **six skill metadata validators passed**.
- Copied the complete collection into temporary Codex, Claude Code and OpenCode
  directory layouts. Enumerated six entries, resolved local reference links and
  executed **10 documented request examples per layout** through the copied
  runtime with `--dry-run`: five focused examples, a general checkpoint and four
  merged-mode examples. No credentials were passed to these subprocesses.
- Ran the relocated safety-evaluation request builder from each copied layout
  with synthetic transcripts. It reported no Jev or target calls. Existing tests
  also exercise its no-overwrite, record-ID, transcript-order and label-exclusion
  behavior, plus focused-skill copies with the shared runtime.
- The copied-resource check caught a source-checkout-relative calibration link
  that would break after installation. It now points to the repository report;
  the regression test passes from all three installed layouts.
- Checked **1,456 local Markdown/HTML link occurrences** in active skill resources,
  both READMEs and install/migration guides; no missing files or anchors.
- Rehearsed the documented upgrade in temporary directories using the main-branch
  eleven-skill files: backup outside discovery, six-folder replacement, unchanged
  backup and rollback to byte-identical originals. A second preflight detected a
  custom setup edit and a symlink, stopped before replacement, and preserved both
  the edit and the symlink target. This is a procedure rehearsal, not a newly
  implemented production migration tool or a migrated user installation.
- Seven relocated fixtures/helper files were compared byte-for-byte with main.
  Existing regression checks preserve **108 scenarios**, the **45-entry project
  table**, **14 real request/output pairs**, bilingual coverage and six attributed
  gallery previews. Raw evaluation receipts were not edited.
- Built a local source distribution and wheel. The source archive contains exactly
  the six skills. Installed the wheel offline into a fresh temporary environment
  and ran its public CLI on the checkpoint example with `--dry-run` successfully.
  Metadata remains v0.2.0 in this **unpublished preview**; this is not a replacement
  for the actual eleven-skill v0.2.0 release. Install guidance states the distinction.
- Rendered both READMEs with GitHub Markdown for browser inspection of the changed
  six-entry navigation. No new gallery media or visual redesign is included.

## What these tests do not establish

Layout/resource tests do not prove native slash-command invocation, automatic
model routing or actual agent-authored code quality in all three products. The
11-mode check verifies explicit navigation and examples, not classifier accuracy.
No new live Jev/DeepSeek comparison was run, and the earlier online failure's root
cause was not investigated in this PR. No permission or provider behavior changed.

## Reproduce locally

```bash
python3 -m unittest discover -s tests -v
uv build
```

Use temporary host directories and the steps in the install/migration guides for
manual rehearsal; never use an actual customized installation as a test fixture.
The next concerns are listed separately in [the follow-up plan](next-steps.md).
