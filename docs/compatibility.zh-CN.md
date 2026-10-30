# 工具适配

[English](compatibility.md) · [简体中文](compatibility.zh-CN.md) · [返回 README](../README.zh-CN.md)

以下以 2026-10-30 查阅的官方文档为依据。已完成入口、相对路径和配置的静态核对；尚未逐工具启动新会话验证自动加载、执行和写回。表中的“导入”与“读取指令”分别表示工具原生加载和由 Agent 使用文件工具读取，不将两者等同。

| 工具 | 本项目提供的入口 | 加载方式与限制 | 官方依据 |
| --- | --- | --- | --- |
| OpenAI Codex | `AGENTS.md` | 发现入口后按指令读取核心；受指令发现范围和实际权限约束 | [OpenAI Docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Claude Code | `CLAUDE.md` | 使用 `@./relay.md` 原生导入，避免依赖 AGENTS 的版本及回退规则 | [Memory](https://code.claude.com/docs/en/memory) |
| Gemini CLI | `GEMINI.md` | 使用 `@./relay.md` 原生导入 | [Context files](https://geminicli.com/docs/cli/gemini-md/) |
| Qwen Code | `QWEN.md` | 使用 `@./relay.md` 文件引用；新版本也可能同时加载 AGENTS | [Memory](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/) |
| GitHub Copilot | `.github/copilot-instructions.md`、`AGENTS.md` | 按指令读取核心；各客户端、Agent 与代码审查的指令支持和文件读取能力不同 | [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) |
| Cursor | `AGENTS.md` | 项目级入口，按指令读取核心 | [Rules](https://cursor.com/docs/rules) |
| Cline | `AGENTS.md`、`.clinerules/relay.md` | 提供标准入口及原生规则；在 Rules 面板确认已启用，重复入口不重复执行初始化 | [Cline Rules](https://github.com/cline/cline/blob/main/docs/customization/cline-rules.mdx) |
| Roo Code | `.roo/rules/relay.md` | 使用原生工作区规则；AGENTS 支持受设置影响 | [Custom instructions](https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/features/custom-instructions.md) |
| Continue | `.continue/rules/relay.md` | `alwaysApply: true`；需要可读取文件的 Agent 模式，自动补全不包含这些规则 | [Rules](https://docs.continue.dev/customize/deep-dives/rules) |
| TRAE | `.trae/rules/project_rules.md` | 提供项目规则并声明 alwaysApply；官方规则页正文未能完整读取，文件名参照官方文章，当前版本目录与激活方式仍需实测确认 | [Rules](https://docs.trae.ai/ide/rules)、[官方文章](https://www.trae.ai/blog/trae_tutorial_0825) |
| OpenCode | `opencode.json`、`AGENTS.md` | `instructions` 原生加载核心；AGENTS 同时作为共享入口 | [Rules](https://opencode.ai/docs/rules/) |
| Aider | `.aider.conf.yml` | `read` 原生加载核心；启用本地自动提交，独立记忆仓库由 Agent 按核心约定管理 | [YAML config](https://aider.chat/docs/config/aider_conf.html) |
| Kiro | `AGENTS.md` | 标准入口；自定义 Agent 可能需显式配置 resources | [Steering](https://kiro.dev/docs/steering/) |
| JetBrains Junie | `AGENTS.md`、`.junie/guidelines.md` | 标准入口加旧版 guidelines 回退；自定义 Guidelines path 可能改变加载来源 | [Guidelines](https://junie.jetbrains.com/docs/guidelines-and-memory.html) |
| Google Antigravity | `AGENTS.md`、`GEMINI.md` | 使用工具支持的工作区入口；需要确认具体产品形态的加载来源 | [Rules](https://antigravity.google/docs/rules/) |
| Qoder IDE | `AGENTS.md` | 官方声明自动识别；既有原生规则可能覆盖同项约定 | [Rules](https://docs.qoder.com/user-guide/rules) |
| Zed 内置 Agent | `AGENTS.md` | 使用项目指令；在 Zed 中运行的外部 Agent 仍遵循其自己的加载规则 | [Instructions](https://zed.dev/docs/ai/instructions) |
| Warp | `AGENTS.md` | 项目规则；确认相应上下文功能已启用 | [Project rules](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/ai-objects/) |
| goose | `.goosehints` | 使用 `@relay.md` 原生包含文件；需要启用 Developer 扩展 | [Hints](https://goose-docs.ai/docs/guides/context-engineering/using-goosehints/) |
| Factory Droid | `AGENTS.md` | 使用持久项目指令，按入口要求读取核心 | [AGENTS.md](https://docs.factory.com/harness/agents-md) |

AGENTS.md 的[官方生态清单](https://agents.md/)还列出了 Jules、Devin 等工具。Windsurf 的原官方入口页本次跳转到无法读取的 Devin 文档，因此没有添加未经核实的新路径。这些工具暂提供共享 AGENTS.md 入口，具体版本、加载优先级和记忆写回仍待核实，不将生态收录等同于完整适配验收。

本项目面向具备文件读写能力的 Agent。普通网页聊天、仅提供行内补全或不能读取其他文件的审查功能，需要额外接入方式。兼容范围按工具和具体功能记录，不承诺未经统计或实测的覆盖百分比。

## 确认接入是否有效

首次使用一个工具时，可用下面三步核对：

1. 让 Agent 说明实际读取的核心文件路径和 human-data 位置，核对它是否真的加载了文件。
2. 提供一条无敏感信息的任务或偏好，让它按核心约定自行保存，再检查实际文件。
3. 打开没有继承聊天上下文的新会话，要求从工作记忆恢复该条信息。

只有完成这些步骤，才能确认该工具在你的环境中完成了读取与写回。工具的信任设置、目录权限、忽略规则、模式及版本变化，都可能影响实际结果。
