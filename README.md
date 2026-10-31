<p align="center">
  <img src="assets/logo.svg" width="104" height="104" alt="Relay logo">
</p>

# Relay

[English](README.md) · [简体中文](README.zh-CN.md)

**Shared memory that keeps work moving across agents and sessions.**

Relay treats agents as mostly stateless executors. Information from people, information produced by agents, and task state live together on disk in `human-data/`, where AI organizes, maintains, and reads them autonomously.

Different sessions and agents use the same persistent information to recover goals, context, working methods, and progress. You do not have to explain everything from scratch. Multiple agents can work from this shared source.

## Get started

No service to run, packages to install, or specific model required.

Keep periodic snapshots or backups of `human-data/` outside that directory so you can recover if an agent accidentally changes or damages the memory.

1. Download this project and open it with an agent that can read and write local files.
2. Grant access to this directory and the projects you want it to work on.
3. Give it a task:

```text
Read relay.md, then restore or initialize human-data.
Follow those instructions to do my task and maintain working memory as you go.
My task is: …
```

When switching sessions or tools, point the new agent to the same directory. Project entry files apply only within each tool's discovery scope.

## How it works

- [relay.md](relay.md) defines the shared agent instructions.
- `human-data/` is the authoritative persistent memory, initially empty. The agent records your input and its own findings, decisions, and progress, and manages retrieval and organization.
- `AGENTS.md`, `CLAUDE.md`, and other tool entries load the same core. See [tool compatibility and connection checks](docs/compatibility.md).

On first real use, the agent creates an independent local Git repository inside `human-data/` for memory history. The public project ignores this private memory; it is not uploaded with the template. Keep credentials out of memory.

## Current limits

Relay provides working instructions and shared files. It has no concurrency locks, task scheduler, or cross-device sync. Agents modifying the same files need coordination. Recovery depends on the agent's capabilities and permissions; complete lossless recovery and fresh-session behavior in every tool have not been verified.
