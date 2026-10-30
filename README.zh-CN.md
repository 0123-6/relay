<p align="center">
  <img src="assets/logo.svg" width="104" height="104" alt="Relay 图标">
</p>

# Relay

[English](README.md) · [简体中文](README.zh-CN.md)

由 AI Agent 自主管理的个人工作中枢。

你描述目标、提供必要信息并决定授权范围。Agent 执行工作，自行保存背景、任务、决策与进度，让下一次会话能够继续接手。human-data 的整理、索引和更新由 Agent 负责，无需你手工维护。

项目的核心是一份 [relay.md](relay.md)，工具入口负责加载它，实际工作记忆保存在 human-data。项目无需启动服务、安装依赖包或指定模型；本地版本追溯使用 Git，由 Agent 在使用前检查。

## 开始使用

1. 下载本项目，放在你准备长期保存工作上下文的位置。
2. 用具备本地文件读写和任务执行能力的 Agent 打开该目录；按工具要求信任工作区、启用项目指令。
3. 描述你要做的事。首次使用时，Agent 按需初始化 human-data，后续自动维护。

一次启动可以这样说：

```text
请先读取当前目录的 relay.md，恢复或初始化 human-data。
接下来按其中约定推进我的任务，并主动维护工作记忆。
我的任务是：……
```

支持的工具会通过各自入口发现核心文件。这段启动语句也可用于首次核对或其他具备文件工具的 Agent，不需要重复填写用户背景表。

human-data 初始只有 `.gitkeep` 占位文件。目录分类、记录格式与摘要由 Agent 按实际需要创建；当前目录不预置任何个人资料或演示任务。

## 日常怎么用

照常向 Agent 提供任务、补充要求和反馈即可。目标、关键确认、验证结果和剩余事项应由 Agent 主动写入 human-data。

切换会话或 Agent 后，让它读取同一份核心文件和工作记忆。只有会影响正确性、范围或授权的关键信息缺失时，才需要你补充。

下面是预期工作流程示例，不是已完成的效果测试：

1. 你提供某个工程的位置，要求修复一个问题。
2. Agent 读取目标工程约定，定位、修改并验证，记录关键结果和未完成项。
3. 新会话中你说“继续上次的任务”。
4. 新 Agent 从 human-data 找到工程位置、最新状态和下一步，重新核实当前代码后继续工作。

## 工作记忆的版本管理

核心约定允许 Agent 在本中枢内自主执行日常本地 Git 操作，包括初始化、检查状态与差异、查阅历史、暂存和提交，无需逐次询问。其他工程的 Git 操作仍遵循各自约定；配置远端、推送、发布、重写历史和丢弃改动需要相应授权。

首次用中枢处理真实任务时，Agent 在 human-data 内建立独立的本地 Git 仓库，在首次记录、重要决策、任务阶段、资料整理和交接后保存有意义的变更。你无需手动初始化或提交记忆。维护或审查公开模板时，记忆目录保持空占位。

两个仓库各有职责：

- 项目仓库保存通用规则、工具入口、说明和图标，继续通过忽略规则排除私人记忆。
- human-data 独立仓库保存记忆历史，默认不配置远端，也不作为项目的子模块；它自己的忽略规则排除凭据及临时文件。

Agent 会核对记忆仓库的实际根目录就是 human-data，不能把识别到上层项目仓库当成已完成初始化。记忆操作明确使用 `git -C <human-data 的绝对路径>`，确保提交进入正确仓库。

已有记忆仓库保留原有历史、分支和配置，其他人的未提交或暂存改动保持原样。如果 Git、提交身份或权限缺失，Agent 先保留已写入的记忆，并明确版本追溯尚未完成；没有变更时不创建空提交。

历史负责追溯，Agent 仍需维护简明的当前索引、摘要和必要归档。工具原生自动提交只覆盖它实际管理的仓库，Agent 还需核对记忆变更是否已在独立仓库提交。

## 在其他工程中工作

本中枢可以服务多个独立工程。工程源码留在原工程目录，背景、决策和交接信息集中保存在本中枢的 human-data。

如果 Agent 从其他目录启动，明确提供中枢实际路径，并给予读取核心文件、读写 human-data 及处理目标工程所需的权限。启动语句示例：

```text
我的个人工作中枢位于 <本中枢的实际绝对路径>。
请先读取该目录的 relay.md 和 human-data，恢复当前任务上下文。
这次工作的目标工程位于 <目标工程的实际绝对路径>。
```

入口文件只在工具规定的工作区或目录范围内生效。下载本项目不会自动修改各工具的全局配置，也不会让另一个工程中的 Agent 自动发现本中枢。

## 文件职责

| 文件或目录 | 用途 |
| --- | --- |
| [relay.md](relay.md) | Agent 的唯一核心通用约定 |
| README.md | 给使用者看的介绍、启动方式和兼容说明 |
| human-data/ | Agent 自主管理的工作记忆，首次实际使用时建立独立本地 Git 仓库 |
| AGENTS.md、CLAUDE.md、GEMINI.md 等 | 按不同工具的规范加载核心文件 |
| opencode.json、.aider.conf.yml | 通过工具原生配置直接加载核心文件 |
| [assets/logo.svg](assets/logo.svg) | 项目图标：多个工作节点连接同一份记忆文档 |
| .gitignore | 默认排除实际工作记忆、本地凭据及临时文件 |

## 工具适配

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

## 个人资料与公开模板

项目级 `.gitignore` 排除 human-data 内的实际资料及其独立 Git 元数据，仅保留 `.gitkeep`；记忆历史保存在独立本地仓库。忽略规则不会加密文件，也不会移除已经提交的历史内容；公开前应确认项目仓库里只保留准备分享的模板文件。

本项目使用后产生的个人背景、公司资料和任务记录，留在你的私有工作副本。Agent 仍需获准读取这些被版本控制忽略的文件；如果某个工具还按忽略规则屏蔽文件读取，需要在该工具中单独允许本目录。

## 项目边界

执行效果取决于 Agent 能力、任务范围、资料和授权。本项目提供共同工作约定与可携带的工作记忆，不额外提供后台运行服务、定时调度或并发锁；这些能力由实际使用的工具承担。

维护通用行为时修改 relay.md；个人偏好、项目进度和具体任务由 Agent 写入 human-data。工具入口只随各工具的加载规范更新，避免维护多份核心规则。
