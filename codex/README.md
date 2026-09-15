# Acahti (Codex)

Acahti workflows for Codex. Instance URL is configured in Codex MCP settings, not bundled in this plugin.

## Install and configure

1. Install this package from [`codex/`](.) in [acahti-plugin](https://github.com/lpythu/acahti-plugin).
2. Start a new task and ask: **Configure Acahti using my instance URL**. Supply your instance base URL when asked.
3. Codex adds a native HTTP MCP connection at that instance's `/mcp` endpoint. Complete your own OAuth sign-in.
4. Start a new task and ask Codex to check your Acahti identity.

For manual setup, use `codex mcp add acahti --url <your-full-mcp-endpoint>` and, if needed, `codex mcp login acahti`. The URL is stored in your Codex MCP settings, outside this plugin. Never put credentials in the URL.

## Changing or adding instances

Ask Codex to change the named Acahti connection to your new base URL and sign in again. For simultaneous instances, use distinct connection names and tell Codex which one to use. Changing an MCP connection does not change repository git remotes.

## Migration from 1.2

Version 1.3 removes the bundled, fixed endpoint. Existing users must configure their intended instance as a native Codex MCP connection once. Reuse an existing standalone connection when present. Update the installed plugin and start a new task before testing. Each engineer authenticates separately; the plugin does not share service permissions or credentials.

## Design

Codex's supported compatibility manifest has no Cursor-style `variables` configuration form. This package therefore separates reusable skills from instance-specific MCP configuration instead of shipping an unresolved URL placeholder or an extra proxy process. See the official [Codex MCP documentation](https://developers.openai.com/codex/mcp).

Current workflow details and remote host matching come from the selected instance's `whoami` response. The Cursor package lives in `../cursor/` in the same repository.
