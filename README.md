# Acahti

Cursor plugin for a self-hosted [Acahti](https://github.com/lpythu/acahti) instance: git, PRs, pipelines, and commit checks.

Set **ACAHTI_URL** in Customize → Acahti → Configure (no trailing slash). MCP is `${ACAHTI_URL}/mcp` (OAuth). Then `whoami` and follow `whoami.skill_url`.

```text
cp -R . ~/.cursor/plugins/local/acahti
```

Reload the Cursor window. Do not also add `acahti` to `~/.cursor/mcp.json`.
