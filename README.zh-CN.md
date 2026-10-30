<p align="center">
  <img src="assets/logo.svg" width="104" height="104" alt="Relay 图标">
</p>

# Relay

[English](README.md) · [简体中文](README.zh-CN.md)

**共享外置记忆，让工作跨会话、跨 Agent 延续。**

Relay 将 Agent 视为近乎无状态的执行者。人提供的信息、Agent 在工作中产生的信息和任务状态，统一保存在磁盘上的 `human-data/`，由 AI 自主整理、维护和读取。

不同会话与 Agent 从同一份持久信息恢复背景、目标、工作方式和进展，无需你每次从零交代“做什么、怎么做”。多个 Agent 也可基于这份信息分工协作。

## 开始使用

无需启动服务、安装依赖包或指定模型。

1. 下载本项目，用具备本地文件读写能力的 Agent 打开目录。
2. 授权它访问本目录和你希望处理的工程。
3. 描述任务：

```text
请先读取 relay.md，恢复或初始化 human-data。
按其中约定执行任务，并持续维护工作记忆。
我的任务是：……
```

切换会话或工具后，让新 Agent 读取同一目录即可。工具入口只在各自规定的目录范围内生效。

## 如何工作

- [relay.md](relay.md)：统一的 Agent 工作约定。
- `human-data/`：唯一权威的持久工作记忆，初始为空。Agent 持续记录你的输入及自己形成的发现、决策和进展，自主组织和按需读取。
- `AGENTS.md`、`CLAUDE.md` 等：各工具的加载入口，共用同一份核心。详见[工具适配与接入检查](docs/compatibility.zh-CN.md)。

首次实际使用时，Agent 在 `human-data/` 内建立独立本地 Git 仓库，保存记忆历史。公开项目默认忽略这些私人记忆，不随模板上传；凭据不要写入记忆。

## 当前边界

Relay 提供工作约定与共享文件，不提供并发锁、任务调度或跨设备同步。同文件并发修改需要协调。恢复效果取决于 Agent 能力与权限，尚未验证完全无损恢复或所有工具的新会话效果。

## Star 历史

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/star-history-dark.svg">
  <img src="assets/star-history.svg" width="900" alt="Relay 每日 GitHub Star 历史，手绘风格折线图">
</picture>

[GitHub Actions 工作流](.github/workflows/star-history.yml)每天记录真实 Star 数并绘图。用于自己的仓库时，启用 Actions 并允许工作流提交即可。历史从启用时积累，不补造过去数据；仅采集公开统计，不读取私人记忆。
