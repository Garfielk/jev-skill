# Awesome Jev Skills

**Jev 具体能做什么：可修改的例子、可安装的技能，以及值得参考的社区项目。**

Jev 负责选择、分类和评分，agent 负责提供上下文和执行。
既可以把它接进 agent，也可以自己拿来处理消息、文档和需要判断的事情。

[English](README.md) · [安装](docs/installation.md) · [社区项目](skills/jev/references/ecosystem.md) · [更多场景](skills/jev/references/index.md)

## 挑一个场景试试

[消息分流](#triage) · [筛选记录](#filter) · [读文档](#documents) ·
[浏览器操作](#browser) · [桌面操作](#desktop) · [工具与模型路由](#routing) ·
[管理上下文](#context) · [代码审查](#review) · [找代码](#search) ·
[让 agent 脱困](#checkpoint) · [游戏与故事](#simulation) · [对话与声音](#voices) ·
[接入 MCP](#mcp) · [定制自己的工具](#custom)

**本仓库提供：**8 个场景技能、1 个通用 `jev` 技能、可修改的 JSON 示例，以及共用的 OpenRouter CLI。
**外链项目：**可以另选的社区方案，不是已经捆绑接入的功能；请先看它们各自的安装要求。

### 从本地仓库开始

公开发布尚未完成；以下命令在下载后的仓库目录中使用。
需要 Python 3.10+、[uv](https://docs.astral.sh/uv/) 和 Node/npm。

```bash
uv tool install .
npx skills add . --skill jev-triage
export OPENROUTER_API_KEY="your-key"
jev-decide decide skills/jev-triage/assets/example.json --dry-run
```

安装器中选择 Codex、Claude Code 或 OpenCode。把 `jev-triage` 换成下文需要的技能，
然后让 agent 使用它。自己直接用也可以：修改 JSON，去掉 `--dry-run` 就会调用 Jev（产生费用）。
[其他安装方式](docs/installation.md)。

**示例状态：**8 个场景示例与声音示例均完成了[真实 API 冒烟调用](evals/SCENARIO_EXAMPLES.md)，
输入是合成数据，不代表真实任务已完成。社区演示默认为作者报告，
而非本仓库复现。[实际实验](#experiments)也保留了负面结果。

<a id="triage"></a>
## 1. 给邮件、消息或客服工单分流

> 用 jev-triage 把这些工单分成账单、故障、使用咨询和其他。标出紧急阻塞和不确定项，
> 先给我看结果表，不要直接修改邮箱。

- **怎么接：**消息 + 你的分类标准 → 队列、紧急程度、待复核状态。
- **怎么改：**VIP 客户、截止时间、团队归属，或者让一条消息拥有多个标签。
- **直接开始：**[jev-triage 技能](skills/jev-triage/SKILL.md) · [工单 example](skills/jev-triage/assets/example.json)。
- **也可以选：**[Jev MCP](https://github.com/jkudish/jev-mcp) 的 classify 工具，或方便写脚本的 [SemDecide](https://github.com/sharziki/semdecide)。
- **实验情况：**我们[此前的 triage 请求](skills/jev/assets/triage.json)通过了真实 API 冒烟测试；没有测试批量邮箱准确率或写入操作。

<a id="filter"></a>
## 2. 用一句自然语言筛选记录

> 用 jev-triage 找出“现在已经阻碍使用”的反馈，不要把功能愿望混进来。
> 保留原始 ID，把边界情况单独列给我。

- **怎么接：**单条记录 + 语义规则 → 保留、跳过或复核。精确日期、计数仍交给代码。
- **怎么改：**论文初筛、用户反馈、日志分类、数据集收录标准。
- **直接开始：**[记录分类技能](skills/jev-triage/SKILL.md) · [可改写的记录 example](skills/jev-triage/assets/example.json) · [独立规则判断](skills/jev/assets/semantic-rules.json)。
- **也可以选：**[SemDecide](https://github.com/sharziki/semdecide) 提供 JSONL 流式筛选。按其文档另外安装后，可以用 `cat tickets.jsonl | semdecide filter 'The customer reports a current service blocker' --field text`。
- **实验情况：**已检查原始说明，未复现。本仓库 CLI 处理判断请求，不包含 SemDecide 的流式 filter 命令。

<a id="documents"></a>
## 3. 找出正确的条款、字段或证据段落

> 用 jev-documents 从这些已提取的文本片段里选出账单邮箱，再检查段落是否支持这条主张。
> 返回原文，不要自己改写一个答案。

- **怎么接：**原文 + 带 ID 的候选片段 → 选中片段；主张 + 证据 → 支持、矛盾或未知。
- **怎么改：**发票字段、合同条款、引文核验、研究证据。扫描件先用宿主的 OCR 工具处理。
- **直接开始：**[jev-documents 技能](skills/jev-documents/SKILL.md) · [片段选择与核验 example](skills/jev-documents/assets/example.json)。
- **也可以选：**[Jev MCP](https://github.com/jkudish/jev-mcp) 的提取/核验工具，或 [TypeSafe AI Playground](https://github.com/TypeSafeAI/typesafe-playground) 的文档例子。
- **实验情况：**[真实示例调用](evals/SCENARIO_EXAMPLES.md)选出了账单片段，并指出主张与原文矛盾；没有测试检索或 OCR。

<a id="browser"></a>
## 4. 决定浏览器下一步点哪里

> 用 jev-ui 查这家酒店的取消政策。先观察页面，再选择相关链接，用浏览器工具打开，
> 最后核对政策原文。不要下单。

- **怎么接：**最新 DOM/无障碍文本 + 可用动作 → 一个动作 → 宿主浏览器执行 → 重新观察。
- **怎么改：**网页导航、表单步骤、商品比较、只读调研。需要自由输入时，再让文本模型生成内容。
- **直接开始：**[jev-ui 技能](skills/jev-ui/SKILL.md) · [可见控件 example](skills/jev-ui/assets/example.json)。
- **也可以选：**[Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) 的浏览器循环，或使用网站工具接口的 [WindTunnel/WebMCP](https://github.com/nekuda-ai/WindTunnel)。
- **实验情况：**Ultrafast 的快速航班搜索演示与 WindTunnel 的任务测试不是同一套配置，见[方法说明](skills/jev/references/x-intake-2026-09-20.md)。本技能需要宿主已经有浏览器工具。

<a id="desktop"></a>
## 5. 在桌面应用里选择控件

> 用 jev-ui 配合桌面工具找到导出窗口。只选择当前观察里可见的控件；
> 如果要覆盖已有文件，先停下来。

- **怎么接：**应用控件观察 + 允许的操作 → 操作和目标 → 宿主执行、核验。
- **怎么改：**具体应用的动作列表、预先准备的输入值、明确的停止条件。
- **直接开始：**[同一个 UI 技能](skills/jev-ui/SKILL.md) · [改写这个带 ID 的控件 example](skills/jev-ui/assets/example.json)。
- **也可以选：**[Jev Desktop](https://github.com/yikangy873-gif/jev-desktop)，它接入已有的 Codex Computer Use 运行环境。
- **实验情况：**上游报告了集成样例，不是受控加速实验。安装本技能不会安装桌面控制能力，也不会授予操作权限。

<a id="routing"></a>
## 6. 为每一步选工具、专家或模型

> 用 jev-route 根据这些任务和真实能力说明，在快速模型、推理模型和人工复核之间选路。
> 先给建议，不要修改我的宿主配置。

- **怎么接：**任务 + 实际能力/成本清单 → 路由选择，或没有适合的选项。
- **怎么改：**延迟预算、工具描述、技能目录、审核角色、升级策略。
- **直接开始：**[jev-route 技能](skills/jev-route/SKILL.md) · [模型路由 example](skills/jev-route/assets/example.json)。
- **也可以选：**[Jev Codex Router](https://github.com/0xNatoshi/jev-codex-router)，在作者已有的 macOS Codex Router 服务上加入路由。
- **实验情况：**它的回测对历史 token 重新计价，并非控制任务质量后的重跑。本技能输出建议，不替你切换宿主配置。

<a id="context"></a>
## 7. 保留有用上下文，判断何时压缩

> 用 jev-context 做建议：哪些工具输出块与当前 bug 有关？现在是不是安全的压缩节点？
> 先给判断，保留可以找回的完整原始输出。

- **怎么接：**目标 + 带 ID 的输出块 + 未解决事项 → 相关性判断，再单独判断是否适合压缩。
- **怎么改：**上下文压力、误删代价、必须保留的错误信息、原文检索方式。先旁路记录，不直接删除。
- **直接开始：**[jev-context 技能](skills/jev-context/SKILL.md) · [保留/压缩 example](skills/jev-context/assets/example.json)。
- **也可以选：**[winnow](https://github.com/GhalebDweikat/winnow) 筛选工具结果；[compact-adviser](https://github.com/kunchenguid/compact-adviser) 寻找适合压缩的任务节点。
- **实验情况：**上游有小规模标注评估，本仓库未复现。“VINNOW”暂按 winnow 收录，见[项目说明](skills/jev/references/ecosystem.md)。

<a id="review"></a>
## 8. 排代码审查优先级，发现可疑修复

> 用 jev-code-review 看这份 diff。标出“没有修行为、只是削弱测试”的变化，
> 排出审查线索并定位证据；真正的测试另行运行。

- **怎么接：**diff + 需求 + 测试回执 → 风险信号、审查顺序 → 阅读和验证。
- **怎么改：**权限、数据丢失、并发、测试完整性，或项目特有的不变量。
- **直接开始：**[jev-code-review 技能](skills/jev-code-review/SKILL.md) · [弱化测试 example](skills/jev-code-review/assets/example.json)。
- **也可以选：**[Jev Review](https://github.com/devagrawal09/jev-review) 的分阶段审查与面板；[blink.review](https://blink.review) 展示了代码审查 CLI。
- **实验情况：**本次检查原仓库/落地页，未运行。风险标记是线索，不是已证实的漏洞，也不能替代测试。

<a id="search"></a>
## 9. 在大仓库里找一段功能在哪里

> 用 jev-find-code 缩小“发票在哪里生成”的范围。优先用项目代码图，
> 选择可能的路径，再打开源码确认，不要凭文件名直接修改。

- **怎么接：**任务 + 真实代码图/路径候选 → 下一处值得查看的位置 → 源码核对。
- **怎么改：**命名习惯、目录提示、搜索深度、什么证据才算找到。
- **直接开始：**[jev-find-code 技能](skills/jev-find-code/SKILL.md) · [路径选择 example](skills/jev-find-code/assets/example.json)。
- **也可以选：**[ellipsis-dev/blink](https://github.com/ellipsis-dev/blink) 用加权搜索者探索路径。按其文档安装后：`./blink "where are invoices generated?" /path/to/repo -r`。
- **实验情况：**已读上游，未运行。这个 Blink 仓库做路径搜索，与上面的审查入口分开记录；文件名相关不等于理解了代码。

<a id="checkpoint"></a>
## 10. 让 agent 脱困，或认清任务还没完成

> 用 Jev 对照我的目标检查最近三次失败。在继续查证、修改计划、重试或暂停之间选一步。
> 宣布完成前检查真实回执。

- **怎么接：**目标 + 最近动作和结果 + 候选恢复步骤 → 检查点建议。
- **怎么改：**重复失败的定义、剩余预算、完成证据、用户离线时允许继续的工作。
- **直接开始：**[通用 jev 技能](skills/jev/SKILL.md) · [恢复 example](skills/jev/assets/checkpoint.json) · [完成核验 example](skills/jev/assets/completion.json)。
- **也可以选：**[Jev MCP](https://github.com/jkudish/jev-mcp) 的决策/核验工具。
- **实验情况：**我们的 [12 组配对实验](evals/RESULTS.md)是 **baseline 12/12，固定 Jev 检查点 10/12**，后者成本更高。应该选择性调用，不保证外挂后更强。

<a id="simulation"></a>
## 11. 驱动 NPC、决策游戏或分支故事

> 用 jev-simulation 跑这个岛屿小镇游戏。规划模型制定策略，Jev 从合法动作中选一步，
> 模拟器更新世界。先记录结果，需要时再渲染成场景。

- **怎么接：**策略 + 当前世界 + 合法动作 → 动作选择 → 确定性的状态更新。渲染是独立可选步骤。
- **怎么改：**目标、NPC 角色、合法行动、资源、重规划条件、剧情分支。
- **直接开始：**[jev-simulation 技能](skills/jev-simulation/SKILL.md) · [岛屿小镇 example](skills/jev-simulation/assets/example.json)。
- **也可以选：**[世界设计/决策/视频演示和 Pac-Man 分享](skills/jev/references/twitter-workflows.md)展示了规划与行动的分工；[Playground](https://github.com/TypeSafeAI/typesafe-playground)也有交互例子。
- **实验情况：**[真实示例调用](evals/SCENARIO_EXAMPLES.md)选择了检查仓库，没有运行模拟器状态更新。社交平台的吞吐量仍只是作者报告。

<a id="voices"></a>
## 12. 编排聊天轮次，选择 TTS 声音风格

> 用 Jev 为这段虚构对话选择下一位允许发言的角色和表达风格。
> 台词由语言模型写，声音由 TTS 引擎生成。

- **怎么接：**对话状态 + 角色/风格选项 → 对应 ID → 对话或 TTS 工具。
- **怎么改：**轮次规则、已有声线、表达语气、打断规则，或暂不发言选项。
- **直接开始：**[通用 jev 技能](skills/jev/SKILL.md) · [角色/语气 example](skills/jev/assets/voice-style.json)。
- **也可以选：**创作者分享的[多聊天机器人编排、七类情感控制 TTS](skills/jev/references/x-intake-2026-09-20.md)启发了这个改编。
- **实验情况：**[真实示例调用](evals/SCENARIO_EXAMPLES.md)选出 analyst + calm，没有运行 TTS。标签是我们的改编，不是原作者配置，也不诊断人的真实情绪。

<a id="mcp"></a>
## 13. 给支持 MCP 的 agent 增加判断工具

> 用判断工具给这个请求分类，检查证据，再从我已有的工具中选下一步。
> 不确定项单独保留。

- **几选一：**[TypeSafe MCP](https://github.com/itsmostafa/typesafe-mcp) 提供通用 `evaluate` 工具；[Jev MCP](https://github.com/jkudish/jev-mcp) 提供 classify、verify、rerank 等命名工具。检查到的版本都支持 OpenRouter。
- **怎么改：**判断标准、固定模型版本、每种输出接到哪里。MCP 与文件夹式 skill 是不同的安装入口。
- **不装 MCP 也能开始：**[通用技能](skills/jev/SKILL.md) · [原生请求 example](skills/jev/assets/triage.json)。本仓库 CLI 不依赖 MCP server。
- **安装/实验情况：**见[供应商和安装说明](skills/jev/references/ecosystem.md)。本次仅检查源文档，没有安装这两个服务；不要直接运行会改客户端配置、保存密钥的安装助手。

<a id="custom"></a>
## 14. 把你自己的判断标准变成工具

> 帮我用 Jev 做一个研究想法筛选工具。先定义需要的证据、可改的标准、未知选项，
> 再准备一小批带标签的例子，验证后才自动化。

- **怎么接：**你的任务 → 证据 → `choice`（选一路）、`noul`（判断命题）或 `score`（按有描述的等级评分）→ 接收结果的人或工具。
- **怎么改：**个人评分表、政策检查、语义特征、重排、实体匹配、结构化标注，都不是固定菜单。
- **直接开始：**[通用技能](skills/jev/SKILL.md) · [评分 example](skills/jev/assets/rubric.json) · [定制指南](skills/jev/references/customization.md) · [22 种连接方法](skills/jev/references/implementation-patterns.md)。
- **也可以选：**[TypeSafe AI Playground](https://github.com/TypeSafeAI/typesafe-playground) 是独立社区项目，不是 TypeSafe 官方产品；其中区分了真实 Jev、mock 和本地求解器。
- **实验情况：**此前的评分请求通过了真实调用冒烟测试，但不代表符合你的偏好。先用人工标签测分歧，再决定如何接入。

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
本项目独立维护，与 TypeSafe、OpenRouter 无隶属关系；开源的是集成与用法，不是 Jev 模型权重。
[MIT](LICENSE)，外链项目保留各自许可证。
