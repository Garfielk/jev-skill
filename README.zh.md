# Awesome Jev Skills

**Jev 具体能做什么：可修改的例子、可安装的技能，以及值得参考的社区项目。**

Jev 负责选择、分类和评分，agent 负责提供上下文和执行。
既可以把它接进 agent，也可以自己拿来处理消息、文档和需要判断的事情。

[English](README.md) · [安装](docs/installation.md) · [社区项目](skills/jev/references/ecosystem.md) · [方法与来源](skills/jev/references/index.md)

## 安装：复制给你的 Agent

把下面这段话发给 **Codex、Claude Code 或 OpenCode**：

```text
帮我给当前 Agent 安装 Jev Skills，包括通用技能和全部场景技能。请读取并按照这份安装指南操作，完成后验证安装是否成功：
https://raw.githubusercontent.com/wuyoscar/jev-skill/main/docs/install.md
```

Agent 会检查环境，默认安装到当前项目，并完成离线验证。
你不用自己运行命令；只需处理必要的授权，以及在本地配置 `OPENROUTER_API_KEY`，不要把密钥发进聊天。
不需要 Vercel 账号；Node/npm 也不是默认安装方式的依赖。
[Agent 安装指南](docs/install.md) · [手动安装与排错](docs/installation.md)

## 全部场景，都在这里

这里展开 **85 个场景与接入用法**：覆盖此前 56 条 agent / 人工配方、22 种连接方法，
以及 X 分享和项目调研中的具体用法。重复场景合并，方法可以用于多个场景。
这是目前已读材料的合集，不是 Jev 能力的上限；只有标题或截断前言的帖子没有被凑成新场景。

每节都给出可复制的任务、输入输出、可改标准、技能/模板和来源。
**已有的 14 次真实 API 示例输出直接放在对应章节里**；未测场景写明状态，不拿演示当复现。

本仓库仍是 **8 个场景技能 + 1 个通用技能**，不是 85 个重复安装包。
同一个技能可以承载多种自定义任务。下面的 JSON 链接是可修改模板，
除标出的实测输入外，不代表已经替每个场景写好完整应用。

