# Awesome Jev Skills

**Practical things to do with Jev — examples you can edit, skills you can install,
and community projects you can build on.**

Jev chooses, classifies and scores; your agent supplies the context and does the
work. Use it inside an agent, or as a tool for your own messages, documents and decisions.

[中文](README.zh.md) · [Install](docs/installation.md) · [Community projects](skills/jev/references/ecosystem.md) · [More recipes](skills/jev/references/index.md)

## Pick something to try

[Sort messages](#triage) · [Filter records](#filter) · [Read documents](#documents) ·
[Browse](#browser) · [Use desktop apps](#desktop) · [Route tools and models](#routing) ·
[Manage context](#context) · [Review code](#review) · [Find code](#search) ·
[Unstick an agent](#checkpoint) · [Run a game](#simulation) · [Control voices](#voices) ·
[Add MCP tools](#mcp) · [Build your own](#custom)

**In this repo:** eight focused skills, a general `jev` skill, editable JSON
examples and one shared OpenRouter CLI. **Linked projects:** optional alternatives,
not bundled integrations. Read their setup requirements before choosing one.

### Start from this checkout

The public release is pending; these commands work from a downloaded checkout.
Python 3.10+, [uv](https://docs.astral.sh/uv/) and Node/npm are needed for this route.

```bash
uv tool install .
npx skills add . --skill jev-triage
export OPENROUTER_API_KEY="your-key"
jev-decide decide skills/jev-triage/assets/example.json --dry-run
```

Choose Codex, Claude Code or OpenCode in the installer. Replace `jev-triage` with
the skill you want below. Then ask your agent to use it. For manual use, edit the
JSON and remove `--dry-run` to call Jev (paid). [Installation options](docs/installation.md).

**Example status:** the eight focused examples and voice example passed
[real API smoke calls](evals/SCENARIO_EXAMPLES.md), using synthetic input—not
completed real-world tasks. Upstream demos are author reports unless marked
otherwise. [Our experiments](#experiments) also include negative results.

<a id="triage"></a>
## 1. Sort an inbox or support queue

> Use jev-triage to sort these tickets into billing, bugs, how-to and other. Flag
> urgent blockers and ambiguous cases; show me the table before changing anything.

- **Flow:** message + your categories → queue, urgency and review status.
- **Make it yours:** VIP customers, deadline rules, team ownership or multiple labels per message.
- **Start:** [jev-triage skill](skills/jev-triage/SKILL.md) · [ticket example](skills/jev-triage/assets/example.json).
- **Other ways:** [Jev MCP](https://github.com/jkudish/jev-mcp) for a named classify tool; [SemDecide](https://github.com/sharziki/semdecide) for scripts.
- **Experiment:** our [earlier triage request](skills/jev/assets/triage.json) passed a live API smoke check; bulk mailbox accuracy and writes were not tested.

<a id="filter"></a>
## 2. Filter records using a rule written in plain English

> Use jev-triage to find feedback that describes a current blocker, not a feature
> wish. Keep the original IDs and send borderline records to a review list.

- **Flow:** one record + a semantic rule → keep, skip or review. Use code for exact dates and counts.
- **Make it yours:** paper screening, customer feedback, log triage or dataset inclusion criteria.
- **Start:** [record classification skill](skills/jev-triage/SKILL.md) · [editable record example](skills/jev-triage/assets/example.json) · [independent rule checks](skills/jev/assets/semantic-rules.json).
- **Other ways:** [SemDecide](https://github.com/sharziki/semdecide) provides actual JSONL filtering: after its separate setup, `cat tickets.jsonl | semdecide filter 'The customer reports a current service blocker' --field text`.
- **Experiment:** source checked, not reproduced. Our CLI judges requests; it does not provide SemDecide's streaming filter command.

<a id="documents"></a>
## 3. Find the right clause, field or supporting passage

> Use jev-documents to select the billing email from these observed spans, then
> check whether this passage supports the claim. Return the original span, not a rewrite.

- **Flow:** source text + indexed candidate spans → selected span ID; claim + evidence → supported, contradicted or unknown.
- **Make it yours:** invoice fields, contract clauses, citations or research evidence. Use host OCR first for scans.
- **Start:** [jev-documents skill](skills/jev-documents/SKILL.md) · [span and evidence example](skills/jev-documents/assets/example.json).
- **Other ways:** [Jev MCP](https://github.com/jkudish/jev-mcp) extraction/verification tools or [TypeSafe AI Playground](https://github.com/TypeSafeAI/typesafe-playground) document examples.
- **Experiment:** the [live example](evals/SCENARIO_EXAMPLES.md) selected the billing span and flagged a contradicted claim. Retrieval and OCR were not tested.

<a id="browser"></a>
## 4. Choose the next browser action

> Use jev-ui to find this hotel's cancellation policy. Observe the page, choose
> a relevant link, open it with the browser tool, then verify the policy text. Do not book.

- **Flow:** fresh DOM/accessibility text + available actions → one action → host browser executes → fresh observation.
- **Make it yours:** navigation, form steps, product comparison or read-only research. A text model supplies free-form typing when needed.
- **Start:** [jev-ui skill](skills/jev-ui/SKILL.md) · [observed-controls example](skills/jev-ui/assets/example.json).
- **Other ways:** [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) for a browser loop; [WindTunnel/WebMCP](https://github.com/nekuda-ai/WindTunnel) for website-exposed tools.
- **Experiment:** Ultrafast's fast flight-search demo and WindTunnel's task results use different setups; see [methodology notes](skills/jev/references/x-intake-2026-09-20.md). Our skill needs an existing browser tool.

<a id="desktop"></a>
## 5. Choose controls in a desktop app

> Use jev-ui with the desktop tool to locate the export dialog. Choose only
> controls visible in the current observation; stop before saving over an existing file.

- **Flow:** observed app controls + permitted operations → operation/target → host action and verification.
- **Make it yours:** an app-specific action list, prepared typing values and explicit stopping points.
- **Start:** [same UI skill](skills/jev-ui/SKILL.md) · [adapt this indexed-controls example](skills/jev-ui/assets/example.json).
- **Other ways:** [Jev Desktop](https://github.com/yikangy873-gif/jev-desktop) integrates with an existing Codex Computer Use runtime.
- **Experiment:** upstream reports integration samples, not a controlled speedup. Installing this skill does not install desktop control or grant permissions.

<a id="routing"></a>
## 6. Pick a tool, specialist or model for each step

> Use jev-route to choose between the fast model, reasoning model and human review
> for these tasks. Use their actual capabilities and return recommendations first.

- **Flow:** task + real capability/cost inventory → selected route or no suitable route.
- **Make it yours:** latency budget, tool descriptions, skill catalogue, reviewer roles or escalation policy.
- **Start:** [jev-route skill](skills/jev-route/SKILL.md) · [model-routing example](skills/jev-route/assets/example.json).
- **Other ways:** [Jev Codex Router](https://github.com/0xNatoshi/jev-codex-router) adds routing to its author's existing macOS Codex Router service.
- **Experiment:** its backtest reprices historical tokens; it is not a quality-controlled rerun. Our skill recommends a route, not a host configuration change.

<a id="context"></a>
## 7. Keep useful context and choose when to compact

> Use jev-context in advisory mode: which tool-output blocks matter for the
> current bug, and is this a safe task boundary for compaction? Keep raw output recoverable.

- **Flow:** goal + indexed output blocks + unresolved work → relevance judgments and a separate compaction decision.
- **Make it yours:** context pressure, false-drop cost, protected errors and retrieval handles. Start with a shadow log, not automatic deletion.
- **Start:** [jev-context skill](skills/jev-context/SKILL.md) · [keep/compact example](skills/jev-context/assets/example.json).
- **Other ways:** [winnow](https://github.com/GhalebDweikat/winnow) filters tool results; [compact-adviser](https://github.com/kunchenguid/compact-adviser) targets safe compaction checkpoints.
- **Experiment:** upstream small labeled evaluations are not reproduced here. “VINNOW” is provisionally mapped to winnow; [details](skills/jev/references/ecosystem.md).

<a id="review"></a>
## 8. Prioritize code review and flag suspicious fixes

> Use jev-code-review on this diff. Flag changes that weaken tests instead of
> fixing behavior, rank review leads and point me to the evidence. Run the real tests separately.

- **Flow:** diff + requirements + test receipts → risk signals and review priorities → inspect and verify.
- **Make it yours:** auth, data loss, concurrency, test integrity or repository-specific invariants.
- **Start:** [jev-code-review skill](skills/jev-code-review/SKILL.md) · [weakened-test example](skills/jev-code-review/assets/example.json).
- **Other ways:** [Jev Review](https://github.com/devagrawal09/jev-review) offers a staged review workflow and dashboard; [blink.review](https://blink.review) advertises a code-review CLI.
- **Experiment:** source/landing-page checks only. A risk flag is a lead, not a verified vulnerability or a replacement for tests.

<a id="search"></a>
## 9. Find where a behavior lives in a large codebase

> Use jev-find-code to narrow down where invoices are generated. Prefer the
> project's code graph, select plausible paths and open them to verify before editing.

- **Flow:** task + actual graph/path candidates → next location to inspect → source confirmation.
- **Make it yours:** naming conventions, directory hints, search depth and what counts as sufficient evidence.
- **Start:** [jev-find-code skill](skills/jev-find-code/SKILL.md) · [path-selection example](skills/jev-find-code/assets/example.json).
- **Other ways:** [ellipsis-dev/blink](https://github.com/ellipsis-dev/blink) searches paths with weighted walkers. After its setup: `./blink "where are invoices generated?" /path/to/repo -r`.
- **Experiment:** upstream inspected, not run. This Blink repository is path search, distinct from the review surface above; filename relevance is not code understanding.

<a id="checkpoint"></a>
## 10. Help an agent recover — or recognize it is not finished

> Use Jev to review the last three failed steps against my goal. Choose between
> inspecting evidence, changing the plan, retrying or pausing. Check actual receipts before claiming completion.

- **Flow:** goal + recent actions/outcomes + candidate recovery steps → checkpoint advice.
- **Make it yours:** repeated-error definition, remaining budget, completion evidence and permitted work while you are away.
- **Start:** [general jev skill](skills/jev/SKILL.md) · [checkpoint example](skills/jev/assets/checkpoint.json) · [completion example](skills/jev/assets/completion.json).
- **Other ways:** use a named decision/verification tool from [Jev MCP](https://github.com/jkudish/jev-mcp).
- **Experiment:** our [12-pair pilot](evals/RESULTS.md) got **12/12 baseline vs 10/12 with fixed Jev checkpoints**, at higher cost. Use selective checkpoints; improvement is not guaranteed.

<a id="simulation"></a>
## 11. Run NPCs, decision games or branching stories

> Use jev-simulation for this island-town game. Let the planner define strategy,
> Jev choose among legal actions and the simulator update the world. Log outcomes before rendering scenes.

- **Flow:** strategy + current world + legal actions → chosen action → deterministic state transition. Rendering is a separate optional step.
- **Make it yours:** goals, NPC roles, legal moves, resources, replan triggers or story branches.
- **Start:** [jev-simulation skill](skills/jev-simulation/SKILL.md) · [island-town example](skills/jev-simulation/assets/example.json).
- **Other ways:** [the world/decision/video demo and Pac-Man reports](skills/jev/references/twitter-workflows.md) illustrate planner–actor splits; [Playground](https://github.com/TypeSafeAI/typesafe-playground) includes interactive examples.
- **Experiment:** our [live example](evals/SCENARIO_EXAMPLES.md) chose to inspect the warehouse; no simulator transition was run. Social throughput claims remain author reports.

<a id="voices"></a>
## 12. Direct a conversation or choose a TTS delivery style

> Use Jev to choose the next eligible speaker and a delivery style for this
> fictional dialogue. Let the language model write the line and the TTS engine render it.

- **Flow:** dialogue state + speaker/style options → selected IDs → dialogue/TTS tools.
- **Make it yours:** turn-taking rules, available voices, emotional tone, interruption policy or a pause option.
- **Start:** [general jev skill](skills/jev/SKILL.md) · [speaker/style example](skills/jev/assets/voice-style.json).
- **Other ways:** a creator's [multi-chatbot and seven-emotion TTS report](skills/jev/references/x-intake-2026-09-20.md) inspired this adaptation.
- **Experiment:** our [live example](evals/SCENARIO_EXAMPLES.md) chose analyst + calm; no TTS was run. Labels are our adaptation, not the author's configuration or a diagnosis of a person's emotions.

<a id="mcp"></a>
## 13. Give an MCP-capable agent reusable decision tools

> Use a decision tool to classify this request, check the evidence and choose
> a next step from my available tools. Keep uncertain cases visible.

- **Choose one:** [TypeSafe MCP](https://github.com/itsmostafa/typesafe-mcp) exposes one generic `evaluate` tool; [Jev MCP](https://github.com/jkudish/jev-mcp) exposes named tasks such as classify, verify and rerank. Both checked versions support OpenRouter.
- **Make it yours:** tool criteria, model pinning and how each answer is consumed. MCP and filesystem skills are different installation surfaces.
- **Start without MCP:** [general skill](skills/jev/SKILL.md) · [native request](skills/jev/assets/triage.json). Our CLI needs no MCP server.
- **Setup/evidence:** [provider and installation notes](skills/jev/references/ecosystem.md); source checked, neither server installed here. Do not blindly run helpers that rewrite client configs or store keys.

<a id="custom"></a>
## 14. Turn your own judgment into a small tool

> Help me build a Jev workflow for screening research ideas. Define useful
> evidence, editable criteria, an unknown path and a small labeled test set before automating it.

- **Flow:** your task → evidence → `choice` (one route), `noul` (a yes/no proposition) or `score` (anchored levels) → a useful consumer.
- **Make it yours:** a personal rubric, policy check, semantic feature, reranker, entity matcher or structured annotation.
- **Start:** [general skill](skills/jev/SKILL.md) · [rubric example](skills/jev/assets/rubric.json) · [customization guide](skills/jev/references/customization.md) · [22 implementation patterns](skills/jev/references/implementation-patterns.md).
- **Other ways:** [TypeSafe AI Playground](https://github.com/TypeSafeAI/typesafe-playground) is an independent community playground, not an official TypeSafe product. It separates live Jev, mocks and local solvers.
- **Experiment:** our earlier rubric request passed a live smoke call; this does not establish agreement with your preferences. Start with labeled examples, then measure disagreements.

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
Independent project, not affiliated with TypeSafe or OpenRouter; this is not an
open release of Jev's model weights. [MIT](LICENSE); linked projects retain their own licenses.
