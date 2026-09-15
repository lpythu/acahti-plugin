# Acahti plugin

One repository, two installable packages for [Acahti](https://github.com/lpythu/acahti):

| Package | Host | Path |
|---|---|---|
| Cursor | Cursor IDE | [`cursor/`](cursor/) |
| Codex | OpenAI Codex | [`codex/`](codex/) |

Shared product behavior still comes from the connected instance (`whoami` → `whoami.skill_url`). These packages only wire MCP and host-specific guidance.

## Cursor

1. Install from this marketplace, or copy locally:

```text
cp -R cursor ~/.cursor/plugins/local/acahti
```

2. Customize → Acahti → Configure: set **ACAHTI_URL** (no trailing slash).
3. Reload Cursor. Do not also add `acahti` to `~/.cursor/mcp.json`.

Details: [cursor/README.md](cursor/README.md).

## Codex

1. Install the Codex package from [`codex/`](codex/).
2. Ask Codex to configure your instance URL, then complete OAuth.
3. MCP lives in Codex settings (`codex mcp add …`), not in this plugin.

Details: [codex/README.md](codex/README.md).

## Layout

```text
.cursor-plugin/marketplace.json   # Cursor marketplace → cursor/
.agents/plugins/marketplace.json  # Codex marketplace → codex/
cursor/                           # Cursor plugin root
codex/                            # Codex plugin root
```

Keep island policy aligned: Cursor `cursor/rules/*.mdc` and the matching sections in `codex/skills/acahti/SKILL.md`.
