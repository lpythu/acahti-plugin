# Acahti for Codex

Use MCP first for identity, repositories, PRs and CI. The generic package supports any Acahti instance; workspace release archives bundle the chosen endpoint.

## First connection

1. Install the plugin. For a workspace package, open its MCP connection settings (gear) and complete Authenticate/OAuth with your own account.
2. For the generic package only, configure your instance through native MCP settings or `codex mcp add <name> --url <endpoint>`, then `codex mcp login <name>` when authentication is required. Reuse existing connections.
3. Return to a local Codex task; start a new task if tools have not refreshed. Ask: **通过 MCP 检查我的 Acahti 身份和待处理事项**.
4. Success requires MCP `whoami` for the intended account and a successful `inbox` call. Logging into the website is a separate operation.

Missing tools: inspect connection status first. Authenticate for missing/expired authorization; diagnose transport errors without repeated login attempts. Do not silently substitute a browser or REST for MCP. Never paste passwords or tokens into a task.

## Git author

Before commit in an Acahti repo, follow the skill: `whoami` then `setup_local`. Unrelated remotes keep their identity. Optional `hooks/hooks.json` only reminds the agent; trust it via `/hooks` if you want that.

## Releases

Use `scripts/package_workspace.py` from the repository root to generate an instance-specific workspace ZIP from this source. Do not reuse an old ZIP after updating skills. The generic plugin remains instance-independent.
