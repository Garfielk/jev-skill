# Jev Skill

**给 agent 和人用的决策工具箱。** 通过 OpenRouter 调用 [TypeSafe Jev](https://typesafe.ai/)，
对当前情况分类、从候选项中选择下一步、按明确标准评分，而不是生成更多文字。

[English](README.md) · [场景目录](skills/jev/references/index.md) · [社区与作者实践](skills/jev/references/community.md) · [对照实验](evals/README.md)

## 可以做什么

| Agent 使用 | 人工使用 |
|---|---|
| 判断任务跑偏、重复失败及恢复路径 | 分类消息、日志、文档和反馈 |
| 选择工具、skill、模型或子 agent | 筛选论文、标注数据、匹配实体 |
| 根据 browser 观察选择下一步 | 按 rubric 评价创意、设计和内容 |
| 用真实证据核查“已完成”的声明 | 将政策例外与模糊情况转交复核 |

[56 个 Reference 场景](skills/jev/references/index.md) 提供具体输入、问题和注意事项，
并区分社区实际报告的用法与我们提出的应用延伸。

## 安装 skill

```bash
npx skills add wuyoscar/jev-skill --skill jev
export OPENROUTER_API_KEY="your-key"
```

在安装器中选择 **Codex、Claude Code 或 OpenCode**。需要 Python 3.10+；
自带脚本无第三方运行时依赖。必要时重启 agent，并确保它的进程能读取环境变量。

可以直接说：“用 Jev 检查任务为什么卡住，从现有工具中选下一步。”
或者：“用 Jev 分类这些工单，把不确定的留给人工。”[手动安装](docs/installation.md)。

## 直接作为工具使用

```bash
uv tool install git+https://github.com/wuyoscar/jev-skill.git@v0.1.0
```

创建带类别说明的 `labels.json`：

```json
{"billing":"Charges, invoices or refunds","bug":"Broken software behavior","other":"Unclear or no matching category"}
```

```bash
jev-decide classify --text "I was charged twice" --criteria labels.json
jev-decide decide request.json --dry-run  # 只校验，不付费调用
jev-decide decide request.json            # state + choice/noul/score 问题
```

输出 JSON，保留标签、不确定状态、原始回答、耗时和服务商返回的用量。
退出码 `0`：已分类／评分；`2`：需要复核；`1`：错误。
[请求示例](skills/jev/assets) · [API 文档](skills/jev/references/api.md)

## 边界

Jev 不会自行执行工具或操作 browser；宿主 agent 提供观察并执行获准的动作。
Skill 是**行为指引，不是强制拦截 hook**。Jev 可能判断错误或受输入操纵，
不能代替授权、确定性校验和人工复核。提交的文本／JSON 会发往 OpenRouter 及其服务商。
本项目开源的是集成工具，**不是 Jev 模型权重**。

## 用实验说话

[配对对照实验](evals/README.md) 使用相同 agent，比较有／无 Jev 检查点建议时的表现，
以模拟环境的确定性最终状态验收。[12 组配对试验](evals/RESULTS.md) 中，基线完成
**12/12**，加入固定 Jev 检查点后完成 **10/12**，费用更高。另有 5 个真实 Jev 示例通过。
建议按需使用；这次小实验**没有证明 agent 整体表现提升**。

参考了 [官方 Jev skill](https://docs.typesafe.ai/agent-skill)、
[JevRouter](https://github.com/BillionsBobby/JevRouter) 和社区实践。
我们的重点是场景库、agent／人工两类用法，以及透明测试。
独立项目，与 TypeSafe、OpenRouter 无隶属关系。[MIT](LICENSE)。
