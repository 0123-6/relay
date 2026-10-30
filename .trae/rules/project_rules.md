---
description: Load the Relay shared core before handling a task.
alwaysApply: true
---

Before handling a task, use a file-reading tool to read `relay.md` at the workspace root, two directories above this rule file.
Follow it to restore or initialize this hub's `human-data`.
If the same core file is already loaded, reuse it. Keep this file limited to loading instructions.
