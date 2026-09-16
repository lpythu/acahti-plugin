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

Keep island policy aligned: Cursor `cursor/rules/*.mdc` and the matching sections in `codex/skills/acahti/SKILL.md`. Codex ships optional, trusted reminder hooks; they do not set Git identity or enforce commits.


## Workspace release archive

Generate each workspace release from the current Codex source instead of editing an older ZIP:

```sh
python3 scripts/package_workspace.py --instance https://your-instance.example --workspace SAIDC --output /path/to/acahti-saidc-1.6.0.zip
```

The instance URL is a release argument, not part of the generic plugin source. The generated package includes the MCP endpoint, current skills, reminder hooks and a release manifest with file hashes. Tests, bytecode and local credentials are excluded. Upload the versioned ZIP and verify the directory version, then test MCP `whoami` and `inbox` from a fresh member task. Hooks must be reviewed/trusted separately after changes; their trust is not shared by the workspace.

## Automatic SAIDC workspace publishing

`workspaces/saidc.json` is the workspace-specific connection and existing plugin ID. The generic `codex/` package stays instance-independent.

Tests: install `tests/requirements.txt`, then run `python3 -m unittest discover -s tests -v`.

On relevant changes to `main`, `.github/workflows/workspace-release.yml` runs tests, generates the workspace package and publishes the `workspace-saidc` branch. The generated version includes the source commit, so changed contents never silently reuse an installed version. `build.json` records provenance. Failed builds do not publish.

Import `https://github.com/lpythu/acahti-plugin` in ChatGPT Admin → Plugins → Add → Import marketplace, leave Path empty and select branch `workspace-saidc`. The marketplace entry's `pluginId` links the existing Acahti plugin, preserving its ID and workspace installation policy. Do not delete the plugin to update it. GitHub-managed plugins are updated by sync rather than ZIP uploads.

After the workflow succeeds, the workspace checks for updates daily; use Marketplaces → Sync now for immediate rollout and check the import report. Changing hooks still requires members to review their trust. Changing OAuth endpoint/account may require authentication; sync does not share credentials.

For rollback, revert the source change on `main` and let the same build/sync process publish a new revision. Do not force-push or manually edit the generated branch. Keep the importing admin's GitHub connection authorized. For another workspace, use its own plugin ID and distribution config; never reuse SAIDC's ID.