- [长程任务与恢复](#agent) — 5 个
- [监督、审查与评测](#quality) — 9 个
- [路由、委派与上下文](#routing) — 12 个
- [浏览器、桌面与交互工具](#interaction) — 11 个
- [消息、客服与日常工作流](#business) — 11 个
- [文档、研究与证据](#documents) — 12 个
- [数据、检索与开发工具](#data) — 12 个
- [想法、游戏与创作](#creative) — 10 个
- [制作与接入自己的工具](#building) — 3 个

### 怎么读例子

- **用法示例**是可以交给 agent 的任务；你也可以自己修改 JSON，用 `jev-decide` 调用。
- **实际输出**逐项摘录已保存的 CLI `decisions`，省略评分等级的文字描述，数值未改。
  Choice 的 `probability` 是选中标签的概率；Noul 的 `probability` 始终是命题为真的概率，
  因此 `value: false, probability: 0.02` 表示“不支持”，不是“只有 2% 把握”。评分不是概率。
- 实测输入为合成数据，真实调用的是 API，没有因此操作邮箱、桌面或交易账户。
  上游性能数字单独归给原作者；扩展用法给出例子，但不编造输出。

<a id="agent"></a>
## 长程任务与恢复

[检查长程任务有没有跑偏](#sc-a01) · [从反复失败的循环里脱困](#sc-a02) · [检查任务是否真的完成](#sc-a06) · [拦住没有证据的“已完成”表述](#sc-a07) · [复盘一次 agent 失败发生在哪里](#sc-a27)

<a id="sc-a01"></a>
<!-- covers: A01 -->
### 1. 检查长程任务有没有跑偏

> 对照最初验收标准，判断“现在去改主题颜色”是否推进修复登录失败这个目标。

- **输入 → 输出：**目标、验收项、最近结果、拟做动作 → 是否直接推进目标。
- **可以改：**里程碑触发时机、验收项、允许的旁支工作；不要擅自重写目标。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/checkpoint.json)。
- **来源 / 可选项目：**[R02](skills/jev/references/community.md#r02) · [P02](skills/jev/references/community.md#p02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a02"></a>
<!-- covers: A02 -->
### 2. 从反复失败的循环里脱困

> 同一测试已经失败三次。用 Jev 在读错误、换假设、验证新修复、升级求助之间选一步。

- **输入 → 输出：**带退出码的尝试记录、输入变化 → 恢复路线。
- **可以改：**重复失败窗口、可用诊断工具、重试上限；没有新证据就别无限重试。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/checkpoint.json)。
- **来源 / 可选项目：**[R02](skills/jev/references/community.md#r02) · [P03](skills/jev/references/community.md#p03)
- **实验状态：**下方展示合成输入的真实 API 返回；尚未评估这条工作流的端到端效果。

**实际输出** — CSV 解析器连续两次出现同一 UnicodeDecodeError，两次运行间没有改源码。

<!-- receipt: examples-2026-09-20.json#checkpoint -->
```json
{
  "next_step": {"status": "selected", "value": "inspect_input", "probability": 1, "margin": 1},
  "stuck": {"status": "selected", "value": true, "probability": 0.88}
}
```

[原始请求与完整响应](evals/results/examples-2026-09-20.json)

<a id="sc-a06"></a>
<!-- covers: A06 H13 -->
### 3. 检查任务是否真的完成

> 把验收清单逐项对上当前版本的测试和产物回执；没有证据的项目写“未证实”。

- **输入 → 输出：**验收项、产物 ID、测试回执、版本 → 逐项证据支持度。
- **可以改：**完成标准、回执新鲜度、必测项；通过日志必须属于当前版本。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/completion.json)。
- **来源 / 可选项目：**[P03](skills/jev/references/community.md#p03) · [N01](skills/jev/references/community.md#n01)
- **实验状态：**下方展示合成输入的真实 API 返回；尚未评估这条工作流的端到端效果。

**实际输出** — 任务只是入队，尚未执行，metrics 文件不存在，但 agent 声称完成。

<!-- receipt: examples-2026-09-20.json#completion -->
```json
{
  "claim_supported": {"status": "selected", "value": false, "probability": 0.02},
  "next_step": {"status": "selected", "value": "check_job", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/examples-2026-09-20.json)

<a id="sc-a07"></a>
<!-- covers: A07 -->
### 4. 拦住没有证据的“已完成”表述

> 核对这段最终汇报：只排队了任务，是否却写成已经成功运行？保留原始失败记录。

- **输入 → 输出：**拟发汇报、独立执行记录 → 哪些成功表述缺乏支持。
- **可以改：**区分计划、尝试、观察到的结果；先补证据或改措辞。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/completion.json)。
- **来源 / 可选项目：**[P03](skills/jev/references/community.md#p03)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a27"></a>
<!-- covers: A27 -->
### 5. 复盘一次 agent 失败发生在哪里

> 根据编号轨迹，分别选出可疑步骤、相关 agent 和错误类别，输出调查清单而非追责结论。

- **输入 → 输出：**失败轨迹、步骤 ID、错误和参与者 → 步骤／参与者／失败类别。
- **可以改：**错误 taxonomy、证据窗口、unknown 路径；复盘标签不是在线恢复策略的证明。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/checkpoint.json)。
- **来源 / 可选项目：**[P06](skills/jev/references/community.md#p06)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="quality"></a>
## 监督、审查与评测

[核对计划和实际调用是否一致](#sc-a03) · [发现削弱测试、刷通过的修复](#sc-a08) · [检查项目约定和语义规则](#sc-a09) · [给即将执行的动作分风险类](#sc-a10) · [标出工具结果里的诱导指令](#sc-a11) · [给代码审查排优先级](#sc-a12) · [判断工具返回是否真正有用](#sc-a13) · [匿名比较几个候选答案](#sc-h14) · [把 Jev 用作可重复的评测裁判](#sc-judge)

<a id="sc-a03"></a>
<!-- covers: A03 -->
### 6. 核对计划和实际调用是否一致

> 计划是只读检查，拟调用却包含写入参数。请比较目标、范围和效果，标出不一致。

- **输入 → 输出：**眼前计划、完整调用及参数 → 语义上一致或不一致。
- **可以改：**需要比较的字段、作用范围、例外；一致不等于有权限。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[R02](skills/jev/references/community.md#r02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a08"></a>
<!-- covers: A08 -->
### 7. 发现削弱测试、刷通过的修复

> 比较改动前后的断言：把检查改成 assert True 是否绕过了需求，而不是修复行为？

- **输入 → 输出：**原始需求、测试意图、前后 diff → 是否削弱必要检查。
- **可以改：**受保护断言、合法测试改动的例外；标记线索，不判断主观作弊意图。
- **动手：**[jev-code-review](skills/jev-code-review/SKILL.md) · [改写这个模板](skills/jev-code-review/assets/example.json)。
- **来源 / 可选项目：**[P03](skills/jev/references/community.md#p03)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：削弱测试命题为 0.97；不是端到端审查基准。

**实际输出** — 把原断言换成 assert True，只运行了被削弱的测试。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-code-review/assets/example.json -->
```json
{
  "weakens_test": {"status": "selected", "value": true, "probability": 0.97},
  "completion": {"status": "selected", "value": "unsupported", "probability": 1, "margin": 1},
  "review_priority": {"status": "scored", "value": 1.97}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a09"></a>
<!-- covers: A09 -->
### 8. 检查项目约定和语义规则

> 按“业务层不能绕过统一鉴权”这条项目规则检查 diff，每条规则分别判断。

- **输入 → 输出：**明确规则、例外、相关代码 → 可能违反／不违反／证据不足。
- **可以改：**规则文本、适用文件、例外范围；语法类约束仍交给 linter。
- **动手：**[jev-code-review](skills/jev-code-review/SKILL.md) · [改写这个模板](skills/jev-code-review/assets/example.json)。
- **来源 / 可选项目：**[P02](skills/jev/references/community.md#p02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a10"></a>
<!-- covers: A10 -->
### 9. 给即将执行的动作分风险类

> 把这些动作分成只读、可逆本地修改、外部影响、潜在破坏、未知，先给审阅顺序。

- **输入 → 输出：**命令、目标环境、授权证据、回滚事实 → 风险类别。
- **可以改：**环境、影响范围、回滚要求；分类不能覆盖硬权限和确认要求。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[R03](skills/jev/references/community.md#r03) · [P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a11"></a>
<!-- covers: A11 -->
### 10. 标出工具结果里的诱导指令

> 这段网页是否试图让 agent 忽略目标、读取密钥或执行无关动作？把可疑片段列出来。

- **输入 → 输出：**原任务、明确隔离的不可信网页或日志 → 是否有指令重定向企图。
- **可以改：**攻击类别、证据窗口；即使低分也继续把外部内容当作不可信数据。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[P02](skills/jev/references/community.md#p02) · [N02](skills/jev/references/community.md#n02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a12"></a>
<!-- covers: A12 H12 -->
### 11. 给代码审查排优先级

> 按行为变化、潜在缺陷、权限或数据丢失风险给 diff 分块评分，让我先看最值得查的地方。

- **输入 → 输出：**diff 块、文件职责、相关测试 → 分块风险分数和审查顺序。
- **可以改：**风险维度、分数锚点、必审范围；低分不免除必须的安全审查。
- **动手：**[jev-code-review](skills/jev-code-review/SKILL.md) · [改写这个模板](skills/jev-code-review/assets/example.json)。
- **来源 / 可选项目：**[P07](skills/jev/references/community.md#p07) · [Jev Review](https://github.com/devagrawal09/jev-review) · [Blink review](https://blink.review/)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a13"></a>
<!-- covers: A13 -->
### 12. 判断工具返回是否真正有用

> 这个工具虽然退出了，但回复是否为空、缺少必要信息、返回错误，还是明确的政策拒绝？

- **输入 → 输出：**预期结果形状、实际返回、工具状态 → 可用／错误／缺信息／拒绝。
- **可以改：**必需字段、错误类别、重试条件；不要把拒绝当作需要绕过的错误。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/completion.json)。
- **来源 / 可选项目：**[R04](skills/jev/references/community.md#r04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h14"></a>
<!-- covers: H14 -->
### 13. 匿名比较几个候选答案

> 按相同证据给 A/B 答案评分，打乱展示顺序，检查支持度、完整性和是否满足要求。

- **输入 → 输出：**问题、独立证据、匿名候选答案 → 有锚点的评分和分歧。
- **可以改：**评分维度、答案顺序、人工抽查；不能让自评成为唯一真值。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04) · [P09](skills/jev/references/community.md#p09) · [N01](skills/jev/references/community.md#n01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-judge"></a>
<!-- covers: E04 U14 U17 U27 -->
### 14. 把 Jev 用作可重复的评测裁判

> 对保存的 agent 轨迹用固定标准判断，多次重复，分别测与人工标签的一致性、重复性、延迟和成本。

- **输入 → 输出：**轨迹/答案、固定标准 → 类型化标签或分数 → 评测统计。
- **可以改：**裁判标准、留出标签、重复次数、误报漏报代价；重复一致不等于判断正确。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[LangChain judge study](skills/jev/references/community.md#n01) · [OpenRouter author post](https://x.com/OpenRouter/status/2101412965765529853)
- **实验状态：**已记录 LangChain 研究；调研中尚未找到 Ori 的准确实验材料，本次没有新增裁判基准实验。

<a id="routing"></a>
## 路由、委派与上下文

[用户不在时选择还能继续的工作](#sc-a04) · [决定查证、升级模型还是交给人](#sc-a05) · [决定子 agent 的消息何时打断主任务](#sc-a14) · [选择下一步该用哪个工具](#sc-a15) · [按任务选择模型档位](#sc-a16) · [把子任务交给合适的专家](#sc-a17) · [从很多技能里挑需要加载的几个](#sc-a18) · [给搜索或 RAG 结果重新排序](#sc-a19) · [在代码库里找功能入口](#sc-a20) · [压缩工具输出，但保留找回原文的能力](#sc-a21) · [避免重复读取没有变化的信息](#sc-a22) · [根据任务边界和上下文压力决定何时压缩](#sc-compaction)

<a id="sc-a04"></a>
<!-- covers: A04 -->
### 15. 用户不在时选择还能继续的工作

> 我只授权本地修改和测试。下一步在检查日志、运行测试、准备补丁、存档等待中选，不要推送。

- **输入 → 输出：**预授权队列、依赖状态、实际可用动作 → 下一步或等待。
- **可以改：**离线期间授权范围、可逆性、停止条件；用户离线不是追加授权。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/checkpoint.json)。
- **来源 / 可选项目：**[P01](skills/jev/references/community.md#p01) · [P02](skills/jev/references/community.md#p02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a05"></a>
<!-- covers: A05 -->
### 16. 决定查证、升级模型还是交给人

> 根据当前证据，判断应该再读一份日志、交给强推理模型分析，还是缺少只有我能决定的信息。

- **输入 → 输出：**问题、已尝试方法、缺失事实、审阅选项 → 查证／强模型／人工。
- **可以改：**错误代价、缺失信息类型、校准后的升级门槛。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[R01](skills/jev/references/community.md#r01) · [P01](skills/jev/references/community.md#p01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a14"></a>
<!-- covers: A14 -->
### 17. 决定子 agent 的消息何时打断主任务

> 这些子任务汇报中，哪些必须现在处理，哪些可以等检查点，哪些重复或需要核验？

- **输入 → 输出：**子任务目标、汇报、证据 ID、主任务状态 → 即刻处理／延后／重复／核验。
- **可以改：**打断代价、紧急性标准、去重规则；原始汇报仍可检索。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[P02](skills/jev/references/community.md#p02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a15"></a>
<!-- covers: A15 -->
### 18. 选择下一步该用哪个工具

> 根据眼前子目标，在真实可用的搜索、读文件、运行测试、询问用户之间选工具。

- **输入 → 输出：**子目标、观察、实际工具说明和可用性 → 工具 ID 或无匹配。
- **可以改：**工具描述、预算、可用权限；参数由宿主另行构造和校验。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[P01](skills/jev/references/community.md#p01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a16"></a>
<!-- covers: A16 -->
### 19. 按任务选择模型档位

> 把简单改写、多步推理和看图任务分别路由到可用模型；不要只按模型名字大小来选。

- **输入 → 输出：**任务、模态要求、时延成本、能力卡 → 模型档位或无法路由。
- **可以改：**质量底线、延迟、缓存切换成本；最终要测任务结果。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[R04](skills/jev/references/community.md#r04) · [R11](skills/jev/references/community.md#r11) · [N04](skills/jev/references/community.md#n04) · [Jev Codex Router](https://github.com/0xNatoshi/jev-codex-router)
- **实验状态：**下方展示合成输入的真实 API 返回；尚未评估这条工作流的端到端效果。

**实际输出** — 解释并发写入实现的差异；候选是 quick、reasoning、human。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-route/assets/example.json -->
```json
{
  "route": {"status": "selected", "value": "reasoning", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a17"></a>
<!-- covers: A17 -->
### 20. 把子任务交给合适的专家

> 从研究、实现、审查专家或留在主 agent 之间选一个，并明确交接的输入输出。

- **输入 → 输出：**有界子任务、专家职责和排除项 → 专家 ID 或留在本地。
- **可以改：**交接粒度、角色契约、并发限制；是否允许委派由宿主决定。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[R01](skills/jev/references/community.md#r01) · [P01](skills/jev/references/community.md#p01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a18"></a>
<!-- covers: A18 M02 -->
### 21. 从很多技能里挑需要加载的几个

> 根据当前任务为已安装技能打相关性分，优先加载直接有用的；不要跳过必需指令。

- **输入 → 输出：**任务、技能简介、必触发规则 → 可选技能相关性或无合适技能。
- **可以改：**技能描述、适用范围、必需项、兜底；没有合适项时不要硬选第一名。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[R06](skills/jev/references/community.md#r06) · [R08](skills/jev/references/community.md#r08)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a19"></a>
<!-- covers: A19 H23 U07 -->
### 22. 给搜索或 RAG 结果重新排序

> 对“取消订阅后是否保留数据”这个问题，按真正能回答问题而非只含关键词来排段落。

- **输入 → 输出：**查询、已有文档/段落及 ID → 相关性概率、排序或待复核项。
- **可以改：**相关性定义、保留数量、漏检代价；保留原排序与引用来源。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[P09](skills/jev/references/community.md#p09) · [N03](skills/jev/references/community.md#n03)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a20"></a>
<!-- covers: A20 -->
### 23. 在代码库里找功能入口

> 优先用项目代码图，缩小发票生成逻辑的候选路径，再打开源码验证。

- **输入 → 输出：**问题、真实目录/符号/摘要 → 下一处值得读取的路径。
- **可以改：**目录提示、遍历深度、停止证据；路径相关不代表找到了 bug。
- **动手：**[jev-find-code](skills/jev-find-code/SKILL.md) · [改写这个模板](skills/jev-find-code/assets/example.json)。
- **来源 / 可选项目：**[R12](skills/jev/references/community.md#r12) · [Blink path search](https://github.com/ellipsis-dev/blink)
- **实验状态：**下方展示合成输入的真实 API 返回；尚未评估这条工作流的端到端效果。

**实际输出** — 调查重复发票：p1 是 billing/invoices.py，p2 是 ui/theme.py，并附有功能摘要。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-find-code/assets/example.json -->
```json
{
  "next_file": {"status": "selected", "value": "p1", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a21"></a>
<!-- covers: A21 -->
### 24. 压缩工具输出，但保留找回原文的能力

> 给这份长日志按块标记无关、背景、必要证据、关键诊断，先旁路看建议，不直接丢弃。

- **输入 → 输出：**当前子目标、带 ID 的输出块 → 保留建议和相关性分数。
- **可以改：**误删代价、必须保留的错误、原文检索方式；完整输出单独保存。
- **动手：**[jev-context](skills/jev-context/SKILL.md) · [改写这个模板](skills/jev-context/assets/example.json)。
- **来源 / 可选项目：**[R06](skills/jev/references/community.md#r06) · [P02](skills/jev/references/community.md#p02) · [N05](skills/jev/references/community.md#n05) · [winnow / VINNOW lead](https://github.com/GhalebDweikat/winnow)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：需要故障块、不需要主题备注；未执行上下文改写。

**实际输出** — b1 是引号内逗号导致的解析错误，b2 是主题配色帮助；故障调查还没结束。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-context/assets/example.json -->
```json
{
  "b1_needed": {"status": "selected", "value": true, "probability": 0.91},
  "b2_needed": {"status": "selected", "value": false, "probability": 0.03},
  "compact_now": {"status": "selected", "value": "ongoing", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a22"></a>
<!-- covers: A22 -->
### 25. 避免重复读取没有变化的信息

> 检查这次读文件是否与上次参数相同、相关状态未变，而且不会给当前问题带来新信息。

- **输入 → 输出：**拟读操作、上次结果、参数、状态版本 → 是否可能冗余。
- **可以改：**缓存有效期、变化范围；代码证明状态相同，模型只判断语义增益。
- **动手：**[jev-context](skills/jev-context/SKILL.md) · [改写这个模板](skills/jev-context/assets/example.json)。
- **来源 / 可选项目：**[R07](skills/jev/references/community.md#r07)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-compaction"></a>
<!-- covers: M19 U13 -->
### 26. 根据任务边界和上下文压力决定何时压缩

> 现在是阶段结束，还是未完成调查？先给压缩建议，用上下文压力调整策略，别改写模型给出的概率。

- **输入 → 输出：**完成度、工作形态判断 + 宿主统计的上下文用量 → 提示或已授权的压缩。
- **可以改：**压力曲线、冷却时间、误触发代价、提示/自动模式；压缩后是否还保留所需信息要单独测。
- **动手：**[jev-context](skills/jev-context/SKILL.md) · [改写这个模板](skills/jev-context/assets/example.json)。
- **来源 / 可选项目：**[compact-adviser](https://github.com/kunchenguid/compact-adviser)
- **实验状态：**上游描述了小规模/私有标签调试；本仓库上下文例子返回 ongoing，没有实际压缩。

<a id="interaction"></a>
## 浏览器、桌面与交互工具

[决定浏览器下一步点哪里](#sc-a23) · [网页没反应时判断等待还是介入](#sc-a24) · [核验网页动作的真实结果](#sc-a25) · [个人助理把消息交接给下一条工作流](#sc-a26) · [解析智能家居的低风险指令](#sc-h26) · [把观察变成可复用的“当前状态”](#sc-situations) · [边说边判断浏览器操作是否完整](#sc-voice-browser) · [直接选网站工具，少走一长串点击](#sc-webmcp) · [只给一个操作加判断，不必做完整 agent](#sc-primitive) · [让表单根据回答选择下一问](#sc-forms) · [在桌面应用里选择下一步控件](#sc-desktop)

<a id="sc-a23"></a>
<!-- covers: A23 U03 U09 -->
### 27. 决定浏览器下一步点哪里

> 根据最新页面控件，在打开取消政策、滚动、等待或阻塞之间选一步；不要下单。

- **输入 → 输出：**最新 DOM/无障碍文本、目标、真实动作 ID → 下一步操作。
- **可以改：**允许的动作、目标条件、观察新鲜度；浏览器由宿主执行。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[P05](skills/jev/references/community.md#p05) · [Jev Ultrafast](https://github.com/browser-use/jev-ultrafast)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：选出 `open_policy`，未执行浏览器动作；Ultrafast 速度来自作者演示。

**实际输出** — 合成页面：取消政策链接 e12、付款按钮 e13、照片 e14；任务只读。

<!-- receipt: examples-2026-09-20.json#browser-route -->
```json
{
  "next_step": {"status": "selected", "value": "read_policy", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/examples-2026-09-20.json)

**实际输出** — 另一合成页面：政策链接 e1、付款按钮 e2；允许动作是 open_policy、wait、blocked。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-ui/assets/example.json -->
```json
{
  "action": {"status": "selected", "value": "open_policy", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-a24"></a>
<!-- covers: A24 -->
### 28. 网页没反应时判断等待还是介入

> 页面仍在加载还是已经报错？在有限等待、重新观察、检查错误、需要登录/同意之间选路。

- **输入 → 输出：**加载状态、错误、上一动作、等待记录 → 等待／查错／交接。
- **可以改：**超时、重试上限、登录交接；不能据此代替用户同意或绕过验证码。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[P05](skills/jev/references/community.md#p05)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a25"></a>
<!-- covers: A25 -->
### 29. 核验网页动作的真实结果

> 点击之后重新读页面，逐项确认路线、日期和结果是否符合要求，不把点过按钮当成功。

- **输入 → 输出：**最新页面回读、明确清单 → 每项是否被观察支持。
- **可以改：**结果清单、精确字段校验、证据截图或文本；付款等结果需要真实回执。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[P05](skills/jev/references/community.md#p05)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-a26"></a>
<!-- covers: A26 -->
### 30. 个人助理把消息交接给下一条工作流

> 判断这条食谱消息该补抓网页、保存完整食谱、提取日程候选，还是先问清楚。

- **输入 → 输出：**消息、当前任务、后续工具所需数据 → 工作流分支或澄清。
- **可以改：**工作流清单、必需信息、交接格式；外部写入另行授权。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[R01](skills/jev/references/community.md#r01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h26"></a>
<!-- covers: H26 M04 -->
### 31. 解析智能家居的低风险指令

> 根据真实设备清单判断“把客厅灯打开”，如果房间或设备不清楚就问，不猜门锁动作。

- **输入 → 输出：**用户请求、可见设备、允许动作 → 意图、目标和是否完整。
- **可以改：**设备名、同义表达、分支问题；只消费选中意图的答案，锁和危险设备另行控制。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[R09](skills/jev/references/community.md#r09)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-situations"></a>
<!-- covers: M12 -->
### 32. 把观察变成可复用的“当前状态”

> 根据已授权的家居观察判断是否在做饭，输出带时间和过期条件的状态，供低风险自动化读取。

- **输入 → 输出：**观察 → 具名情境概率 → 多条确定性自动化。
- **可以改：**情境定义、刷新事件、有效期、预算；同样可以描述 agent 的待验证状态，不能静默复用旧结论。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[Home Assistant situation layer](skills/jev/references/community.md#p12)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-voice-browser"></a>
<!-- covers: M14 -->
### 33. 边说边判断浏览器操作是否完整

> 结合半句语音转写和最新页面，判断我是不是说完了、指哪个控件，还是应该继续等。

- **输入 → 输出：**语音转写、最新 UI、候选片段 → 意图、目标、完整性 → 操作或等待。
- **可以改：**完整性标准、去抖时间、候选文本、确认规则；识别语音和浏览器执行都是其他工具。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[Voice-browser implementation](skills/jev/references/community.md#p18)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-webmcp"></a>
<!-- covers: M18 U08 -->
### 34. 直接选网站工具，少走一长串点击

> 网站确实提供 search_products 时，先选这个工具，再让文本模型提供参数，校验后执行，不要虚构网站 API。

- **输入 → 输出：**任务、网站实际工具 → 选工具 → 生成参数 → 执行与核验。
- **可以改：**动作粒度、参数来源、UI 兜底、完成标准；生成文本与选择工具分开。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[WindTunnel](https://github.com/nekuda-ai/WindTunnel) · [Benchmark methodology](skills/jev/references/x-intake-2026-09-20.md)
- **实验状态：**上游按每题三次多数成功统计为 49/49 题，实际 141/147 次成功；本仓库未复现，也不是只改接口的严格消融。

<a id="sc-primitive"></a>
<!-- covers: M18 U12 U23 -->
### 35. 只给一个操作加判断，不必做完整 agent

> 只在已有 Stagehand 操作内部选择控件或源文本，外围流程保持不变，不必新建自治 agent。

- **输入 → 输出：**单次观察、操作内候选 → act／observe／extract 内部的局部选择。
- **可以改：**操作边界、目标清单、参数来源、核验方式；选择有效按钮和选择正确下一步不同。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[Stagehand author report](https://x.com/kylejeong/status/2101046888468553855)
- **实验状态：**作者描述；本仓库未安装 Stagehand 集成或测其耗时。

<a id="sc-forms"></a>
<!-- covers: X02 -->
### 36. 让表单根据回答选择下一问

> 根据已填内容和缺失信息，选择下一问、澄清或结束；必填校验仍由代码做。

- **输入 → 输出：**部分表单、允许的问题 → 下一问 ID → 表单渲染器。
- **可以改：**题库、分支规则、完成标准、跳过规则；不能跳过必须的信息收集。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[JevForm report](skills/jev/references/twitter-workflows.md#x02)
- **实验状态：**作者帖子摘录；未检查完整应用代码或复现表单。

<a id="sc-desktop"></a>
<!-- covers: E01 -->
### 37. 在桌面应用里选择下一步控件

> 根据最新桌面观察找到导出窗口；覆盖旧文件前停止，每一步看真实结果。

- **输入 → 输出：**真实控件、允许操作 → 操作/目标 → 宿主 CUA 执行。
- **可以改：**应用动作、预备输入值、停止点、回读核验；需要已有桌面工具。
- **动手：**[jev-ui](skills/jev-ui/SKILL.md) · [改写这个模板](skills/jev-ui/assets/example.json)。
- **来源 / 可选项目：**[Jev Desktop](https://github.com/yikangy873-gif/jev-desktop) · [Setup notes](skills/jev/references/ecosystem.md)
- **实验状态：**上游提供集成样例而非受控加速实验；我们的 UI 冒烟是合成网页，不是这个桌面流程。

<a id="business"></a>
## 消息、客服与日常工作流

[给客服工单分流](#sc-h02) · [按紧急程度排列待办和故障](#sc-h03) · [预筛聊天记录里的未解决问题](#sc-h15) · [识别明确的取消或流失信号](#sc-h16) · [从销售或客服对话整理下一步](#sc-h17) · [给安全事件初步分诊](#sc-h18) · [筛可疑邮件和消息](#sc-h19) · [把联系表单分给正确团队](#sc-h20) · [从消息里整理日程候选](#sc-h24) · [自己写邮件标签和处理规则](#sc-mail-rules) · [按自己的兴趣筛研究流和社交内容](#sc-personal-feed)

<a id="sc-h02"></a>
<!-- covers: H02 U21 -->
### 38. 给客服工单分流

> 把这批工单分成账单、技术、账号访问、安全复核和其他，混合问题单独留给分诊。

- **输入 → 输出：**工单、产品背景、队列定义 → 建议队列或待复核。
- **可以改：**队列职责、多问题处理、例外；每条记录保留独立 ID。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：故障队列、紧急分 1.29/2；未测批量路由。

**实际输出** — 同一订单被扣款两次，但结账仍可用，客户希望当天核查。

<!-- receipt: examples-2026-09-20.json#triage -->
```json
{
  "category": {"status": "selected", "value": "billing", "probability": 1, "margin": 1},
  "needs_human": {"status": "selected", "value": true, "probability": 0.91},
  "urgency": {"status": "scored", "value": 1}
}
```

[原始请求与完整响应](evals/results/examples-2026-09-20.json)

**实际输出** — 所有团队成员导出都报错，明天需要月报。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-triage/assets/example.json -->
```json
{
  "queue": {"status": "selected", "value": "bug", "probability": 1, "margin": 1},
  "urgency": {"status": "scored", "value": 1.29}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-h03"></a>
<!-- covers: H03 -->
### 39. 按紧急程度排列待办和故障

> 区分信息通知、有替代方案、重要工作阻塞、严重进行中影响，不猜测未提供的受影响人数。

- **输入 → 输出：**报告的影响、受阻流程、事件规则 → 有锚点的紧急分数。
- **可以改：**严重性锚点、客户影响、升级期限；已知硬规则仍由代码执行。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04) · [R05](skills/jev/references/community.md#r05)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h15"></a>
<!-- covers: H15 -->
### 40. 预筛聊天记录里的未解决问题

> 找出仍未解决的产品安全投诉，区分用户已经确认解决和只是客服说会处理。

- **输入 → 输出：**授权且脱敏的对话、明确关注点 → 需进一步审阅的会话。
- **可以改：**未解决的定义、上下文范围、漏检代价；低分不是安全证明。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[R05](skills/jev/references/community.md#r05)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h16"></a>
<!-- covers: H16 -->
### 41. 识别明确的取消或流失信号

> 哪些消息表达了“问题未解决，所以我要取消”，哪些只是询问取消规则？

- **输入 → 输出：**消息、必要的相关历史 → 具体取消意向命题概率。
- **可以改：**信号定义、语言差异、跟进方式；不自动改账号或发挽留优惠。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h17"></a>
<!-- covers: H17 -->
### 42. 从销售或客服对话整理下一步

> 按实际承诺选出发资料、安排跟进、技术排查、未承诺或需澄清，给每项附原文。

- **输入 → 输出：**通话记录、承诺、允许的跟进类型 → 待确认行动列表。
- **可以改：**行动清单、承诺证据标准、联系人确认；不要编造承诺。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[R05](skills/jev/references/community.md#r05)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h18"></a>
<!-- covers: H18 -->
### 43. 给安全事件初步分诊

> 按给定事件规则，把报告分为可能账号被接管、服务故障、正常变化或信息不足。

- **输入 → 输出：**脱敏事件、明确升级策略 → 调查类别和待复核项。
- **可以改：**事件类别、已知高风险指示、升级门槛；不能只凭分数封禁账号。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h19"></a>
<!-- covers: H19 -->
### 44. 筛可疑邮件和消息

> 标出要求提供凭据或转账的可疑指令，只看已提供的正文和链接元数据，不打开附件。

- **输入 → 输出：**正文、显示的发送者、可见链接信息 → 可疑命题概率。
- **可以改：**可疑特征、组织规则、复核区间；不输出“保证可以点击”。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h20"></a>
<!-- covers: H20 -->
### 45. 把联系表单分给正确团队

> 把这些咨询分给支持、销售、合作、反馈或其他，不要把陌生但合法的请求直接丢掉。

- **输入 → 输出：**联系表单、咨询类别定义 → 队列标签或草稿处理建议。
- **可以改：**团队边界、垃圾信息规则、未知请求去向；发送回复另行授权。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h24"></a>
<!-- covers: H24 -->
### 46. 从消息里整理日程候选

> 区分新事件、时间变更、只是提醒、非事件和模糊项，先给草稿，不直接发邀请。

- **输入 → 输出：**授权消息、日程相关标准 → 事件候选及类别。
- **可以改：**事件定义、时区、冲突处理；日期由专用代码校验。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[R01](skills/jev/references/community.md#r01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-mail-rules"></a>
<!-- covers: M13 -->
### 47. 自己写邮件标签和处理规则

> 给每封邮件独立判断账单、旅行、需要回复等标签；一封可以命中多个，冲突时先给我看。

- **输入 → 输出：**邮件、可编辑类别 → 多标签命中 → 标签或复核队列。
- **可以改：**标签阈值、优先级、预览模式、允许动作；不能因为多标签命中而反复移动同一封邮件。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[Mail-classifier configuration](skills/jev/references/community.md#p13)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-personal-feed"></a>
<!-- covers: X05 -->
### 48. 按自己的兴趣筛研究流和社交内容

> 按我的研究兴趣给已读取的帖子评分，我可以本地调权重或撤销隐藏，不把喜好当成通用质量。

- **输入 → 输出：**已观察帖子、个人 rubric → 保存判断 → 可撤销排序或隐藏。
- **可以改：**兴趣、排除项、本地权重、更新策略、撤销；问题或证据变了才重新判断。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[Your Signal report](skills/jev/references/twitter-workflows.md#x05)
- **实验状态：**作者帖子摘录；本仓库未安装信息流集成。

<a id="documents"></a>
## 文档、研究与证据

[初筛论文和阅读清单](#sc-h07) · [检查一句主张有没有原文支持](#sc-h08) · [把政策要求做成可复核清单](#sc-h09) · [把合同条款整理给审核人](#sc-h10) · [按品牌和编辑规则检查文案](#sc-h11) · [帮求职者整理岗位要求的证据](#sc-h21) · [选出正确的原始字段值](#sc-spans) · [别把“最像”当成“真的有答案”](#sc-suitability) · [把散乱文本恢复成标题、列表和段落](#sc-structure) · [理解日期表达，再交给代码算日期](#sc-dates) · [复核小模型提取的结构化数据](#sc-extraction-cascade) · [给演讲、访谈、展示做逐段批注](#sc-transcript)

<a id="sc-h07"></a>
<!-- covers: H07 -->
### 49. 初筛论文和阅读清单

> 按“实测 agent 调用工具”筛摘要，区分只提到 agent 和真正做了实验，模糊项留给全文阅读。

- **输入 → 输出：**标题、摘要、纳入条件 → 逐项满足程度与阅读优先级。
- **可以改：**研究范围、纳入排除条件、宁可多留还是少留；摘要不能代替全文评估。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[P09](skills/jev/references/community.md#p09)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h08"></a>
<!-- covers: H08 -->
### 50. 检查一句主张有没有原文支持

> 这段引用真的支持“所有用户都受影响”吗？核对范围、对象和条件，不只看词语相似。

- **输入 → 输出：**准确主张、可定位的原文 → 支持／矛盾／未知。
- **可以改：**支持标准、来源窗口、范围限定；来源支持不等于事实必真。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04) · [P09](skills/jev/references/community.md#p09) · [N02](skills/jev/references/community.md#n02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h09"></a>
<!-- covers: H09 -->
### 51. 把政策要求做成可复核清单

> 对照审核员提供的要求，把条款标成明确涉及、似有冲突、未展示、模糊，并链接原文。

- **输入 → 输出：**当前适用规则、材料摘录 → 审阅矩阵。
- **可以改：**要求版本、例外、证据粒度；由合适的审核人作最终合规判断。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[R05](skills/jev/references/community.md#r05)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h10"></a>
<!-- covers: H10 -->
### 52. 把合同条款整理给审核人

> 把条款分为终止、责任、数据使用、付款和其他，保留条款号，不判断合同是否应该签。

- **输入 → 输出：**条款原文、审核人给定类别 → 分组后的条款清单。
- **可以改：**条款 taxonomy、交叉标签、例外；不能判断法律效力或替人审批。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[R05](skills/jev/references/community.md#r05) · [P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h11"></a>
<!-- covers: H11 -->
### 53. 按品牌和编辑规则检查文案

> 按“不得使用无依据的最强、第一”这条规则检查草稿，区分作者断言与带来源的引述。

- **输入 → 输出：**草稿、明确编辑规则 → 逐条风险标记。
- **可以改：**品牌语气、规则例外、归因要求；模型负责判断，改写另行完成。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[P02](skills/jev/references/community.md#p02) · [P04](skills/jev/references/community.md#p04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h21"></a>
<!-- covers: H21 -->
### 54. 帮求职者整理岗位要求的证据

> 逐条找出我的简历对岗位要求有什么明确、相关或未写出的证据，不替招聘方筛掉人。

- **输入 → 输出：**本人授权的简历、与工作相关的要求 → 证据位置与覆盖情况。
- **可以改：**岗位要求、证据强度、缺失信息；未写出不等于没有能力，不推断受保护属性。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[R08](skills/jev/references/community.md#r08)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-spans"></a>
<!-- covers: M01 -->
### 55. 选出正确的原始字段值

> 从已提取的两个邮箱片段里选账单收件地址，返回片段 ID，让代码复制原值而不是编一个邮箱。

- **输入 → 输出：**候选片段、字段角色 → 片段 ID 或无匹配 → 复制原值。
- **可以改：**字段角色、候选提取方式、格式归一化；候选里没有的值不能凭空找回。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[Official span extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：选出 s2（0.97），同时指出主张与原文矛盾；未测 OCR 或检索。

**实际输出** — s1 是通用邮箱 hello@example.invalid，s2 是账单邮箱 accounts@example.invalid；待核验主张把 s1 当作账单邮箱。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-documents/assets/example.json -->
```json
{
  "source": {"status": "selected", "value": "s2", "probability": 0.97, "margin": 0.94},
  "claim_support": {"status": "selected", "value": "contradicted", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-suitability"></a>
<!-- covers: M02 -->
### 56. 别把“最像”当成“真的有答案”

> 先选最相关段落，再独立判断这里到底有没有答案；几个都不合适时返回无匹配。

- **输入 → 输出：**问题、候选 → 相对最优项 + 独立的是否存在合适答案判断。
- **可以改：**适合标准、片段大小、补检索条件；最高排名不等于足够相关。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[Semantic find](https://docs.typesafe.ai/cookbooks/semantic_find)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-structure"></a>
<!-- covers: M03 -->
### 57. 把散乱文本恢复成标题、列表和段落

> 保留 OCR 原文，先判断哪些相邻行属于同一块，再把块分成标题、列表、普通段落。

- **输入 → 输出：**逐行连续性判断 → 代码合块 → 块类型和属性 → 渲染。
- **可以改：**合行条件、块类型、标题层级、可疑断行；第二遍必须使用第一遍的真实输出。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/document-block.json)。
- **来源 / 可选项目：**[Autoformat cookbook](https://docs.typesafe.ai/cookbooks/autoformat)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-dates"></a>
<!-- covers: M05 -->
### 58. 理解日期表达，再交给代码算日期

> 识别“下周五”的日期语义，用指定基准日和时区交给日历代码算具体日期，不让模型心算。

- **输入 → 输出：**日期表达 → 绝对/相对日期部件 → 确定性日历解析。
- **可以改：**语言、基准时刻、时区、非法日期处理；单位和金额也可采用语义与计算分工。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/span-selection.json)。
- **来源 / 可选项目：**[Date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-extraction-cascade"></a>
<!-- covers: M10 -->
### 59. 复核小模型提取的结构化数据

> 对照发票原文逐字段核验小模型提取结果，区分支持、矛盾和缺失；需要修复时只修问题字段。

- **输入 → 输出：**生成字段、独立原文 → 逐字段判断 → 有界修复或复核。
- **可以改：**字段、原文窗口、错误分类、修复上限；不要反复问到通过为止。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[Structured extraction cascade](https://docs.typesafe.ai/cookbooks/sde_cascade)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-transcript"></a>
<!-- covers: M15 -->
### 60. 给演讲、访谈、展示做逐段批注

> 按我的 rubric 给每轮发言标直接回答、给出证据、含糊主张，保留上下文，再做批注时间线。

- **输入 → 输出：**转写单元、上下文 → 独立 rubric 概率 → 批注或时间线。
- **可以改：**句子或轮次粒度、上下文范围、标签、汇总方式；修辞评价不等于事实核查。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[Jevmeter](skills/jev/references/community.md#p19)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="data"></a>
## 数据、检索与开发工具

[像 grep 一样按语义找日志或笔记](#sc-h01) · [给商品或内容分层归类](#sc-h04) · [发现重复记录或同一实体](#sc-h05) · [给问卷和访谈做多标签编码](#sc-h06) · [给数据集记录做质量侧栏](#sc-h22) · [沿知识图谱或大分类树逐步寻找](#sc-graph) · [给传统机器学习模型制作语义特征](#sc-features) · [JSON 格式正确以后，再检查含义](#sc-semantic-validation) · [从已有命令历史里选合适的建议](#sc-shell-history) · [在普通查询旁边加语义筛选](#sc-semantic-sql) · [让表格列名变成可修改的语义规则](#sc-spreadsheet) · [用市场回放研究决策与过期处理](#sc-market-replay)

<a id="sc-h01"></a>
<!-- covers: H01 -->
### 61. 像 grep 一样按语义找日志或笔记

> 找出真正描述“无法完成结账”的片段，而不只是提到了支付；返回原始片段 ID。

- **输入 → 输出：**编号文本块、具体检索条件 → 逐块匹配概率与候选清单。
- **可以改：**匹配标准、近似案例、复核区间；抽查被排除的片段。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04) · [SemDecide](https://github.com/sharziki/semdecide)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h04"></a>
<!-- covers: H04 M06 -->
### 62. 给商品或内容分层归类

> 先判断这件零件属于紧固件、轴承、密封件还是电气件，再在真实子类中继续分类。

- **输入 → 输出：**描述、分类树、候选定义 → 类别路径或其他。
- **可以改：**分类树、层级深度、描述边界；测试第一层选错造成的连锁误差。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[R05](skills/jev/references/community.md#r05) · [N03](skills/jev/references/community.md#n03) · [N04](skills/jev/references/community.md#n04)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h05"></a>
<!-- covers: H05 -->
### 63. 发现重复记录或同一实体

> 这两条店铺记录是否指向同一实体？比较名称、地址和来源，不要仅凭名字相似就合并。

- **输入 → 输出：**两条记录、身份属性、来源 → 同实体概率和待确认项。
- **可以改：**实体类型、匹配条件、冲突字段；合并仍需确认，保留原记录。
- **动手：**[jev-documents](skills/jev-documents/SKILL.md) · [改写这个模板](skills/jev-documents/assets/example.json)。
- **来源 / 可选项目：**[R01](skills/jev/references/community.md#r01)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h06"></a>
<!-- covers: H06 -->
### 64. 给问卷和访谈做多标签编码

> 按我的 codebook，分别判断每条回答是否谈到价格、缺功能和易用性；允许多个标签共存。

- **输入 → 输出：**单条回答、预定义编码本 → 独立主题标签及概率。
- **可以改：**标签定义、上下文窗口、多人编码分歧；不要强塞进单选。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P04](skills/jev/references/community.md#p04) · [N02](skills/jev/references/community.md#n02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-h22"></a>
<!-- covers: H22 -->
### 65. 给数据集记录做质量侧栏

> 按用途给每条数据评相关性、完整性，再分别标重复和敏感信息疑点；原始数据不删除。

- **输入 → 输出：**单条数据、用途 rubric → 分数和独立检查标签。
- **可以改：**用途、质量锚点、抽查比例；通顺不代表数学正确或许可证合适。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[P08](skills/jev/references/community.md#p08) · [N02](skills/jev/references/community.md#n02)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-graph"></a>
<!-- covers: M06 -->
### 66. 沿知识图谱或大分类树逐步寻找

> 每次只给当前节点的真实邻居，让 Jev 选值得展开的方向，代码限制深度、去重并验证目标。

- **输入 → 输出：**当前节点、邻居描述 → 局部选择 → 有限搜索前沿。
- **可以改：**节点描述、搜索宽度、已访问集合、深度预算；路径分不是校准的正确率。
- **动手：**[jev-find-code](skills/jev-find-code/SKILL.md) · [改写这个模板](skills/jev-find-code/assets/example.json)。
- **来源 / 可选项目：**[Hierarchy method](https://docs.typesafe.ai/cookbooks/hierarchical_classification) · [Graph prototype](skills/jev/references/community.md#p14)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-features"></a>
<!-- covers: M08 -->
### 67. 给传统机器学习模型制作语义特征

> 让生成模型提出评论相关问题，用 Jev 答成数值特征，再训练传统预测器；留出的测试标签不能参与挑问题。

- **输入 → 输出：**候选问题 → 标注记录的数值特征 → 监督学习器 → 开发集误差反馈。
- **可以改：**预测目标、问题族、学习器、数据划分；这是下游特征学习，不是给 Jev 做 RLCD 训练。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[Autoresearch feature discovery](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-semantic-validation"></a>
<!-- covers: M09 -->
### 68. JSON 格式正确以后，再检查含义

> 先通过 schema 校验，再判断描述是否符合所选类别、要求的证据是否真的出现；每条语义规则独立问。

- **输入 → 输出：**结构合法的数据、语义规则 → 每条满足／疑点／未知／不可用。
- **可以改：**字段路径、例外、适用范围、反馈措辞；精确规则继续留在代码里。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[zod-jev](skills/jev/references/community.md#p16) · [JevLint](skills/jev/references/community.md#p17)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-shell-history"></a>
<!-- covers: M11 -->
### 69. 从已有命令历史里选合适的建议

> 根据当前目录和任务，从脱敏后的历史命令里选建议，允许无匹配，不直接执行。

- **输入 → 输出：**已有命令候选、当前上下文 → 命令建议。
- **可以改：**历史窗口、上下文字段、过期结果丢弃；上传前去掉密钥，选中不等于获准执行。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[Shell-history prototype](skills/jev/references/community.md#p15)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-semantic-sql"></a>
<!-- covers: M16 -->
### 70. 在普通查询旁边加语义筛选

> 先用 SQL 缩小近期反馈范围，再让 Jev 筛“未解决的导出失败”；保留行 ID 和判断记录。

- **输入 → 输出：**确定性查询 → 选定字段 → 语义判断 → 过滤、分组或排序。
- **可以改：**字段投影、问题、调用预算、数据外发范围；本仓库没有安装数据库扩展。
- **动手：**[jev-triage](skills/jev-triage/SKILL.md) · [改写这个模板](skills/jev-triage/assets/example.json)。
- **来源 / 可选项目：**[jevQL prototype](skills/jev/references/community.md#p20)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-spreadsheet"></a>
<!-- covers: X04 -->
### 71. 让表格列名变成可修改的语义规则

> 把“是否值得跟进”这个列名变成明确分级标准，再逐行评分；改列名时更新规则并标记旧结果失效。

- **输入 → 输出：**可编辑列含义、行文本 → 评分标准 → 每行分数。
- **可以改：**列语义、分数锚点、行字段、去抖、过期结果处理；每个问题明确对应行 ID。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[Predictive spreadsheet report](skills/jev/references/twitter-workflows.md#x04)
- **实验状态：**作者帖子摘录；本仓库未测试表格 UI 或批量准确率。

<a id="sc-market-replay"></a>
<!-- covers: E05 U05 U15 -->
### 72. 用市场回放研究决策与过期处理

> 仅在 mock 回放中，根据给定快照选择买、卖或不动，丢弃迟到决策，分别记录意图、执行回执和成交。

- **输入 → 输出：**历史/合成快照 → 有界决策 → dry-run 模拟器与回执记录。
- **可以改：**快照时效、截止时间、单请求在途、回放指标；这里只研究流程，不授权真实交易或声称盈利。
- **动手：**[jev-simulation](skills/jev-simulation/SKILL.md) · [改写这个模板](skills/jev-simulation/assets/example.json)。
- **来源 / 可选项目：**[Jev Trader](https://github.com/jarrodwatts/jev-trader) · [Mock/live distinction](skills/jev/references/x-intake-2026-09-20.md)
- **实验状态：**作者演示与 README 的 mock/dry-run 默认模式分别记录；未连接钱包、未运行交易。

<a id="creative"></a>
## 想法、游戏与创作

[让游戏 NPC 从合法动作里作选择](#sc-a28) · [按自己的标准做想法工作坊](#sc-h25) · [给内容选择适合的文档组件](#sc-h28) · [一次测维度，随时改自己的权重](#sc-reweight) · [世界设计、动作选择、视频呈现分开接](#sc-world-video) · [大模型定策略，Jev 高频选局部动作](#sc-strategy) · [给多个聊天角色排发言顺序](#sc-speakers) · [给剧本或播报选择 TTS 语气](#sc-tts) · [让模拟谈判有退出条件，不原地打转](#sc-negotiation) · [按创作要求选图片或视频模型](#sc-creative-route)

<a id="sc-a28"></a>
<!-- covers: A28 H27 -->
### 73. 让游戏 NPC 从合法动作里作选择

> 根据眼前游戏状态和角色目标，在帮助、撤退、交谈、等待中选合法动作，再让模拟器更新状态。

- **输入 → 输出：**可见世界、角色准则、合法动作 → 下一步动作。
- **可以改：**角色性格、目标、行动预算、进度指标；不要假装知道隐藏状态。
- **动手：**[jev-simulation](skills/jev-simulation/SKILL.md) · [改写这个模板](skills/jev-simulation/assets/example.json)。
- **来源 / 可选项目：**[R10](skills/jev/references/community.md#r10) · [X01](skills/jev/references/twitter-workflows.md#x01) · [X03](skills/jev/references/twitter-workflows.md#x03) · [R03](skills/jev/references/community.md#r03)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：检查仓库；未运行状态更新或测胜率。

**实际输出** — 食物还剩两天，桥因风暴关闭，同岸有可到达的仓库；策略是先找本地补给。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev-simulation/assets/example.json -->
```json
{
  "action": {"status": "selected", "value": "inspect_warehouse", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-h25"></a>
<!-- covers: H25 -->
### 74. 按自己的标准做想法工作坊

> 给这个想法的问题清晰度、受众具体度、可测试性分别打分，再设计真正要验证的问题。

- **输入 → 输出：**想法、本人定义的分级标准 → 多维评分。
- **可以改：**维度、可观察锚点、讨论目的；不是生意成功率或投资预测。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[P10](skills/jev/references/community.md#p10)
- **实验状态：**下方展示合成输入的真实 API 返回；尚未评估这条工作流的端到端效果。

**实际输出** — 为忙碌家庭设计离线优先的食材应用；有目标人群，但尚无用户或市场验证。

<!-- receipt: examples-2026-09-20.json#rubric -->
```json
{
  "audience_fit": {"status": "scored", "value": 1.98},
  "validation": {"status": "selected", "value": "untested", "probability": 1, "margin": 1}
}
```

[原始请求与完整响应](evals/results/examples-2026-09-20.json)

<a id="sc-h28"></a>
<!-- covers: H28 -->
### 75. 给内容选择适合的文档组件

> 这段内容应该用比较表、时间线、清单还是普通段落？选已有组件，让代码渲染原内容。

- **输入 → 输出：**结构化内容、受众、组件定义 → 组件 ID。
- **可以改：**组件库、受众、信息结构；选布局不等于生成文案或图片。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/document-block.json)。
- **来源 / 可选项目：**[R12](skills/jev/references/community.md#r12)
- **实验状态：**延伸配方；这个具体场景尚未单独评估。

<a id="sc-reweight"></a>
<!-- covers: M07 -->
### 76. 一次测维度，随时改自己的权重

> 给方案的清晰度、证据、投入分别评分，保存结果；我调权重时用本地代码重排，不重新调用模型。

- **输入 → 输出：**独立维度判断 → 保存特征向量 → 用户权重生成排序。
- **可以改：**维度、锚点、权重、硬排除项；问题含义变了才需要重测，效用分不是概率。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/rubric.json)。
- **来源 / 可选项目：**[Composite configuration](skills/jev/references/community.md#p12) · [Feature experience](skills/jev/references/community.md#n02)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-world-video"></a>
<!-- covers: M17 X01 -->
### 77. 世界设计、动作选择、视频呈现分开接

> 规划模型设计鲸背城市，Jev 选合法动作，模拟器更新世界，渲染工具再把真实轮次结果做成视频。

- **输入 → 输出：**世界规则 → 状态和合法动作 → 决策 → 模拟器 → 可选图像或视频。
- **可以改：**世界规则、角色目标、轮次 ID、呈现方式；视频里桥修好了不代表模拟器真的修好了。
- **动手：**[jev-simulation](skills/jev-simulation/SKILL.md) · [改写这个模板](skills/jev-simulation/assets/example.json)。
- **来源 / 可选项目：**[gokayfem demo](https://x.com/gokayfem/status/2101022590722810271) · [Access and claim notes](skills/jev/references/twitter-workflows.md#x01)
- **实验状态：**作者报告约五分钟生成 264 个片段；不是本仓库复现，也不足以确定恰好调用了 264 次 API。

<a id="sc-strategy"></a>
<!-- covers: M20 X03 U10 U26 -->
### 78. 大模型定策略，Jev 高频选局部动作

> 规划模型给 Pac-Man 一个短期目标，Jev 连续选合法动作；目标完成、条件变化或停滞时再规划。

- **输入 → 输出：**低频策略 → 高频局部动作 → 新状态 → 重规划触发。
- **可以改：**子目标、刷新触发、进度窗口、行动预算；过期子目标不能取代原始目标。
- **动手：**[jev-simulation](skills/jev-simulation/SKILL.md) · [改写这个模板](skills/jev-simulation/assets/example.json)。
- **来源 / 可选项目：**[Pac-Man report](https://x.com/daniel_mac8/status/2100335929273524541) · [Tetris lead](skills/jev/references/twitter-workflows.md#x03)
- **实验状态：**作者演示；本仓库没有复现长程成功率。

<a id="sc-speakers"></a>
<!-- covers: M21 U28 -->
### 79. 给多个聊天角色排发言顺序

> 根据对话状态、角色职责和发言资格选下一位，或者暂停；台词仍让生成模型写。

- **输入 → 输出：**对话状态、允许发言的角色 → 角色/回应模式 ID → 台词生成。
- **可以改：**角色、资格、打断规则、轮次上限、暂停条件；避免机器人彼此无限循环。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/voice-style.json)。
- **来源 / 可选项目：**[Multi-chatbot/TTS report](https://x.com/greenhill_pharm/status/2101492328137711891)
- **实验状态：**本仓库角色/语气联合调用选出 analyst + calm，完整摘录见下一场景。

<a id="sc-tts"></a>
<!-- covers: M21 U28 -->
### 80. 给剧本或播报选择 TTS 语气

> 给这句虚构角色台词选平静、明快、严肃或中性语气，再映射到已有 TTS 预设。

- **输入 → 输出：**剧本、表达 rubric → 语气标签 → TTS 预设；声音由其他工具生成。
- **可以改：**语气标签、声线映射、平滑切换、中性兜底；不是对真人内心情绪的诊断。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/voice-style.json)。
- **来源 / 可选项目：**[Creator report](https://x.com/greenhill_pharm/status/2101492328137711891)
- **实验状态：**[真实合成示例](evals/SCENARIO_EXAMPLES.md)：analyst + calm；没有生成语音。

**实际输出** — 虚构播客里主持人请分析员解释相互矛盾的证据，选择下一位角色和表达语气。

<!-- receipt: scenario-smoke-2026-09-20.json#skills/jev/assets/voice-style.json -->
```json
{
  "speaker": {"status": "selected", "value": "analyst", "probability": 1, "margin": 1},
  "delivery": {"status": "selected", "value": "calm", "probability": 0.98, "margin": 0.96}
}
```

[原始请求与完整响应](evals/results/scenario-smoke-2026-09-20.json)

<a id="sc-negotiation"></a>
<!-- covers: X06 -->
### 81. 让模拟谈判有退出条件，不原地打转

> 在 Catan 式模拟谈判里从接受、还价、拒绝、跳过中选合法动作，超过无进展预算就退出。

- **输入 → 输出：**报价历史、合法选项 → 局部回应 → 宿主检查进度与死锁。
- **可以改：**谈判预算、效用标准、跳过/终止动作、进度定义；局部合理不保证集体推进。
- **动手：**[jev-simulation](skills/jev-simulation/SKILL.md) · [改写这个模板](skills/jev-simulation/assets/example.json)。
- **来源 / 可选项目：**[Catan failure report](skills/jev/references/twitter-workflows.md#x06)
- **实验状态：**来源报告了谈判停滞；这里是根据失败设计的改编，不是已经证明有效的修复。

<a id="sc-creative-route"></a>
<!-- covers: X07 -->
### 82. 按创作要求选图片或视频模型

> 根据图片/视频类型、编辑要求、尺寸、预算，从实际可用的生成器里选一个，再单独调用。

- **输入 → 输出：**创作需求、当前能力卡 → 生成器 ID 或无匹配。
- **可以改：**媒介、编辑能力、延迟、预算、成品评价标准；不能只测路由置信度。
- **动手：**[jev-route](skills/jev-route/SKILL.md) · [改写这个模板](skills/jev-route/assets/example.json)。
- **来源 / 可选项目：**[Creative-model routing demo](skills/jev/references/twitter-workflows.md#x07)
- **实验状态：**作者帖子摘录；没有复现生成或成品质量对照。

<a id="building"></a>
## 制作与接入自己的工具

[用一句需求生成可编辑的判断问题](#sc-compile) · [通过 MCP 给现有 agent 增加判断工具](#sc-mcp) · [边改例子边学，再让 agent 写新例子](#sc-playground)

<a id="sc-compile"></a>
<!-- covers: M22 -->
### 83. 用一句需求生成可编辑的判断问题

> 把“找出当前阻碍使用的反馈”编成 typed questions 和标准，先给边界例子检查，再逐条应用。

- **输入 → 输出：**用户需求 → 模型起草问题 → schema 和标准复核 → Jev 逐条判断。
- **可以改：**问题含义、标签、行 ID、标准版本、结果接收者；这是工作流，不是本 CLI 已有 compiler 命令。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/semantic-rules.json)。
- **来源 / 可选项目：**[OpenRouter question compiler](https://openrouter.ai/labs/jev/compile)
- **实验状态：**来源描述了这种方法；这里的改编尚未运行。

<a id="sc-mcp"></a>
<!-- covers: E02 -->
### 84. 通过 MCP 给现有 agent 增加判断工具

> 选择一个通用 evaluate 工具，或者 classify/verify/rerank 这类命名工具，用自己的标准和复核路径。

- **输入 → 输出：**Agent 工具调用、状态和问题 → 类型化判断 → 已有宿主流程。
- **可以改：**工具形态、模型版本、供应商、结果消费策略；MCP 与文件夹 skill 分别安装。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/triage.json)。
- **来源 / 可选项目：**[TypeSafe MCP](https://github.com/itsmostafa/typesafe-mcp) · [Jev MCP](https://github.com/jkudish/jev-mcp)
- **实验状态：**检查到的两个版本均支持 OpenRouter，本仓库未安装；先检查会改配置或存密钥的安装助手。

<a id="sc-playground"></a>
<!-- covers: E03 U29 -->
### 85. 边改例子边学，再让 agent 写新例子

> 读一个 playground 例子的 state、questions、替换输入和消费者，再让 coding agent 照这个结构写自己的用法。

- **输入 → 输出：**可编辑例子 → 替换输入 → 检查判断与下游行为。
- **可以改：**任务、标准、边界输入、live/mock 模式、消费者；页面演示不自动等于模型调用。
- **动手：**[jev](skills/jev/SKILL.md) · [改写这个模板](skills/jev/assets/triage.json)。
- **来源 / 可选项目：**[TypeSafe AI Playground](https://github.com/TypeSafeAI/typesafe-playground) · [Jev Explained](https://github.com/davila7/jev-explained)
- **实验状态：**已读原始 README，未运行界面；TypeSafe AI Playground 区分真实调用、mock 和本地求解器。

## 让概率真正有用

“自动处理 / 强模型复核 / 交给人”是**可以定制的策略**，不是通用的 0.9/0.7 规则。
先明确使用的是哪个答案的概率，在留出的标注数据上检验，再按错误代价选阈值。
`score` 不是概率，置信度也不等于执行权限。[校准指南](skills/jev/references/calibration.md)。

每个场景都保留未知路径、读取最新状态，并在执行后核验结果。
Jev 本身不浏览、不执行工具，也不生成自由文本。判断输入会发送给 OpenRouter 及其供应商，建议先用合成数据尝试。

<a id="experiments"></a>
## 可以查看的实验

- [Agent 使用前后对照](evals/RESULTS.md)：12 组，baseline 12/12，固定检查点 10/12；是该接入策略的小规模负面结果。
- [决策/校准试验](evals/CALIBRATION_RESULTS.md)：160 题命中 136 题；置信度 ≥0.9 的 100 题仍错了 8 题。
- [9 个场景 API 示例](evals/SCENARIO_EXAMPLES.md)：记录了 8 个场景技能和声音编排的实际返回，没有执行宿主动作。
- [此前的 5 个真实 API 示例](evals/results/examples-2026-09-20.json)：保留请求/响应，是冒烟回执，不是场景准确率测试。
- [验证与复现说明](docs/validation.md)：分别记录打包检查、离线运行，以及尚未验证的宿主边界。

## 更多资料 · 致谢

本合集参考了这些 awesome 项目的线索整理：
[Anil-matcha/awesome-jev-by-typesafe](https://github.com/Anil-matcha/awesome-jev-by-typesafe)、
[cobanov/awesome-jev](https://github.com/cobanov/awesome-jev)、
[yibie/awesome-jev](https://github.com/yibie/awesome-jev)、
[yzfly/awesome-jev-zh](https://github.com/yzfly/awesome-jev-zh)、
[hellogumbo/awesome-jev](https://github.com/hellogumbo/awesome-jev)。

继续探索：[固定版本的项目调研](skills/jev/references/ecosystem.md) ·
[Reddit、GitHub 等平台使用记录](skills/jev/references/community.md) ·
[你提供的 29 条 X 分享及后续核验](skills/jev/references/x-intake-2026-09-20.md) ·
[56 个 agent / 人工场景](skills/jev/references/index.md)。

也受到[官方 Jev skill](https://docs.typesafe.ai/agent-skill)的启发。

特别感谢 [LINUX DO](https://linux.do/?tl=en)。

[MIT](LICENSE)，外链项目保留各自许可证。
