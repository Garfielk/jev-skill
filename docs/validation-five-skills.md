# Five-skill source preview

This is an unpublished source update, not a new release. Published v0.2.0 still
contains eleven entry points. The [migration guide](skill-migration.md) also
covers the previous six-entry checkout. No user installation was changed.

## What changed

- Five entry points: `jev`, `jev-triage`, `jev-documents`, `jev-eval`, `jev-act`.
  UI and world examples remain separate modes of `jev-act`.
- `jev` has an optional prompt-conversion guide and a small calling example,
  informed by [sumleo/prompt2jev](https://github.com/sumleo/prompt2jev). No second
  CLI, scheduler or model backend was added.
- All 108 scenarios have a primary skill and reverse navigation. Short entries
  lead to one local guide or template, not the entire README.
- Both READMEs retain 14 complete historical input/output pairs and use three
  main sections. The directory now has 57 rows: 45 existing entries plus 12 new
  entries, including one grouped official-demo entry.
- Six attributed previews share an 800 × 450 canvas. The browser GIF keeps all
  91 frames and their timing. Only the review dashboard is cropped; full originals
  and third-party license notices remain available in the media credits.

## Real Jev smoke checks

Three synthetic requests were sent once each through the existing OpenRouter
route, with no retries and no external actions. All returned protocol-valid
responses resolving to `typesafe/jev-1.13-20260917`.

| Input | Questions | Observed result | Wall time |
|---|---:|---|---:|
| Converted support prompt | 3 | Billing, refund requested, impact 0 | 0.609 s |
| Two-record batch | 6 | Billing / bug; one account-review question remained uncertain | 0.385 s |
| Observed UI choices | 1 | `open_policy`; no click executed | 0.338 s |

Total provider-reported cost: **$0.000097986**. This is ten questions in three
requests, not a load test or a speed/accuracy claim. The uncertain batch judgment
remains `needs_review`; it was not retried or counted as a confident decision.
[Full requests, raw responses and decisions](../evals/results/five-skills-2026-09-22.json).

## Offline and visual checks

The accepted test surfaces are README navigation/rendering, copied skill folders,
and the existing CLI request interface. Targeted checks cover five-name discovery,
relocated examples, all 108 primary/reverse links, bilingual content, six preview
canvas sizes, source-list deduplication, conversion dry runs and false/uncertain
refund handling. Historical request/output equality checks remain in place.

All **136 offline tests passed**, including copied installations in the three
documented host layouts. All five skill metadata checks and Python compilation
passed; the project has no configured static type checker. The final link pass
resolved 1,755 local link occurrences in active skills, READMEs and installation
guides. The official TypeSafe example's native model ID is checked offline at
the transport boundary; it was not live-run against the official endpoint.

Both READMEs were rendered with GitHub's Markdown API and inspected in a local
browser with GitHub Markdown CSS at 1280 px and 390 px. All six images loaded with
the same 16:9 ratio and pairwise dimensions. This checks sanitized GitHub markup,
not every client theme or native skill invocation.

The source archive and wheel built successfully. The archive contains exactly
five skill entries, the preview GIF and the calling example; local agent config,
specs and tickets are excluded. A fresh offline wheel installation passed the
public CLI and official-provider example dry runs. The copied safety guide's
preparation command and all three emitted requests also passed offline checks.

Migration rehearsals covered both eleven-to-five and six-to-five updates in
temporary folders: backups stayed unchanged, rollback was byte-identical, and
local edits and symlinks were detected. No real skill installation was touched.

Representative reading paths below start with that skill's `SKILL.md`, then only
the named guide and request. Counts are whitespace-separated words, including
frontmatter and JSON, not model tokens or latency estimates. These requests all
pass the existing offline CLI; no README or sibling skill needs to be loaded.

| Skill | Guide after the entry | Request in `assets/` | Total words |
|---|---|---|---:|
| `jev` | `references/prompt-to-jev.md` | `prompt-to-jev.json` | 1,426 |
| `jev-triage` | Workflow in the entry | `example.json` | 945 |
| `jev-documents` | `references/find-code.md` | `find-code.json` | 1,115 |
| `jev-eval` | `references/code-review.md` | `code-review.json` | 1,029 |
| `jev-act` | `references/ui.md` | `example.json` | 856 |

## Independent review

Two read-only reviews used main commit `36b08bb` as the fixed baseline.

### Standards

Two P2 findings were fixed: the official-provider example's model ID and an
ambiguous installed-folder path in the safety guide. Regression and copied-folder
checks passed. The reviewer confirmed both closed; no remaining findings.

### Spec

Two P2 findings were fixed: task-specific reverse template links and worked
conversion outputs for missing evidence and dependent steps. Offline request and
navigation checks passed. The reviewer confirmed both closed; no remaining
findings. These fixtures do not claim autonomous conversion quality.

## Limits

- Project intake checked original READMEs/model cards, revision identifiers and
  file metadata; it did not execute community projects. [Source checks](../skills/jev/references/intake-2026-09-22.md).
- The six conversion cases are authored guide checks, not a benchmark of an
  autonomous agent following instructions. Only the example request was live-run.
- Folder layout, links and dry runs do not establish native slash-command routing
  in Codex, Claude Code or OpenCode. No paid baseline comparison was performed.
- No protocol, permission policy, runtime default or published version changed.
