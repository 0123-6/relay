# Tool compatibility

[English](compatibility.md) · [简体中文](compatibility.zh-CN.md) · [Back to README](../README.md)

The table is based on official documentation reviewed on 2026-10-30. Entry files, relative paths, and configuration syntax have been checked statically. Automatic loading, task execution, and memory write-back have not been tested in fresh sessions with every tool. “Import” means native inclusion; a “read instruction” asks the agent to use a file-reading tool. These are different mechanisms.

| Tool | Entry provided | Loading behavior and limitations | Official reference |
| --- | --- | --- | --- |
| OpenAI Codex | `AGENTS.md` | A read instruction loads the core after entry discovery; instruction scope and actual permissions apply | [OpenAI Docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Claude Code | `CLAUDE.md` | Native `@./relay.md` import; does not rely on AGENTS version or fallback behavior | [Memory](https://code.claude.com/docs/en/memory) |
| Gemini CLI | `GEMINI.md` | Native `@./relay.md` import | [Context files](https://geminicli.com/docs/cli/gemini-md/) |
| Qwen Code | `QWEN.md` | `@./relay.md` reference; newer versions may also load AGENTS | [Memory](https://qwenlm.github.io/qwen-code-docs/en/users/features/memory/) |
| GitHub Copilot | `.github/copilot-instructions.md`, `AGENTS.md` | A read instruction loads the core; instruction support and file access vary across clients, agents, and code review | [Custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions) |
| Cursor | `AGENTS.md` | Project instructions direct the agent to read the core | [Rules](https://cursor.com/docs/rules) |
| Cline | `AGENTS.md`, `.clinerules/relay.md` | Standard entry and native rule; confirm they are enabled in the Rules panel; duplicate entries should not repeat initialization | [Cline Rules](https://github.com/cline/cline/blob/main/docs/customization/cline-rules.mdx) |
| Roo Code | `.roo/rules/relay.md` | Native workspace rule; AGENTS support depends on settings | [Custom instructions](https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/features/custom-instructions.md) |
| Continue | `.continue/rules/relay.md` | `alwaysApply: true`; requires an agent mode with file access; autocomplete does not include these rules | [Rules](https://docs.continue.dev/customize/deep-dives/rules) |
| TRAE | `.trae/rules/project_rules.md` | Provides a project rule with alwaysApply; the full official rules page could not be retrieved, so the filename follows the official article; current directory and activation behavior still need testing | [Rules](https://docs.trae.ai/ide/rules), [Official article](https://www.trae.ai/blog/trae_tutorial_0825) |
| OpenCode | `opencode.json`, `AGENTS.md` | Native `instructions` loading, with AGENTS as a shared entry | [Rules](https://opencode.ai/docs/rules/) |
| Aider | `.aider.conf.yml` | Native `read` loading; local automatic commits are enabled; the agent versions the independent memory repository according to the core | [YAML config](https://aider.chat/docs/config/aider_conf.html) |
| Kiro | `AGENTS.md` | Standard entry; custom agents may require explicit resources configuration | [Steering](https://kiro.dev/docs/steering/) |
| JetBrains Junie | `AGENTS.md`, `.junie/guidelines.md` | Standard entry with a legacy guidelines fallback; a custom Guidelines path can change discovery | [Guidelines](https://junie.jetbrains.com/docs/guidelines-and-memory.html) |
| Google Antigravity | `AGENTS.md`, `GEMINI.md` | Uses supported workspace entries; confirm the loading source for the specific product surface | [Rules](https://antigravity.google/docs/rules/) |
| Qoder IDE | `AGENTS.md` | Officially recognized automatically; existing native rules may override conflicting instructions | [Rules](https://docs.qoder.com/user-guide/rules) |
| Zed built-in agent | `AGENTS.md` | Project instructions; external agents running inside Zed follow their own loading rules | [Instructions](https://zed.dev/docs/ai/instructions) |
| Warp | `AGENTS.md` | Project rules; confirm the relevant context feature is enabled | [Project rules](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/ai-objects/) |
| goose | `.goosehints` | Native `@relay.md` inclusion; requires the Developer extension | [Hints](https://goose-docs.ai/docs/guides/context-engineering/using-goosehints/) |
| Factory Droid | `AGENTS.md` | Persistent project instructions direct the agent to read the core | [AGENTS.md](https://docs.factory.com/harness/agents-md) |

The [official AGENTS.md ecosystem list](https://agents.md/) also includes Jules and Devin. Windsurf's former official entry page redirected to Devin documentation that could not be retrieved, so no unverified new paths have been added. These tools currently receive the shared AGENTS.md entry; version-specific behavior, loading precedence, and memory write-back still need verification. Ecosystem listing alone is not a completed compatibility check.

This project is intended for agents with file read/write tools. Browser-only chat, inline completion, and review features that cannot read other files need an additional integration. Compatibility is recorded by tool and feature; no unmeasured coverage percentage is promised.

## Verifying a connection

When using a tool for the first time:

1. Ask the agent to identify the actual core file path and human-data location, and check that it read the file.
2. Give it a non-sensitive task or preference, let it save the information according to the core instructions, and inspect the actual files.
3. Open a fresh session without inherited chat context and ask it to recover that information from working memory.

Completing these steps confirms reading and write-back for that tool in your environment. Trust settings, directory permissions, ignore rules, modes, and versions can affect the result.
