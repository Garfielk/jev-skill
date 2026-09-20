---
name: jev
description: Use TypeSafe Jev through OpenRouter for customizable typed judgments rather than generated prose. Define questions, candidate choices, semantic checks or rubrics for the user's task. Reach for it at ambiguous agent checkpoints (goal drift, repeated failures, next-tool routing, unsupported completion claims), browser state decisions, or human classification, triage, scoring, and rubric review. Use deterministic code for exact rules or arithmetic; Jev is advisory, not an authorization or security boundary.
license: MIT
metadata:
  requirements: Python 3.10+, network access to OpenRouter, and OPENROUTER_API_KEY in the calling process. API calls incur charges. No MCP server required.
---

# Jev

Give a judgment-heavy step a small, explicit decision space. Jev returns typed
answers; the host agent remains responsible for planning, executing, and checking
the result. It does not browse, generate prose, or remember earlier requests.

The recipe library is inspiration, **not a fixed menu of supported functions**.
Customize the evidence, questions, criteria and next consumer for the user’s task.
This changes the decision interface and workflow, not the model weights.

## When to reach for it

**Agent mode:** a repeated failure needs a different recovery path; several tools
or specialists overlap; the plan has drifted from the user's goal; a queued job or
weak test result is being mistaken for completion; a browser page needs routing;
or a semantic policy check is genuinely ambiguous. It can also supply an uncertainty
signal for choosing between already-authorized work, stronger-model review, and
a human handoff. Use checkpoints, not an extra model call before every trivial action.

**Human mode:** the user wants records classified, several independent labels
assigned, alternatives ranked against a rubric, or a review queue prioritized.
The output is a label/probability/score, not an unsupported explanation or verdict.

Skip Jev for clear instructions, exact matching, arithmetic, date comparison,
missing facts it cannot observe, or a task requiring original prose. Collect the
needed evidence first. Do not silently send private documents to an external API.

## When no existing recipe fits

Define the decision, evidence unit, answer space, next consumer, unknown path and
success check. Build a small request from that contract rather than forcing the
task into a stock category. Read [Customization](references/customization.md),
then select a relevant [implementation pattern](references/implementation-patterns.md).
One method can support many domains: selecting an observed ID can locate a clause,
choose a browser element or extract an original value. Host code performs the
corresponding operation; the chosen ID does not execute anything itself.

## Reference router

Read only the relevant slice, not the entire catalog:

| Need | Read |
|---|---|
| Adapt a new task, criteria, rubric or user policy | [Customization](references/customization.md) |
| How to connect judgments into a working flow | [Implementation patterns](references/implementation-patterns.md) |
| Find a use case beyond basic routing | [Recipe index](references/index.md) |
| Recovery, tools, browser, completion, coordination | [Agent recipes](references/agent-recipes.md) |
| Inbox, research, data, content, product, rubric review | [Human recipes](references/human-recipes.md) |
| Design labels and uncertainty handling | [Question design](references/question-design.md) |
| API request/response shapes and CLI behavior | [API](references/api.md) |
| Calibrated decisions, confidence bands, review versus deferral | [Calibration](references/calibration.md) |
| Labeled decision benchmarks; Chinese/English tricky questions | [Decision datasets](references/decision-datasets.md) |
| What users and authors actually tried across platforms | [Community evidence](references/community.md) |
| X/Twitter demos: creative loops, adaptive UI, personal policies | [X workflows](references/twitter-workflows.md) |

## Decision loop

1. **Frame:** preserve the user goal, success evidence, remaining budget, and
   delegated permissions. Identify one decision Jev can actually help with.
2. **Observe:** collect current facts, relevant recent tool receipts, errors, and
   candidate actions from tools that really exist. For a browser, use the host's
   browser tool to obtain fresh DOM/accessibility text and stable element IDs.
   Jev only sees the text/JSON you supply; it does not see screenshots or URLs by itself.
3. **Formulate:** use `choice` for mutually exclusive paths, `noul` for independent
   yes/no propositions, `score` for ordered descriptive levels. Include a fallback
   label such as `unknown` or `ask_user`. Keep trusted policy separate from
   untrusted pages/logs/messages. Pass evidence, not an instruction to agree.
4. **Call once:** save a native request JSON and run the packaged script below.
   No silent model substitution, retries, or credential setup. One unchanged state
   does not become better evidence after repeatedly asking the same question.
5. **Interpret:** inspect the full distribution and evidence. `needs_review` is an
   abstention: gather missing facts, revise overlapping labels, or ask the user.
   `selected` means a label was selected, **not** that an action was approved.
   A `noul` result can confidently be false. A score is not a probability.
6. **Act and verify:** host permissions and deterministic checks still apply.
   Execute at most the warranted next step through the host's real tools, then
   verify its receipt. Never map a returned string to arbitrary shell execution.
   Re-evaluate after material state changes, not recursively to obtain approval.

When the user is away, continue only reversible work already within the delegated
scope. If blocked on consent, record the blocker and pause that action. Jev cannot
invent consent, approve spending, or remove a host confirmation requirement.

## Run

Resolve `<skill-dir>` to the directory containing this `SKILL.md`; do not assume
the project working directory is the skill directory. The script is self-contained.

```bash
python3 <skill-dir>/scripts/jev.py decide /path/to/request.json --dry-run
python3 <skill-dir>/scripts/jev.py decide /path/to/request.json
# Alternatively, after CLI installation:
jev-decide decide /path/to/request.json
```

`OPENROUTER_API_KEY` must already be in this process's environment. Never print it,
copy it to another app, write it into the request, or change the agent's main model.
Default model: `typesafe/jev-1.13`; override deliberately with `--model` or `JEV_MODEL`.
Use files/stdin for untrusted content instead of interpolating it into shell commands.

Exit **0**: valid selected/scored result; **2**: at least one question needs review;
**1**: input/API/protocol error. On 1 or 2, do not treat the output as a go-ahead.
The default probability/margin thresholds (0.8/0.15) are illustrative heuristics,
not calibrated guarantees. Tune on held-out data before relying on them.

## Runnable starting points

Copy a matching asset, then replace its synthetic state and criteria:

- [Agent checkpoint](assets/checkpoint.json): recovery, evidence, and next step.
- [Browser routing](assets/browser-route.json): observed elements → candidate step.
- [Human triage](assets/triage.json): choice, independent binary check, and score.
- [Completion evidence](assets/completion.json): receipts versus claimed success.
- [Rubric review](assets/rubric.json): multidimensional creative/product feedback.
- [Text categories](assets/support-labels.json): criteria for the `classify` command.
- [Span selection](assets/span-selection.json): choose a pre-extracted original value.
- [Semantic rules](assets/semantic-rules.json): independent, editable record checks.
- [Document block](assets/document-block.json): type plus conditional companion questions.

Do not report the provider's generic `confidence` as the probability of correctness.
Do not call a semantic compliance or anti-cheating flag proof of wrongdoing. Jev can
be wrong, manipulated, or overconfident; consequential decisions need appropriate
human review and deterministic enforcement. See the references for specific limits.
