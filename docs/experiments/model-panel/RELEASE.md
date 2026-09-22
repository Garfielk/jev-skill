# v0.2.1 candidate — not released

This branch prepares package metadata **0.2.1**. The actual latest release remains **v0.2.0** (eleven-entry legacy package). The source preview has **five** entries. Existing installation/update guides must not claim that v0.2.1 assets exist yet.

Scope: five-model dataset pilots, paired Agent results, offline reproduction, source/license records, and measured-example links in all five skills. No new skill, runtime provider, or automatic action permission.

After the user merges PR #8:

1. Pin the reviewed merged commit. Synchronize stable install/update pins with the five-entry migration before publication; do not point users to unavailable assets.
2. Rebuild wheel, sdist and full source ZIP at that commit; verify all five skill directories, references, fixtures and experiment records, then calculate SHA256 checksums.
3. Publish a new v0.2.1 tag/release only with the authorized merged commit; never overwrite v0.2.0.
4. Verify published downloads and repeat clean CLI/skill installation. Update source-preview language only when release assets are available.

Current local builds/tests are candidate verification, not evidence of a published release or native slash-command execution.
