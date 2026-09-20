# Awesome Jev Skills

**Practical things to do with Jev — examples you can edit, skills you can install,
and community projects you can build on.**

Jev chooses, classifies and scores; your agent supplies the context and does the
work. Use it inside an agent, or as a tool for your own messages, documents and decisions.

[中文](README.zh.md) · [Install](docs/installation.md) · [Community projects](skills/jev/references/ecosystem.md) · [Methods and sources](skills/jev/references/index.md)

## The full collection

**85 scenarios and integration uses**, covering the earlier 56 agent/human recipes,
22 implementation patterns, and concrete uses from X and project research.
Duplicate recipes are merged; one method can support several scenarios.
This covers the material read so far, not the limit of Jev's uses. Unseen sections
of truncated posts are not counted as reviewed scenarios.

Each section includes a task, inputs/outputs, customization, a skill/template and
sources. **Outputs from all 14 recorded live API examples appear inline below.**
Untested adaptations are labeled rather than presented as reproduced demos.

There are still **eight focused skills plus one general skill**, not 85 duplicate
packages. One skill can serve many custom tasks. JSON links are templates to edit,
not complete applications for every scenario; measured inputs are labeled separately.

- [Keep a long task on track](#agent) — 5 uses
- [Supervision, review and evaluation](#quality) — 9 uses
- [Routing, delegation and context](#routing) — 12 uses
- [Browser, desktop and interactive tools](#interaction) — 11 uses
- [Inbox, support and everyday workflows](#business) — 11 uses
- [Documents, research and evidence](#documents) — 12 uses
- [Data, search and developer workflows](#data) — 12 uses
- [Ideas, games and creative tools](#creative) — 10 uses
- [Build and connect your own tools](#building) — 3 uses

### Install
Python 3.10+, [uv](https://docs.astral.sh/uv/) and Node/npm are needed for this route.

```bash
uv tool install git+https://github.com/wuyoscar/jev-skill.git@v0.1.0
npx skills add wuyoscar/jev-skill --skill jev-triage
export OPENROUTER_API_KEY="your-key"
```

Choose Codex, Claude Code or OpenCode in the installer. Replace `jev-triage` with
the skill you want below, then copy a task prompt into your agent. For manual use,
download/edit an example and run `jev-decide decide request.json --dry-run` to
validate it for free; remove `--dry-run` to call Jev (paid). [Installation options](docs/installation.md).

### Reading the examples

- **Try** is a task to give your agent. You can also edit JSON and call `jev-decide` yourself.
- **Observed output** is an excerpt of the saved CLI `decisions`, omitting textual score-level
  descriptions without changing values. Choice `probability` refers to the selected label;
  Noul `probability` always means the proposition is true, even when `value` is false.
  A score is not a probability.
- Live API inputs were synthetic; no mailbox, desktop or trading account was operated.
  Upstream performance claims remain attributed to their authors. Untested adaptations have no invented outputs.

<a id="agent"></a>
## Keep a long task on track

[Goal-drift checkpoint](#sc-a01) · [Stuck-loop recovery](#sc-a02) · [Completion evidence check](#sc-a06) · [Detect unsupported success language](#sc-a07) · [Postmortem failure attribution](#sc-a27)

<a id="sc-a01"></a>
<!-- covers: A01 -->
### 1. Goal-drift checkpoint

> Use Jev: **Noul:** “Does this action directly advance acceptance check C3?” Criteria: concrete link to the check, not merely useful adjacent cleanup.

- **Input / question:** Goal, active acceptance check, recent observed result, proposed action → see the typed question above.
- **Use the result:** Low/uncertain support triggers a replan note; it does not erase work or redefine the user's goal. Test for false interruptions.
- **Customize:** Milestone triggers, acceptance criteria and permitted side work.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/checkpoint.json).
- **Sources / alternatives:** [R02](skills/jev/references/community.md#r02) · [P02](skills/jev/references/community.md#p02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a02"></a>
<!-- covers: A02 -->
### 2. Stuck-loop recovery

> Use Jev: **Choice:** `inspect_error` (unread evidence), `change_hypothesis` (same approach failed), `verify_fix` (new success evidence), `escalate_unknown`.

- **Input / question:** Last three attempts, commands, exit codes, error excerpts, changed inputs → see the typed question above.
- **Use the result:** The main agent selects a concrete recovery tool within the chosen route. Exact repeated commands can be counted without Jev; never endlessly retry because a score is high.
- **Customize:** Failure window, diagnostic tools and retry limits.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/checkpoint.json).
- **Sources / alternatives:** [R02](skills/jev/references/community.md#r02) · [P03](skills/jev/references/community.md#p03)
- **Evidence:** Synthetic API smoke output shown below; no end-to-end outcome benchmark for this workflow.

**Observed output** — CSV parser: the same UnicodeDecodeError twice, no source change between runs.

<!-- receipt: examples-2026-09-20.json#checkpoint -->
```json
{
  "next_step": {"status": "selected", "value": "inspect_input", "probability": 1, "margin": 1},
  "stuck": {"status": "selected", "value": true, "probability": 0.88}
}
```

[Original request and full response](evals/results/examples-2026-09-20.json)

<a id="sc-a06"></a>
<!-- covers: A06 H13 -->
### 3. Completion evidence check

> Use Jev: **Noul per criterion:** “Does the supplied evidence support criterion C2?” Require evidence for that criterion, not a generic success log.

- **Input / question:** Acceptance checklist plus actual artifact IDs, test receipts and their revision hashes → see the typed question above.
- **Use the result:** Run missing checks or report partial completion. Code checks freshness and exit status; Jev cannot certify a test ran or a file exists.
- **Customize:** Acceptance criteria, receipt freshness and mandatory checks.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/completion.json).
- **Sources / alternatives:** [P03](skills/jev/references/community.md#p03) · [N01](skills/jev/references/community.md#n01)
- **Evidence:** Synthetic API smoke output shown below; no end-to-end outcome benchmark for this workflow.

**Observed output** — The job was queued but not executed, the metrics file did not exist, yet the agent claimed completion.

<!-- receipt: examples-2026-09-20.json#completion -->
```json
{
  "claim_supported": {"status": "selected", "value": false, "probability": 0.02},
  "next_step": {"status": "selected", "value": "check_job", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/examples-2026-09-20.json)

<a id="sc-a07"></a>
<!-- covers: A07 -->
### 4. Detect unsupported success language

> Use Jev: **Noul:** “Does this message claim a successful outcome not established by the ledger?” Distinguish planned, attempted and observed.

- **Input / question:** Proposed final claim and a minimal, independently captured execution ledger → see the typed question above.
- **Use the result:** Revise the claim or collect evidence. Never convert the classifier's agreement into a success receipt. Preserve raw contradictory results.
- **Customize:** Distinguish planned, attempted and observed outcomes.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/completion.json).
- **Sources / alternatives:** [P03](skills/jev/references/community.md#p03)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a27"></a>
<!-- covers: A27 -->
### 5. Postmortem failure attribution

> Use Jev: Separate **Choice** questions: responsible agent ID; decisive step ID; error class (`missing_evidence`, `wrong_tool`, `stale_state`, `execution_error`, `unknown`).

- **Input / question:** Failed trace with numbered steps, observed errors and named agents → see the typed question above.
- **Use the result:** Create an investigation shortlist, not a blame verdict. A retrospective label must be tested before it becomes an online recovery policy.
- **Customize:** Failure taxonomy, evidence window and unknown route.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/checkpoint.json).
- **Sources / alternatives:** [P06](skills/jev/references/community.md#p06)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="quality"></a>
## Supervision, review and evaluation

[Plan versus action](#sc-a03) · [Test weakening / reward gaming](#sc-a08) · [Project-rule compliance](#sc-a09) · [Action-risk triage](#sc-a10) · [Suspicious tool-output instructions](#sc-a11) · [Prioritize code review](#sc-a12) · [Empty or unhelpful tool response](#sc-a13) · [Independent answer comparison](#sc-h14) · [Use Jev as a repeatable evaluation judge](#sc-judge)

<a id="sc-a03"></a>
<!-- covers: A03 -->
### 6. Plan versus action

> Use Jev: **Noul:** “Is this call consistent with the stated plan?” Compare target, scope and intended effect.

- **Input / question:** Agent's stated immediate plan and exact proposed call/arguments → see the typed question above.
- **Use the result:** Feed mismatch back for correction; hard permissions still govern execution. Agreement between two texts does not prove either is authorized.
- **Customize:** Fields to compare, scope and explicit exceptions.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [R02](skills/jev/references/community.md#r02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a08"></a>
<!-- covers: A08 -->
### 7. Test weakening / reward gaming

> Use Jev: **Noul:** “Does this edit weaken a required check without implementing the requirement?” Show before/after assertion behavior.

- **Input / question:** Changed assertions, original task, protected test intent → see the typed question above.
- **Use the result:** Route to review; deterministic checks separately catch removed/skipped tests. A test change can be legitimate; do not call it deliberate cheating from a score.
- **Customize:** Protected assertions and legitimate test-change exceptions.
- **Start:** [jev-code-review](skills/jev-code-review/SKILL.md) · [Template to adapt](skills/jev-code-review/assets/example.json).
- **Sources / alternatives:** [P03](skills/jev/references/community.md#p03)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): test weakening 0.97; not an end-to-end review benchmark.

**Observed output** — The assertion was replaced with assert True; only the weakened test was run.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-code-review/assets/example.json -->
```json
{
  "weakens_test": {"status": "selected", "value": true, "probability": 0.97},
  "completion": {"status": "selected", "value": "unsupported", "probability": 1, "margin": 1},
  "review_priority": {"status": "scored", "value": 1.97}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a09"></a>
<!-- covers: A09 -->
### 8. Project-rule compliance

> Use Jev: **Noul:** “Does this diff violate this rule?” Criteria quote the rule and its exceptions.

- **Input / question:** One applicable rule, relevant diff and necessary surrounding code → see the typed question above.
- **Use the result:** Attach a focused review note; run linters for syntactic rules. One question per rule; broad “is this good code?” questions produce unclear feedback.
- **Customize:** Rule text, applicable files and exclusions.
- **Start:** [jev-code-review](skills/jev-code-review/SKILL.md) · [Template to adapt](skills/jev-code-review/assets/example.json).
- **Sources / alternatives:** [P02](skills/jev/references/community.md#p02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a10"></a>
<!-- covers: A10 -->
### 9. Action-risk triage

> Use Jev: **Choice:** `read_only`, `reversible_local_change`, `external_effect`, `potentially_destructive`, `unknown`.

- **Input / question:** Proposed command/action, target environment, authorization evidence, rollback facts → see the typed question above.
- **Use the result:** Use the label to decide review priority. Permission, deny lists and confirmation requirements are deterministic and cannot be overruled by the prediction.
- **Customize:** Environment, blast radius and rollback requirements.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [R03](skills/jev/references/community.md#r03) · [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a11"></a>
<!-- covers: A11 -->
### 10. Suspicious tool-output instructions

> Use Jev: **Noul:** “Does this content try to redirect the agent's instructions or request secrets/actions outside the task?”

- **Input / question:** Untrusted page/log text and original task, explicitly delimited → see the typed question above.
- **Use the result:** Flag the source; continue treating all source text as untrusted regardless of score. This is defense in depth, not an injection-proof filter.
- **Customize:** Redirect categories and evidence windows; retain trust boundaries.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [P02](skills/jev/references/community.md#p02) · [N02](skills/jev/references/community.md#n02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a12"></a>
<!-- covers: A12 H12 -->
### 11. Prioritize code review

> Use Jev: **Score per hunk:** 0 = cosmetic; 1 = behavior touched; 2 = plausible defect requires inspection; 3 = plausible security/data-loss issue.

- **Input / question:** Diff hunks, file roles and related tests, not an entire repository dump → see the typed question above.
- **Use the result:** Prioritize expert inspection and tests. A high score is a lead, not proof; a low score must not bypass mandatory security review.
- **Customize:** Risk dimensions, rubric anchors and mandatory review scope.
- **Start:** [jev-code-review](skills/jev-code-review/SKILL.md) · [Template to adapt](skills/jev-code-review/assets/example.json).
- **Sources / alternatives:** [P07](skills/jev/references/community.md#p07) · [Jev Review](https://github.com/devagrawal09/jev-review) · [Blink review](https://blink.review/)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a13"></a>
<!-- covers: A13 -->
### 12. Empty or unhelpful tool response

> Use Jev: **Choice:** `usable_result`, `empty_or_error`, `missing_required_information`, `policy_refusal`.

- **Input / question:** User request, expected result shape, tool/agent reply and actual tool status → see the typed question above.
- **Use the result:** Retry legitimate errors or gather missing evidence. Preserve policy refusals and host safety constraints; do not route around them. Syntax/schema failures should be checked in code first.
- **Customize:** Required fields, error categories and legitimate retry conditions.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/completion.json).
- **Sources / alternatives:** [R04](skills/jev/references/community.md#r04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h14"></a>
<!-- covers: H14 -->
### 13. Independent answer comparison

> Use Jev: **Score per answer:** 0 = unsupported; 1 = partly supported/incomplete; 2 = supported and meets the stated requirement.

- **Input / question:** Same question, relevant source evidence and anonymized candidate answers → see the typed question above.
- **Use the result:** Compare disagreement and review samples manually. Counterbalance answer order; do not let models grade their own output as sole ground truth.
- **Customize:** Rubric dimensions, counterbalanced order and human audits.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04) · [P09](skills/jev/references/community.md#p09) · [N01](skills/jev/references/community.md#n01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-judge"></a>
<!-- covers: E04 U14 U17 U27 -->
### 14. Use Jev as a repeatable evaluation judge

> Use Jev: Apply a fixed rubric to saved agent traces, repeat the same judgments and compare agreement with human labels, latency and cost.

- **Input / question:** Trace/answer + fixed criteria → typed labels/scores → evaluation statistics. → see the typed question above.
- **Customize:** Judge rubric, held-out labels, repeat count and false-positive/negative costs.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [LangChain judge study](skills/jev/references/community.md#n01) · [OpenRouter author post](https://x.com/OpenRouter/status/2101412965765529853)
- **Evidence:** LangChain study documented; exact Ori experiment assets not located in the research pass. No new judge benchmark run here.

<a id="routing"></a>
## Routing, delegation and context

[User absent, safe work remains](#sc-a04) · [Decide whether to escalate](#sc-a05) · [Subagent report admission](#sc-a14) · [Tool routing](#sc-a15) · [Model tier routing](#sc-a16) · [Specialist delegation](#sc-a17) · [Skill/tool discovery](#sc-a18) · [Rerank search and retrieval results](#sc-a19) · [Repository navigation](#sc-a20) · [Recoverable output reduction](#sc-a21) · [Duplicate observation suppression](#sc-a22) · [Choose a safe moment to compact](#sc-compaction)

<a id="sc-a04"></a>
<!-- covers: A04 -->
### 15. User absent, safe work remains

> Use Jev: **Choice:** `inspect_logs`, `run_local_checks`, `draft_patch`, `checkpoint_and_wait`; offer only currently available, pre-authorized actions.

- **Input / question:** Pre-approved work queue, dependency status, evidence, host-computed permission flags → see the typed question above.
- **Use the result:** Execute a selected safe step or save a checkpoint. If only a consequential decision remains, wait; do not invent preferences or approval.
- **Customize:** Preauthorized queue, reversibility and stop conditions.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/checkpoint.json).
- **Sources / alternatives:** [P01](skills/jev/references/community.md#p01) · [P02](skills/jev/references/community.md#p02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a05"></a>
<!-- covers: A05 -->
### 16. Decide whether to escalate

> Use Jev: **Choice:** `gather_local_evidence` (an untried relevant read), `request_reasoning_review` (evidence exists), `needs_user_input` (preference/authority missing).

- **Input / question:** Bounded issue description, attempts, missing facts, available safe diagnostic actions → see the typed question above.
- **Use the result:** Use a stronger reasoner for analysis, not to bypass permissions. If the user is away, record the exact missing decision and avoid dependent actions.
- **Customize:** Error costs, missing-information types and validated escalation policy.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [R01](skills/jev/references/community.md#r01) · [P01](skills/jev/references/community.md#p01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a14"></a>
<!-- covers: A14 -->
### 17. Subagent report admission

> Use Jev: **Choice:** `action_required_now`, `useful_next_checkpoint`, `duplicate`, `needs_verification`.

- **Input / question:** Child objective, compact result, evidence IDs, parent's current decision → see the typed question above.
- **Use the result:** Wake the parent only for relevant urgent material; retain all reports for retrieval. Claims of urgency in the child text are not enough.
- **Customize:** Interruption cost, urgency criteria and duplicate rules.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [P02](skills/jev/references/community.md#p02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a15"></a>
<!-- covers: A15 -->
### 18. Tool routing

> Use Jev: **Choice:** `search_web`, `read_local_file`, `run_test`, `ask_user`, `none`; each ID maps to a real permitted capability.

- **Input / question:** Current subgoal, observation, real tool descriptions and availability → see the typed question above.
- **Use the result:** Call the selected tool using host-validated arguments. Jev neither invents tools nor writes safe shell commands. Re-observe after execution.
- **Customize:** Tool descriptions, budget and available capabilities.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [P01](skills/jev/references/community.md#p01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a16"></a>
<!-- covers: A16 -->
### 19. Model tier routing

> Use Jev: **Choice:** `small_text`, `reasoning`, `vision`, `cannot_route`. Define tiers by capabilities, not prestige.

- **Input / question:** Current request, required modality, latency/cost constraints and model capability cards → see the typed question above.
- **Use the result:** Host invokes an available model; retain a fallback on quality failure. Evaluate routing regret and total task cost, including reload/caching overhead.
- **Customize:** Quality floor, latency and model-switch/cache costs.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [R04](skills/jev/references/community.md#r04) · [R11](skills/jev/references/community.md#r11) · [N04](skills/jev/references/community.md#n04) · [Jev Codex Router](https://github.com/0xNatoshi/jev-codex-router)
- **Evidence:** Synthetic API smoke output shown below; no end-to-end outcome benchmark for this workflow.

**Observed output** — Explain disagreement between concurrent-write implementations; choices are quick, reasoning and human.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-route/assets/example.json -->
```json
{
  "route": {"status": "selected", "value": "reasoning", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a17"></a>
<!-- covers: A17 -->
### 20. Specialist delegation

> Use Jev: **Choice:** `researcher`, `implementer`, `reviewer`, `stay_with_parent`; describe inputs/outputs and exclusions.

- **Input / question:** Bounded subtask and candidate specialist contracts → see the typed question above.
- **Use the result:** Delegate with a concrete handoff, or keep local work. Independent subtasks and available slots are host facts, not model predictions.
- **Customize:** Handoff size, specialist contracts and host concurrency rules.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [R01](skills/jev/references/community.md#r01) · [P01](skills/jev/references/community.md#p01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a18"></a>
<!-- covers: A18 M02 -->
### 21. Skill/tool discovery

> Use Jev: **Score per optional skill:** 0 = unrelated; 1 = possibly relevant; 2 = directly useful.

- **Input / question:** User task, short installed-skill descriptions and mandatory-trigger rules → see the typed question above.
- **Use the result:** Load relevant optional instructions; always retain mandatory instructions and manual access. This recipe does not rewrite installed skills or global configuration.
- **Customize:** Skill descriptions, mandatory entries and suitability fallback.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [R06](skills/jev/references/community.md#r06) · [R08](skills/jev/references/community.md#r08)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a19"></a>
<!-- covers: A19 H23 U07 -->
### 22. Rerank search and retrieval results

> Use Jev: **Noul per passage:** “Does passage D7 contain information relevant to answering this query?” Define relevant versus merely sharing vocabulary.

- **Input / question:** Query and observed passage IDs/text → see the typed question above.
- **Use the result:** Sort/filter candidates locally while keeping provenance and a recovery path. Relevance does not establish correctness or adequate citation support.
- **Customize:** Relevance criteria, retained depth and false-drop cost.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [P09](skills/jev/references/community.md#p09) · [N03](skills/jev/references/community.md#n03)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a20"></a>
<!-- covers: A20 -->
### 23. Repository navigation

> Use Jev: **Choice:** `auth/session.ts`, `api/login.ts`, `tests/session.test.ts`, `none`; candidates must come from actual discovery.

- **Input / question:** Concrete bug question, directory/file candidates, observed summaries or symbols → see the typed question above.
- **Use the result:** Inspect the selected file, then update the state. Respect any required graph/index search workflow; this is not evidence that a file contains the bug.
- **Customize:** Directory hints, traversal depth and stopping evidence.
- **Start:** [jev-find-code](skills/jev-find-code/SKILL.md) · [Template to adapt](skills/jev-find-code/assets/example.json).
- **Sources / alternatives:** [R12](skills/jev/references/community.md#r12) · [Blink path search](https://github.com/ellipsis-dev/blink)
- **Evidence:** Synthetic API smoke output shown below; no end-to-end outcome benchmark for this workflow.

**Observed output** — Duplicate invoice investigation: p1 = billing/invoices.py; p2 = ui/theme.py, with supplied summaries.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-find-code/assets/example.json -->
```json
{
  "next_file": {"status": "selected", "value": "p1", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a21"></a>
<!-- covers: A21 -->
### 24. Recoverable output reduction

> Use Jev: **Score per block:** 0 = unrelated/redundant; 1 = useful context; 2 = needed evidence; 3 = required diagnostic.

- **Input / question:** Current subgoal plus numbered blocks of one bulky tool result → see the typed question above.
- **Use the result:** Preserve raw output on disk; retain IDs, errors and dependencies. Start with shadow comparison. Do not silently remove history, user constraints or native reasoning state.
- **Customize:** False-drop cost, protected errors and raw-output retrieval.
- **Start:** [jev-context](skills/jev-context/SKILL.md) · [Template to adapt](skills/jev-context/assets/example.json).
- **Sources / alternatives:** [R06](skills/jev/references/community.md#r06) · [P02](skills/jev/references/community.md#p02) · [N05](skills/jev/references/community.md#n05) · [winnow / VINNOW lead](https://github.com/GhalebDweikat/winnow)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): keep diagnostic block, not theme notes; actual context rewriting untested.

**Observed output** — b1 is a quoted-comma parser failure; b2 is color-theme help; investigation is still unfinished.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-context/assets/example.json -->
```json
{
  "b1_needed": {"status": "selected", "value": true, "probability": 0.91},
  "b2_needed": {"status": "selected", "value": false, "probability": 0.03},
  "compact_now": {"status": "selected", "value": "ongoing", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a22"></a>
<!-- covers: A22 -->
### 25. Duplicate observation suppression

> Use Jev: **Noul:** “Would this observation provide no new information for the current subgoal?”

- **Input / question:** Proposed read, last equivalent read, prior result, explicit mutation epoch → see the typed question above.
- **Use the result:** Skip only if code also proves equivalent arguments and unchanged relevant state. Network pages or time-sensitive facts may change without a local mutation.
- **Customize:** Cache lifetime, mutation scope and information-gain criteria.
- **Start:** [jev-context](skills/jev-context/SKILL.md) · [Template to adapt](skills/jev-context/assets/example.json).
- **Sources / alternatives:** [R07](skills/jev/references/community.md#r07)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-compaction"></a>
<!-- covers: M19 U13 -->
### 26. Choose a safe moment to compact

> Use Jev: Is this a completed phase or unfinished investigation? Give a compaction hint; let context pressure change the policy, not the probability.

- **Input / question:** Completion/work-shape judgments + host-measured context usage → hint or opted-in compaction. → see the typed question above.
- **Customize:** Pressure schedule, cooldown, false-trigger cost and hint/automatic mode.
- **Start:** [jev-context](skills/jev-context/SKILL.md) · [Template to adapt](skills/jev-context/assets/example.json).
- **Sources / alternatives:** [compact-adviser](https://github.com/kunchenguid/compact-adviser)
- **Evidence:** Upstream describes small/private-label tuning. Our context example returned ongoing; no actual compaction ran.

<a id="interaction"></a>
## Browser, desktop and interactive tools

[Next browser action](#sc-a23) · [Browser wait versus intervention](#sc-a24) · [Browser outcome verification](#sc-a25) · [Personal-assistant handoff](#sc-a26) · [Smart-home intent resolution](#sc-h26) · [Turn observations into reusable situation labels](#sc-situations) · [Turn partial speech into a browser action](#sc-voice-browser) · [Choose website tools instead of long click sequences](#sc-webmcp) · [Use Jev inside one act, observe or extract step](#sc-primitive) · [Ask the next useful question in a form](#sc-forms) · [Choose controls in a desktop application](#sc-desktop)

<a id="sc-a23"></a>
<!-- covers: A23 U03 U09 -->
### 27. Next browser action

> Use Jev: **Choice:** `click:17`, `select:8:option2`, `scroll:main`, `wait`, `blocked`; offer only compatible operations.

- **Input / question:** Fresh DOM/accessibility snapshot, goal and observed action IDs → see the typed question above.
- **Use the result:** Existing browser tools execute after rechecking snapshot/target freshness. Never turn generated text into selectors or coordinates. Text entry belongs to a separate validated step.
- **Customize:** Allowed actions, target conditions and observation freshness.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [P05](skills/jev/references/community.md#p05) · [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): chose `open_policy`; no browser action executed. Ultrafast timing is an author demo.

**Observed output** — Synthetic page: cancellation-policy link e12, pay button e13, photos e14; read-only task.

<!-- receipt: examples-2026-09-20.json#browser-route -->
```json
{
  "next_step": {"status": "selected", "value": "read_policy", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/examples-2026-09-20.json)

**Observed output** — Second synthetic page: policy link e1 and pay button e2; allowed actions are open_policy, wait and blocked.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-ui/assets/example.json -->
```json
{
  "action": {"status": "selected", "value": "open_policy", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a24"></a>
<!-- covers: A24 -->
### 28. Browser wait versus intervention

> Use Jev: **Choice:** `wait_for_results`, `refresh_observation`, `inspect_error`, `needs_login_or_consent`, `blocked`.

- **Input / question:** Current page status, observed loading/error states and recent action → see the typed question above.
- **Use the result:** Bound waits and retries in code. Do not log in, accept terms, grant permissions or defeat a CAPTCHA because the classifier selects a route.
- **Customize:** Timeouts, retry limits and login/consent handoff.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [P05](skills/jev/references/community.md#p05)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a25"></a>
<!-- covers: A25 -->
### 29. Browser outcome verification

> Use Jev: **Noul per item:** “Does this observation establish the requested route?” Check other fields separately.

- **Input / question:** Fresh result readback and an explicit checklist, such as route/date/results visible → see the typed question above.
- **Use the result:** Code validates exact dates/counts; independently inspect the resulting page. A `DONE` choice is only a request to verify, never proof of a booking/payment.
- **Customize:** Result checklist, exact-field validation and outcome receipts.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [P05](skills/jev/references/community.md#p05)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-a26"></a>
<!-- covers: A26 -->
### 30. Personal-assistant handoff

> Use Jev: **Choice:** `scrape_missing_recipe`, `save_complete_recipe`, `calendar_candidate`, `needs_clarification`, `other`.

- **Input / question:** Inbound text, current task and specialist data requirements → see the typed question above.
- **Use the result:** Build a draft handoff; verify extracted dates/amounts in code and ask before consequential external writes. Routing does not mean extracted facts are correct.
- **Customize:** Workflow inventory, required fields and handoff format.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [R01](skills/jev/references/community.md#r01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h26"></a>
<!-- covers: H26 M04 -->
### 31. Smart-home intent resolution

> Use Jev: **Choice:** `living_room_light_on`, `living_room_light_off`, `no_match`, `clarify`; include room ambiguity.

- **Input / question:** User request, observed devices and currently allowed harmless actions → see the typed question above.
- **Use the result:** Display or execute only pre-authorized low-risk actions through the home controller. Locks, alarms and hazardous appliances need separate strict controls.
- **Customize:** Device names, intent branches and low-risk action allowlists.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [R09](skills/jev/references/community.md#r09)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-situations"></a>
<!-- covers: M12 -->
### 32. Turn observations into reusable situation labels

> Use Jev: From the authorized home observations, estimate whether cooking is happening. Publish a timestamped state for low-risk automations, with unknown and expiry.

- **Input / question:** Observations → named situation probabilities → several deterministic consumers. → see the typed question above.
- **Customize:** Situation definitions, refresh events, freshness and budgets.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [Home Assistant situation layer](skills/jev/references/community.md#p12)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-voice-browser"></a>
<!-- covers: M14 -->
### 33. Turn partial speech into a browser action

> Use Jev: Use the partial transcript and fresh page controls to decide whether I finished a command, which target I mean, or whether to wait.

- **Input / question:** Speech transcript + fresh UI + candidate spans → intent, target and completeness → host action/wait. → see the typed question above.
- **Customize:** Completion rules, debounce, candidate text and confirmation policy.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [Voice-browser implementation](skills/jev/references/community.md#p18)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-webmcp"></a>
<!-- covers: M18 U08 -->
### 34. Choose website tools instead of long click sequences

> Use Jev: If the site exposes a real search_products tool, select that action and let a text model supply its query; validate arguments before execution.

- **Input / question:** Task + exposed website tools → tool selection → argument generation → execution and verification. → see the typed question above.
- **Customize:** Action granularity, argument source, fallback UI and completion criteria.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [WindTunnel](https://github.com/nekuda-ai/WindTunnel) · [Benchmark methodology](skills/jev/references/x-intake-2026-09-20.md)
- **Evidence:** Upstream reports 49/49 tasks by majority of three attempts, 141/147 attempts passed; not reproduced here or a pure interface ablation.

<a id="sc-primitive"></a>
<!-- covers: M18 U12 U23 -->
### 35. Use Jev inside one act, observe or extract step

> Use Jev: Inside this existing Stagehand step, choose the visible element or source text to use. Keep the surrounding workflow unchanged.

- **Input / question:** One observed state + operation-specific candidates → local selection inside a primitive. → see the typed question above.
- **Customize:** Primitive boundary, target inventory, argument source and verification.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [Stagehand author report](https://x.com/kylejeong/status/2101046888468553855)
- **Evidence:** Author description; no Stagehand integration was installed or timed here.

<a id="sc-forms"></a>
<!-- covers: X02 -->
### 36. Ask the next useful question in a form

> Use Jev: Given completed fields and missing information, select a permitted next question, clarification or finish; validate required fields in code.

- **Input / question:** Partial form + allowed questions → next question ID → form renderer. → see the typed question above.
- **Customize:** Question bank, branching rules, completion criteria and skip policy.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [JevForm report](skills/jev/references/twitter-workflows.md#x02)
- **Evidence:** Author-post excerpt, not a source-inspected or reproduced form application.

<a id="sc-desktop"></a>
<!-- covers: E01 -->
### 37. Choose controls in a desktop application

> Use Jev: Use fresh desktop observations to find the export dialog. Stop before overwriting an existing file; verify each actual action.

- **Input / question:** Observed controls + allowed operations → operation/target → host CUA execution. → see the typed question above.
- **Customize:** App-specific actions, prepared values, stopping points and readback checks.
- **Start:** [jev-ui](skills/jev-ui/SKILL.md) · [Template to adapt](skills/jev-ui/assets/example.json).
- **Sources / alternatives:** [Jev Desktop](https://github.com/yikangy873-gif/jev-desktop) · [Setup notes](skills/jev/references/ecosystem.md)
- **Evidence:** Upstream integration samples, not a controlled speedup. Our UI smoke was a synthetic page, not this desktop workflow.

<a id="business"></a>
## Inbox, support and everyday workflows

[Support queue routing](#sc-h02) · [Urgency screening](#sc-h03) · [Conversation concern prefilter](#sc-h15) · [Customer churn signals](#sc-h16) · [Sales/support next-step suggestion](#sc-h17) · [Security incident triage](#sc-h18) · [Suspicious message screening](#sc-h19) · [Form/inquiry routing](#sc-h20) · [Personal inbox/event sorting](#sc-h24) · [Write your own multilabel inbox rules](#sc-mail-rules) · [Filter a research or social feed by your own interests](#sc-personal-feed)

<a id="sc-h02"></a>
<!-- covers: H02 U21 -->
### 38. Support queue routing

> Use Jev: **Choice:** `billing`, `technical`, `account_access`, `security_review`, `other`; distinguish payment disputes from login failures.

- **Input / question:** Ticket text, product context and current queue definitions → see the typed question above.
- **Use the result:** Suggest a queue or send ambiguous/multi-issue tickets to triage. Changing ticket ownership is a separate authorized workflow.
- **Customize:** Queue ownership, multi-issue handling and exclusions.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): bug queue, urgency 1.29/2; bulk routing untested.

**Observed output** — The same order was charged twice, but checkout still worked; the customer requested review today.

<!-- receipt: examples-2026-09-20.json#triage -->
```json
{
  "category": {"status": "selected", "value": "billing", "probability": 1, "margin": 1},
  "needs_human": {"status": "selected", "value": true, "probability": 0.91},
  "urgency": {"status": "scored", "value": 1}
}
```

[Original request and full response](evals/results/examples-2026-09-20.json)

**Observed output** — Export fails for all team members; the monthly report is needed tomorrow.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-triage/assets/example.json -->
```json
{
  "queue": {"status": "selected", "value": "bug", "probability": 1, "margin": 1},
  "urgency": {"status": "scored", "value": 1.29}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-h03"></a>
<!-- covers: H03 -->
### 39. Urgency screening

> Use Jev: **Score:** 0 = informational; 1 = workaround available; 2 = important work blocked; 3 = critical active impact.

- **Input / question:** Reported user impact, affected workflow and incident policy → see the typed question above.
- **Use the result:** Sort a review queue; code applies known severity rules and escalation deadlines. Jev cannot infer unseen affected-user counts.
- **Customize:** Severity anchors, user impact and escalation deadlines.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04) · [R05](skills/jev/references/community.md#r05)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h15"></a>
<!-- covers: H15 -->
### 40. Conversation concern prefilter

> Use Jev: **Noul:** “Does this conversation contain an unresolved product-safety complaint?” Show what counts as unresolved.

- **Input / question:** Authorized, redacted transcript and a precisely defined concern → see the typed question above.
- **Use the result:** Send positives/uncertain cases to a reviewer or larger model. Measure missed concerns; do not claim a low score means the conversation is safe.
- **Customize:** Unresolved criteria, context scope and missed-concern cost.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [R05](skills/jev/references/community.md#r05)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h16"></a>
<!-- covers: H16 -->
### 41. Customer churn signals

> Use Jev: **Noul:** “Does this message express a concrete intent to cancel because of an unresolved issue?” Distinguish hypothetical discussion.

- **Input / question:** Customer message and limited relevant account history → see the typed question above.
- **Use the result:** Prepare a support follow-up queue; no automatic retention offers or account changes. Protect customer data and audit language/domain bias.
- **Customize:** Signal definition, language differences and follow-up policy.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h17"></a>
<!-- covers: H17 -->
### 42. Sales/support next-step suggestion

> Use Jev: **Choice:** `send_requested_docs`, `schedule_followup`, `technical_investigation`, `no_commitment`, `clarify`.

- **Input / question:** Call transcript, promised actions and permitted follow-up types → see the typed question above.
- **Use the result:** Draft an action list with source references; a human verifies commitments and authorizes contact. Classification must not invent a promise.
- **Customize:** Follow-up types, commitment evidence and contact confirmation.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [R05](skills/jev/references/community.md#r05)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h18"></a>
<!-- covers: H18 -->
### 43. Security incident triage

> Use Jev: **Choice:** `possible_account_takeover`, `service_issue`, `benign_change`, `insufficient_evidence`.

- **Input / question:** Redacted incident text and an explicit escalation policy → see the typed question above.
- **Use the result:** Route for investigation; deterministic rules handle known high-risk indicators. Do not disable accounts solely on an uncalibrated model score.
- **Customize:** Incident classes, known indicators and escalation thresholds.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h19"></a>
<!-- covers: H19 -->
### 44. Suspicious message screening

> Use Jev: **Noul:** “Does this message solicit credentials or payment through suspicious instructions?”

- **Input / question:** Message body, displayed sender and observed link metadata; no credentials → see the typed question above.
- **Use the result:** Flag for human review without opening links or attachments. Avoid both a universal spam threshold and a “safe to click” certification.
- **Customize:** Suspicion criteria, organizational rules and review band.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h20"></a>
<!-- covers: H20 -->
### 45. Form/inquiry routing

> Use Jev: **Choice:** `support`, `sales`, `partnership`, `feedback`, `spam_or_other`.

- **Input / question:** Contact form and allowed inquiry-category definitions → see the typed question above.
- **Use the result:** Generate queue labels or draft replies; sending is separate. Keep unrecognized legitimate requests accessible rather than silently discarding them.
- **Customize:** Team boundaries, spam criteria and unknown-request handling.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h24"></a>
<!-- covers: H24 -->
### 46. Personal inbox/event sorting

> Use Jev: **Choice:** `new_event_candidate`, `event_change`, `reminder_only`, `not_an_event`, `ambiguous`.

- **Input / question:** Authorized message text and calendar-related criteria → see the typed question above.
- **Use the result:** Create draft event candidates. Parse dates/time zones separately and confirm conflicts; never add calendar items or invite people without authority.
- **Customize:** Event criteria, timezone and conflict checks.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [R01](skills/jev/references/community.md#r01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-mail-rules"></a>
<!-- covers: M13 -->
### 47. Write your own multilabel inbox rules

> Use Jev: Label each message independently for invoices, travel and action-needed; show conflicts before applying any mailbox action.

- **Input / question:** Message + editable category descriptions → multiple matches → labels or review queue. → see the typed question above.
- **Customize:** Per-label thresholds, precedence, preview mode and allowed effects.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [Mail-classifier configuration](skills/jev/references/community.md#p13)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-personal-feed"></a>
<!-- covers: X05 -->
### 48. Filter a research or social feed by your own interests

> Use Jev: Score these visible posts for my research interests, then let me adjust local weights and undo hiding decisions.

- **Input / question:** Observed posts + personal rubric → saved judgments → reversible ranking/hiding. → see the typed question above.
- **Customize:** Interests, exclusions, local weights, refresh policy and undo.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [Your Signal report](skills/jev/references/twitter-workflows.md#x05)
- **Evidence:** Author-post excerpt; no feed integration installed here.

<a id="documents"></a>
## Documents, research and evidence

[Reading-list/literature screen](#sc-h07) · [Claim-to-source check](#sc-h08) · [Policy checklist triage](#sc-h09) · [Contract-clause sorting](#sc-h10) · [Editorial/brand checks](#sc-h11) · [Job-requirement evidence organization](#sc-h21) · [Extract the right original value](#sc-spans) · [Check whether any candidate is actually suitable](#sc-suitability) · [Recover headings, lists and paragraphs](#sc-structure) · [Extract date meaning, then resolve it in code](#sc-dates) · [Check a cheap model’s structured extraction](#sc-extraction-cascade) · [Annotate talks, interviews or presentations](#sc-transcript)

<a id="sc-h07"></a>
<!-- covers: H07 -->
### 49. Reading-list/literature screen

> Use Jev: **Noul per criterion:** “Does this study evaluate an agent executing tools?” Distinguish mention from measured study.

- **Input / question:** Title, abstract and explicit inclusion criteria → see the typed question above.
- **Use the result:** Prioritize full-text reading; retain uncertain papers. Abstract screening is not a complete eligibility or quality assessment.
- **Customize:** Research scope, inclusion/exclusion criteria and recall preference.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [P09](skills/jev/references/community.md#p09)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h08"></a>
<!-- covers: H08 -->
### 50. Claim-to-source check

> Use Jev: **Noul:** “Do these passages support this exact claim?” Require matching scope, population and conditions.

- **Input / question:** One claim and supplied, identifiable source passages → see the typed question above.
- **Use the result:** Flag weakly supported statements for an actual source read. Support is not truth, and no matching evidence is not proof of falsity.
- **Customize:** Support criteria, source window and scope qualifiers.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04) · [P09](skills/jev/references/community.md#p09) · [N02](skills/jev/references/community.md#n02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h09"></a>
<!-- covers: H09 -->
### 51. Policy checklist triage

> Use Jev: **Choice:** `explicitly_addressed`, `apparently_conflicting`, `not_shown`, `ambiguous`.

- **Input / question:** One supplied policy requirement and relevant document excerpt → see the typed question above.
- **Use the result:** Build a review matrix linked to exact excerpts. Qualified reviewers decide compliance; use current authoritative requirements and do not treat classification as legal advice.
- **Customize:** Requirement version, exceptions and evidence granularity.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [R05](skills/jev/references/community.md#r05)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h10"></a>
<!-- covers: H10 -->
### 52. Contract-clause sorting

> Use Jev: **Choice:** `termination`, `liability`, `data_use`, `payment`, `other`.

- **Input / question:** Contract clauses and a reviewer-authored taxonomy → see the typed question above.
- **Use the result:** Group clauses for a legal reviewer; do not autonomously approve a contract or determine enforceability. A document title is insufficient evidence.
- **Customize:** Clause taxonomy, overlapping labels and exclusions.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [R05](skills/jev/references/community.md#r05) · [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h11"></a>
<!-- covers: H11 -->
### 53. Editorial/brand checks

> Use Jev: **Noul:** “Does this excerpt make an unsupported superlative claim?” Define exclusions such as attributed quotations.

- **Input / question:** Draft excerpt and one concrete editorial rule → see the typed question above.
- **Use the result:** Flag for human revision. Keep one question per rule; the model supplies no trustworthy explanation merely by selecting a label.
- **Customize:** Brand rules, quotation exceptions and attribution requirements.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [P02](skills/jev/references/community.md#p02) · [P04](skills/jev/references/community.md#p04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h21"></a>
<!-- covers: H21 -->
### 54. Job-requirement evidence organization

> Use Jev: **Choice:** `explicit_evidence`, `related_evidence`, `not_stated`; criteria require supplied text.

- **Input / question:** User-authorized résumé text and one job-related requirement → see the typed question above.
- **Use the result:** Help a person locate evidence, not rank or reject candidates. Do not infer protected traits, assess character or equate unstated with absent ability.
- **Customize:** Job-related requirements and evidence strength; no candidate ranking.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [R08](skills/jev/references/community.md#r08)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-spans"></a>
<!-- covers: M01 -->
### 55. Extract the right original value

> Use Jev: Select the invoice-delivery email from these source spans; return its ID so code can copy the original value.

- **Input / question:** Parsed candidate spans + requested role → candidate ID or none → exact source value. → see the typed question above.
- **Customize:** Field role, candidate extraction, normalization and no-match behavior.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [Official span extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): selected s2 (0.97), with a contradicted claim; no OCR/retrieval test.

**Observed output** — s1 = general email hello@example.invalid; s2 = invoice email accounts@example.invalid. The claim incorrectly used s1 for invoices.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-documents/assets/example.json -->
```json
{
  "source": {"status": "selected", "value": "s2", "probability": 0.97, "margin": 0.94},
  "claim_support": {"status": "selected", "value": "contradicted", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-suitability"></a>
<!-- covers: M02 -->
### 56. Check whether any candidate is actually suitable

> Use Jev: Choose the closest passage, then separately judge whether any passage answers the question. Return no match if none does.

- **Input / question:** Question + candidates → best candidate AND a separate suitability judgment. → see the typed question above.
- **Customize:** Absolute suitability criteria, passage size and retrieval fallback.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [Semantic find](https://docs.typesafe.ai/cookbooks/semantic_find)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-structure"></a>
<!-- covers: M03 -->
### 57. Recover headings, lists and paragraphs

> Use Jev: Group these OCR lines without rewriting them, then classify each block as heading, list or paragraph.

- **Input / question:** Line continuity judgments → code builds blocks → block type/attributes → renderer. → see the typed question above.
- **Customize:** Joining rules, block taxonomy, heading levels and uncertain joins.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/document-block.json).
- **Sources / alternatives:** [Autoformat cookbook](https://docs.typesafe.ai/cookbooks/autoformat)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-dates"></a>
<!-- covers: M05 -->
### 58. Extract date meaning, then resolve it in code

> Use Jev: Identify the meaning of “next Friday” using the supplied reference date and timezone; let calendar code calculate the actual date.

- **Input / question:** Date expression → absolute/relative components → deterministic calendar resolution. → see the typed question above.
- **Customize:** Locale, reference time, timezone and invalid-date handling; same split works for units and amounts.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/span-selection.json).
- **Sources / alternatives:** [Date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-extraction-cascade"></a>
<!-- covers: M10 -->
### 59. Check a cheap model’s structured extraction

> Use Jev: Compare these extracted invoice fields with the source. Mark each supported, inconsistent or missing before requesting a bounded repair.

- **Input / question:** Generated fields + independent source → field-level checks → bounded repair/review. → see the typed question above.
- **Customize:** Fields, source windows, failure taxonomy and repair budget.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [Structured extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-transcript"></a>
<!-- covers: M15 -->
### 60. Annotate talks, interviews or presentations

> Use Jev: Apply my rubric to each speaking turn: direct answer, supporting evidence, vague claim. Keep context and show a timeline of annotations.

- **Input / question:** Transcript units + context → independent rubric probabilities → annotations or timeline. → see the typed question above.
- **Customize:** Sentence/turn granularity, surrounding context, labels and aggregation.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [Jevmeter](skills/jev/references/community.md#p19)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="data"></a>
## Data, search and developer workflows

[Semantic grep](#sc-h01) · [Product taxonomy assignment](#sc-h04) · [Duplicate/entity matching](#sc-h05) · [Survey/interview coding](#sc-h06) · [Dataset curation](#sc-h22) · [Navigate a knowledge graph or large hierarchy](#sc-graph) · [Build semantic features for a supervised model](#sc-features) · [Validate meaning after validating JSON shape](#sc-semantic-validation) · [Find a useful command from your history](#sc-shell-history) · [Add semantic predicates to data queries](#sc-semantic-sql) · [Make a spreadsheet column a semantic rubric](#sc-spreadsheet) · [Replay market decisions without placing orders](#sc-market-replay)

<a id="sc-h01"></a>
<!-- covers: H01 -->
### 61. Semantic grep

> Use Jev: **Noul per chunk:** “Does this describe a user unable to complete checkout?” Require actual inability, not generic payment discussion.

- **Input / question:** Numbered text chunks and a precise search criterion → see the typed question above.
- **Use the result:** Show matching IDs and source excerpts. Keep a review band and sample discarded chunks; a low score does not prove no incident.
- **Customize:** Match criteria, near misses and review band.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04) · [SemDecide](https://github.com/sharziki/semdecide)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h04"></a>
<!-- covers: H04 M06 -->
### 62. Product taxonomy assignment

> Use Jev: **Choice:** `fastener`, `bearing`, `seal`, `electrical_component`, `other`; use a second call for observed subcategories if needed.

- **Input / question:** Product description and candidate category definitions → see the typed question above.
- **Use the result:** Produce reviewable labels. For large taxonomies, use a documented hierarchy/shortlist within API limits; test errors introduced by the first-stage filter.
- **Customize:** Taxonomy, hierarchy depth and category boundaries.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [R05](skills/jev/references/community.md#r05) · [N03](skills/jev/references/community.md#n03) · [N04](skills/jev/references/community.md#n04)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h05"></a>
<!-- covers: H05 -->
### 63. Duplicate/entity matching

> Use Jev: **Noul:** “Do these records refer to the same real-world entity?” Criteria: compatible identity attributes, not just similar names.

- **Input / question:** Two records with names, descriptions, locations and provenance → see the typed question above.
- **Use the result:** Suggest duplicate pairs; retain both records until confirmed. Do not merge people/accounts automatically or infer hidden identity.
- **Customize:** Entity type, matching criteria and conflicting fields.
- **Start:** [jev-documents](skills/jev-documents/SKILL.md) · [Template to adapt](skills/jev-documents/assets/example.json).
- **Sources / alternatives:** [R01](skills/jev/references/community.md#r01)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h06"></a>
<!-- covers: H06 -->
### 64. Survey/interview coding

> Use Jev: Separate **Noul** questions for `price_concern`, `missing_feature`, `usability_issue`; codes may co-occur.

- **Input / question:** One response and a predefined qualitative codebook → see the typed question above.
- **Use the result:** Export labels with record IDs; audit disagreements with human coders. Do not force multi-label answers into one mutually exclusive Choice.
- **Customize:** Codebook, context window and coder-disagreement audit.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P04](skills/jev/references/community.md#p04) · [N02](skills/jev/references/community.md#n02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-h22"></a>
<!-- covers: H22 -->
### 65. Dataset curation

> Use Jev: **Score:** 0 = irrelevant/unusable; 1 = partially useful; 2 = directly useful and coherent. Ask separate Nouls for duplication or sensitive-data concerns.

- **Input / question:** One record and an explicit intended-use rubric → see the typed question above.
- **Use the result:** Keep original rows and sidecar scores; audit rejected examples and distribution shifts. Coherence does not establish mathematical correctness or license suitability.
- **Customize:** Intended use, quality anchors and rejection audits.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [P08](skills/jev/references/community.md#p08) · [N02](skills/jev/references/community.md#n02)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-graph"></a>
<!-- covers: M06 -->
### 66. Navigate a knowledge graph or large hierarchy

> Use Jev: Choose relevant neighbors from the current graph node; keep a small frontier and stop when a verified target is reached.

- **Input / question:** Current node + neighbors → local choice → bounded search frontier. → see the typed question above.
- **Customize:** Node descriptions, beam width, visited set and search budget.
- **Start:** [jev-find-code](skills/jev-find-code/SKILL.md) · [Template to adapt](skills/jev-find-code/assets/example.json).
- **Sources / alternatives:** [Hierarchy method](https://docs.typesafe.ai/cookbooks/hierarchical_classification) · [Graph prototype](skills/jev/references/community.md#p14)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-features"></a>
<!-- covers: M08 -->
### 67. Build semantic features for a supervised model

> Use Jev: Propose useful questions about these reviews, use Jev for numeric features, then train a predictor without exposing held-out test labels.

- **Input / question:** Question proposals → labeled-record features → supervised learner → development-error feedback. → see the typed question above.
- **Customize:** Prediction target, question families, learner and train/dev/test split.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [Autoresearch feature discovery](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-semantic-validation"></a>
<!-- covers: M09 -->
### 68. Validate meaning after validating JSON shape

> Use Jev: After schema validation, check whether the description matches the selected category and whether required evidence is actually present.

- **Input / question:** Valid structured data + semantic rules → pass, concern, unknown or unavailable per rule. → see the typed question above.
- **Customize:** Field paths, exceptions, scope and user-facing feedback; exact checks stay in code.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [zod-jev](skills/jev/references/community.md#p16) · [JevLint](skills/jev/references/community.md#p17)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-shell-history"></a>
<!-- covers: M11 -->
### 69. Find a useful command from your history

> Use Jev: Rank these sanitized history commands for the current directory and task; show a suggestion, do not execute it.

- **Input / question:** Existing command candidates + current context → ranked suggestion. → see the typed question above.
- **Customize:** History window, context fields, stale-result rejection and no-match rule.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [Shell-history prototype](skills/jev/references/community.md#p15)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-semantic-sql"></a>
<!-- covers: M16 -->
### 70. Add semantic predicates to data queries

> Use Jev: First select recent feedback rows in SQL, then ask Jev which rows describe an unresolved export failure. Keep row IDs and judgments.

- **Input / question:** Deterministic query → selected row fields → semantic predicate/category/score → filter/group/rank. → see the typed question above.
- **Customize:** Field projection, question, budget and external-data policy.
- **Start:** [jev-triage](skills/jev-triage/SKILL.md) · [Template to adapt](skills/jev-triage/assets/example.json).
- **Sources / alternatives:** [jevQL prototype](skills/jev/references/community.md#p20)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-spreadsheet"></a>
<!-- covers: X04 -->
### 71. Make a spreadsheet column a semantic rubric

> Use Jev: Turn this column heading into clear scoring anchors, then rate each row. When I change the heading, version the rubric and invalidate old scores.

- **Input / question:** Editable column meaning + row text → rubric → row scores. → see the typed question above.
- **Customize:** Column semantics, anchors, row fields, debounce and stale-result handling.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [Predictive spreadsheet report](skills/jev/references/twitter-workflows.md#x04)
- **Evidence:** Author-post excerpt; spreadsheet UI and bulk accuracy not tested here.

<a id="sc-market-replay"></a>
<!-- covers: E05 U05 U15 -->
### 72. Replay market decisions without placing orders

> Use Jev: In a mock replay only, choose among buy, sell and hold from supplied snapshots; reject late decisions and keep intent separate from execution receipts.

- **Input / question:** Historical/synthetic snapshot → bounded decision → dry-run simulator and receipt accounting. → see the typed question above.
- **Customize:** Snapshot age, deadline, one-in-flight scheduling and replay metrics.
- **Start:** [jev-simulation](skills/jev-simulation/SKILL.md) · [Template to adapt](skills/jev-simulation/assets/example.json).
- **Sources / alternatives:** [Jev Trader](https://github.com/jarrodwatts/jev-trader) · [Mock/live distinction](skills/jev/references/x-intake-2026-09-20.md)
- **Evidence:** Author demo plus README describing mock/dry-run defaults; no wallet connected or trading run here.

<a id="creative"></a>
## Ideas, games and creative tools

[Choose legal game and NPC actions](#sc-a28) · [Idea workshop](#sc-h25) · [Reusable document-component selection](#sc-h28) · [Compare options with weights you can change](#sc-reweight) · [Turn world decisions into a visual story](#sc-world-video) · [Let a planner set strategy and Jev handle local moves](#sc-strategy) · [Choose who speaks next in a multi-bot conversation](#sc-speakers) · [Choose a voice delivery style for a script](#sc-tts) · [Keep simulated negotiation from stalling](#sc-negotiation) · [Choose an image or video generator for a request](#sc-creative-route)

<a id="sc-a28"></a>
<!-- covers: A28 H27 -->
### 73. Choose legal game and NPC actions

> Use Jev: **Choice:** `move_left`, `move_right`, `interact`, `wait`; restrict choices to current legal actions.

- **Input / question:** Structured visible game state, legal actions and short objective → see the typed question above.
- **Use the result:** Execute in a sandboxed simulator, observe again and score objective outcomes. This is not vision, strategic reasoning or a physical safety controller.
- **Customize:** Character rubric, goals, action budget and progress measures.
- **Start:** [jev-simulation](skills/jev-simulation/SKILL.md) · [Template to adapt](skills/jev-simulation/assets/example.json).
- **Sources / alternatives:** [R10](skills/jev/references/community.md#r10) · [X01](skills/jev/references/twitter-workflows.md#x01) · [X03](skills/jev/references/twitter-workflows.md#x03) · [R03](skills/jev/references/community.md#r03)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): inspect warehouse; no simulator transition or win-rate measurement.

**Observed output** — Two days of food, storm-closed bridge, accessible warehouse on the same bank; strategy is to seek local supplies.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-simulation/assets/example.json -->
```json
{
  "action": {"status": "selected", "value": "inspect_warehouse", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-h25"></a>
<!-- covers: H25 -->
### 74. Idea workshop

> Use Jev: Separate **Scores** for problem clarity, audience specificity and testability: 0 = absent; 1 = vague; 2 = concrete.

- **Input / question:** Idea description and a rubric defined by the person using the tool → see the typed question above.
- **Use the result:** Calculate summaries in code, then plan actual interviews/tests. These are discussion prompts, not forecasts of business success or investment advice.
- **Customize:** Dimensions, observable anchors and discussion goals.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [P10](skills/jev/references/community.md#p10)
- **Evidence:** Synthetic API smoke output shown below; no end-to-end outcome benchmark for this workflow.

**Observed output** — Offline-first pantry app for busy households; clear audience, but no user or market validation.

<!-- receipt: examples-2026-09-20.json#rubric -->
```json
{
  "audience_fit": {"status": "scored", "value": 1.98},
  "validation": {"status": "selected", "value": "untested", "probability": 1, "margin": 1}
}
```

[Original request and full response](evals/results/examples-2026-09-20.json)

<a id="sc-h28"></a>
<!-- covers: H28 -->
### 75. Reusable document-component selection

> Use Jev: **Choice:** `comparison_table` (parallel attributes), `timeline` (dated sequence), `checklist` (actions), `paragraph` (narrative), `none`.

- **Input / question:** Structured content, audience and fixed component definitions → see the typed question above.
- **Use the result:** Local code renders the chosen component; a person reviews it. This is selection, not text/image generation; escape all untrusted input.
- **Customize:** Component library, audience and information structure.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/document-block.json).
- **Sources / alternatives:** [R12](skills/jev/references/community.md#r12)
- **Evidence:** Adaptation; this exact recipe has not been individually evaluated.

<a id="sc-reweight"></a>
<!-- covers: M07 -->
### 76. Compare options with weights you can change

> Use Jev: Score these proposals for clarity, evidence and effort separately. Save the values so I can change weights without another model call.

- **Input / question:** Focused scores/propositions → saved feature vector → user-weighted shortlist. → see the typed question above.
- **Customize:** Dimensions, anchors, weights and hard exclusions; changed questions require new judgments.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/rubric.json).
- **Sources / alternatives:** [Composite configuration](skills/jev/references/community.md#p12) · [Feature experience](skills/jev/references/community.md#n02)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-world-video"></a>
<!-- covers: M17 X01 -->
### 77. Turn world decisions into a visual story

> Use Jev: Let a planner design a whale-city world, Jev choose legal actions, the simulator update state and a renderer visualize the resulting rounds.

- **Input / question:** Authored world → state + legal actions → decision → simulator → optional images/video. → see the typed question above.
- **Customize:** World rules, character goals, round IDs and rendering medium.
- **Start:** [jev-simulation](skills/jev-simulation/SKILL.md) · [Template to adapt](skills/jev-simulation/assets/example.json).
- **Sources / alternatives:** [gokayfem demo](https://x.com/gokayfem/status/2101022590722810271) · [Access and claim notes](skills/jev/references/twitter-workflows.md#x01)
- **Evidence:** Author reports 264 clips in about five minutes; not our run or proof of exactly 264 API calls.

<a id="sc-strategy"></a>
<!-- covers: M20 X03 U10 U26 -->
### 78. Let a planner set strategy and Jev handle local moves

> Use Jev: Let the planner choose a Pac-Man subgoal; Jev selects legal moves until the subgoal completes, assumptions change or progress stalls.

- **Input / question:** Occasional strategy → repeated local decisions → fresh state → replan trigger. → see the typed question above.
- **Customize:** Subgoals, refresh triggers, progress windows and per-strategy action budget.
- **Start:** [jev-simulation](skills/jev-simulation/SKILL.md) · [Template to adapt](skills/jev-simulation/assets/example.json).
- **Sources / alternatives:** [Pac-Man report](https://x.com/daniel_mac8/status/2100335929273524541) · [Tetris lead](skills/jev/references/twitter-workflows.md#x03)
- **Evidence:** Author demos; no long-horizon success measurement reproduced here.

<a id="sc-speakers"></a>
<!-- covers: M21 U28 -->
### 79. Choose who speaks next in a multi-bot conversation

> Use Jev: Select the next eligible speaker or pause, using the conversation state and turn-taking rules. Let another model write the line.

- **Input / question:** Conversation state + eligible roles → speaker/response-mode ID → dialogue generator. → see the typed question above.
- **Customize:** Roles, eligibility, interruption rules, turn limits and pause conditions.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/voice-style.json).
- **Sources / alternatives:** [Multi-chatbot/TTS report](https://x.com/greenhill_pharm/status/2101492328137711891)
- **Evidence:** Our joint speaker/style call selected analyst + calm; the full output is shown in the next scenario.

<a id="sc-tts"></a>
<!-- covers: M21 U28 -->
### 80. Choose a voice delivery style for a script

> Use Jev: Choose calm, bright, serious or neutral delivery for this fictional line, then map it to a supported TTS preset.

- **Input / question:** Script + delivery rubric → style label → TTS preset; audio generated elsewhere. → see the typed question above.
- **Customize:** Style labels, voice mappings, smoothing and neutral fallback.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/voice-style.json).
- **Sources / alternatives:** [Creator report](https://x.com/greenhill_pharm/status/2101492328137711891)
- **Evidence:** [Live synthetic example](evals/SCENARIO_EXAMPLES.md): analyst + calm; no speech generated.

**Observed output** — A host invites the analyst to explain conflicting evidence in a fictional podcast; choose speaker and delivery style.

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev/assets/voice-style.json -->
```json
{
  "speaker": {"status": "selected", "value": "analyst", "probability": 1, "margin": 1},
  "delivery": {"status": "selected", "value": "calm", "probability": 0.98, "margin": 0.96}
}
```

[Original request and full response](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-negotiation"></a>
<!-- covers: X06 -->
### 81. Keep simulated negotiation from stalling

> Use Jev: In this Catan-style negotiation, choose accept, counter, decline or pass from legal moves, and stop after the no-progress budget is exhausted.

- **Input / question:** Offer history + legal options → local response → host progress/deadlock check. → see the typed question above.
- **Customize:** Negotiation budget, utility rubric, pass/terminate options and progress definition.
- **Start:** [jev-simulation](skills/jev-simulation/SKILL.md) · [Template to adapt](skills/jev-simulation/assets/example.json).
- **Sources / alternatives:** [Catan failure report](skills/jev/references/twitter-workflows.md#x06)
- **Evidence:** The source reports agents stopping negotiation; this is a failure-informed adaptation, not a demonstrated fix.

<a id="sc-creative-route"></a>
<!-- covers: X07 -->
### 82. Choose an image or video generator for a request

> Use Jev: Choose from my available generators using the requested medium, edit needs, output size and budget; invoke the selected tool separately.

- **Input / question:** Creative brief + current capability cards → generator ID or no match. → see the typed question above.
- **Customize:** Medium, edit support, latency, budget and output evaluation rubric.
- **Start:** [jev-route](skills/jev-route/SKILL.md) · [Template to adapt](skills/jev-route/assets/example.json).
- **Sources / alternatives:** [Creative-model routing demo](skills/jev/references/twitter-workflows.md#x07)
- **Evidence:** Author-post excerpt; no generation or quality comparison reproduced.

<a id="building"></a>
## Build and connect your own tools

[Turn a plain-language task into editable questions](#sc-compile) · [Add reusable decision tools through MCP](#sc-mcp) · [Learn by changing examples in a playground](#sc-playground)

<a id="sc-compile"></a>
<!-- covers: M22 -->
### 83. Turn a plain-language task into editable questions

> Use Jev: Turn “find feedback about active blockers” into typed questions and criteria. Show near-miss examples before applying it to each record.

- **Input / question:** User request → model drafts questions → schema/rubric review → Jev judges scoped records. → see the typed question above.
- **Customize:** Question meaning, candidate labels, row IDs, rubric version and consumer.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/semantic-rules.json).
- **Sources / alternatives:** [OpenRouter question compiler](https://openrouter.ai/labs/jev/compile)
- **Evidence:** Source-described pattern; this adaptation has not been run here.

<a id="sc-mcp"></a>
<!-- covers: E02 -->
### 84. Add reusable decision tools through MCP

> Use Jev: Expose either one generic evaluate tool or named classify/verify/rerank tools, with my editable criteria and an explicit review path.

- **Input / question:** Agent tool call + state/questions → typed judgment → existing host workflow. → see the typed question above.
- **Customize:** Tool surface, model pin, provider and downstream action policy.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/triage.json).
- **Sources / alternatives:** [TypeSafe MCP](https://github.com/itsmostafa/typesafe-mcp) · [Jev MCP](https://github.com/jkudish/jev-mcp)
- **Evidence:** Both checked versions support OpenRouter; neither installed here. Setup helpers may change configs/store keys: review them first.

<a id="sc-playground"></a>
<!-- covers: E03 U29 -->
### 85. Learn by changing examples in a playground

> Use Jev: Clone a reviewed playground, inspect one example’s state, questions, sample inputs and consumer, then ask the coding agent to add a related example.

- **Input / question:** Editable example → alternative inputs → inspect judgments and consumer behavior. → see the typed question above.
- **Customize:** Task, rubric, edge cases, live/mock mode and consumer.
- **Start:** [jev](skills/jev/SKILL.md) · [Template to adapt](skills/jev/assets/triage.json).
- **Sources / alternatives:** [TypeSafe AI Playground](https://github.com/TypeSafeAI/typesafe-playground) · [Jev Explained](https://github.com/davila7/jev-explained)
- **Evidence:** READMEs checked; playgrounds not run. TypeSafe AI Playground documents live calls, mocks and local solvers separately.

## Make probabilities useful

“Auto-handle / stronger model / person” is a **customizable policy**, not a universal
0.9/0.7 rule. First define which answer's probability you mean, check it against
held-out labels and choose thresholds for the cost of mistakes. A `score` is not
a probability; confidence is not permission. [Calibration guide](skills/jev/references/calibration.md).

For every scenario: keep an unknown route, observe fresh state and verify the
outcome after acting. Jev does not browse, execute tools or generate prose by itself.
Data sent for judgment goes to OpenRouter and its provider; use synthetic data first.

<a id="experiments"></a>
## Experiments you can inspect

- [Agent before/after](evals/RESULTS.md): 12 pairs, baseline 12/12 vs fixed-checkpoint 10/12. Small negative result for that integration policy.
- [Decision/calibration pilot](evals/CALIBRATION_RESULTS.md): 136/160 benchmark labels matched; the confidence ≥0.9 group still had 8/100 errors.
- [Nine scenario API examples](evals/SCENARIO_EXAMPLES.md): observed answers for all eight focused skills plus voice direction; no host actions.
- [Five earlier live API examples](evals/results/examples-2026-09-20.json): request/response smoke receipts, not scenario-level accuracy tests.
- [Validation and reproduction](docs/validation.md): package checks, dry runs and untested host boundaries are recorded separately.

## More to explore · Credits

This collection builds on discovery work from
[Anil-matcha/awesome-jev-by-typesafe](https://github.com/Anil-matcha/awesome-jev-by-typesafe),
[cobanov/awesome-jev](https://github.com/cobanov/awesome-jev),
[yibie/awesome-jev](https://github.com/yibie/awesome-jev),
[yzfly/awesome-jev-zh](https://github.com/yzfly/awesome-jev-zh) and
[hellogumbo/awesome-jev](https://github.com/hellogumbo/awesome-jev).

Go deeper: [pinned project research](skills/jev/references/ecosystem.md) ·
[Reddit, GitHub and other field reports](skills/jev/references/community.md) ·
[29 supplied X posts and follow-up checks](skills/jev/references/x-intake-2026-09-20.md) ·
[56 agent/human recipes](skills/jev/references/index.md).

Inspired also by the [official Jev skill](https://docs.typesafe.ai/agent-skill).

Special thanks to [LINUX DO](https://linux.do/?tl=en).

[MIT](LICENSE); linked projects retain their own licenses.
