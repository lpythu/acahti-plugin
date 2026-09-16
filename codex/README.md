# Acahti for Codex

Use MCP first for identity, repositories, PRs and CI. The generic package supports any Acahti instance; workspace release archives bundle the chosen endpoint.

## First connection

1. Install the plugin. For a workspace package, open its MCP connection settings (gear) and complete Authenticate/OAuth with your own account.
2. For the generic package only, configure your instance through native MCP settings or `codex mcp add <name> --url <endpoint>`, then `codex mcp login <name>` when authentication is required. Reuse existing connections.
3. Return to a local Codex task; start a new task if tools have not refreshed. Ask: **通过 MCP 检查我的 Acahti 身份和待处理事项**.
4. Success requires MCP `whoami` for the intended account and a successful `inbox` call. Logging into the website is a separate operation.

Missing tools: inspect connection status first. Authenticate for missing/expired authorization; diagnose transport errors without repeated login attempts. Do not silently substitute a browser or REST for MCP. Never paste passwords or tokens into a task.

## Git author

For commits targeting Acahti, follow the skill: fresh MCP `whoami`, `setup_local`, then verify author and committer. This includes merge/pull-generated commits; inspect outgoing commits before pushing. Preserve original authorship when replaying or amending existing commits. Other destinations keep their identity. Optional `hooks/hooks.json` only reminds the agent; trust it via `/hooks` if you want that. It does not enforce a Git-level block.

## Releases

For SAIDC, merge reviewed changes into `main`. The `workspace-release` GitHub Actions workflow tests this source, bundles `workspaces/saidc.json`, and publishes the generated `workspace-saidc` branch. The workspace marketplace tracks that branch through daily sync or **Sync now**. Do not edit the generated branch or delete the workspace plugin to update it.

Use `scripts/package_workspace.py` for standalone ZIP distributions. The generic plugin remains instance-independent. Workspace sync distributes configuration, not personal OAuth credentials; verify the new version in a new task. Changed hooks may require renewed trust in `/hooks`.
