# Project directory, complete roundup intake, and setup — September 21, 2026

## What changed

- A 45-entry directory in both READMEs: projects, apps, reports, alternative
  models and methodology references. Evidence labels distinguish inspected
  READMEs, author posts, reports and unverified directory leads.
- 108 visible scenario blocks (previously 90). The 39-item LINUX DO roundup,
  supplied 15-project article and supplied Datawhale 22-item article each have
  a row in the [76-entry intake ledger](../../skills/jev/references/intake-2026-09-21.md).
  Repeated uses are consolidated, not counted as new projects.
- New `jev-setup` and `jev-redteam` skills: 11 installable folders total.
  Setup prefers an existing OpenRouter account, offers official TypeSafe,
  and asks before current-agent or approved available-model simulation.
  DeepSeek is an example, not a bundled service or an automatic fallback.
- Direct TypeSafe support via explicit `--provider typesafe`, `TYPESAFE_API_KEY`,
  `/v1/systemone` and `jev-1.13.0`. OpenRouter remains the CLI default.
  `jev-decide setup` checks presence only. No cross-provider retry or silent
  simulation. The installation guide pins v0.2.0.
- Authorized batch, multi-turn and team evaluation protocols with three benign
  authored transcripts and an offline JSONL-to-request builder. These are not
  observed target outputs, an attack runner or claimed jailbreak successes.

## What the sources changed in our understanding

[pg-jev](https://github.com/realZachi/pg-jev) and jevql are different integrations;
[pi-warden](https://github.com/DevMortimer/pi-warden) monitors agent trajectories;
[jev-skill-gate](https://github.com/ShivamPansuriya/jev-skill-gate) changes available
skills, which requires attention to hidden capabilities and local configuration.
The [MCP jev-shield](https://github.com/caiovicentino/jev-shield) is distinct from
a same-named ad-blocker. None is installed by our collection.

The [PrimeLine report](https://primeline.cc/blog/typesafe-jev-pre-registered-test)
is more qualified than the supplied retelling: results depend on task, threshold
and label source. It is not a universal or independently double-blind calibration
victory. Alternative OpenJev implementations are not Jev weights or verified RLCD.

The LINUX DO original by **@QianCheng** was read and original links recovered.
Twelve selected X post texts were read; videos were not reproduced. The PQ-search
and Excalidraw originals could not be read and remain labeled roundup leads.
The two supplied articles have no original publication URLs. This expansion used
GitHub, official docs, X, Made with Jev and LINUX DO; it did not perform a new
Reddit-wide survey. No copyrighted article or new third-party media was copied.

## Verification

- 96 unit tests; all 11 skill entrypoints pass the skill validator.
- Fresh v0.2.0 wheel installation; 33 complete skill-folder copies across three
  temporary host-style paths, 60 provider-specific dry runs, three offline
  request-builder runs and nine generated-request validations.
- Both providers fail without their matching key, without inventing decisions.
  TypeSafe request routing/credentials and no-fallback behavior are mock-tested;
  the official endpoint was **not called live**.
- Source archive includes all 11 skills, JSONL fixtures and new agent YAML files.
- 1,187 local documentation link occurrences resolved at this checkpoint.
- Both READMEs rendered with GitHub's Markdown API and visually inspected;
  the directory was also checked in a narrow content column and a dark preview.
  These are local previews, not a claim of native-client testing.
- All 14 existing real input/output pairs and previous negative evaluation
  results remain unchanged. No new paid model or target calls were made.

The copied-install checks establish packaging, not native invocation inside
Codex, Claude Code or OpenCode, simulation accuracy, or a new Jev benchmark.
