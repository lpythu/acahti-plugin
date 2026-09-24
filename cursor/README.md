# Acahti (Cursor)

Cursor plugin for a self-hosted [Acahti](https://github.com/lpythu/acahti) instance: git, PRs, pipelines, secrets, and commit checks.

Set **ACAHTI_URL** in Customize → Acahti → Configure (no trailing slash). MCP is `${ACAHTI_URL}/mcp` (OAuth). Then `whoami` and follow `whoami.skill_url`.

## Rules

| Rule | When |
|---|---|
| `rules/git-author.mdc` | Commits and pushes targeting Acahti only; verify the actual destination |
| `rules/island-git.mdc` | Clone / dual remote / push to the island |
| `rules/island-ci.mdc` | Protected branches, PRs, post-push checks, git tag `vX.Y.Z` vs image tags without `v` |
| `rules/skill-source.mdc` | Any Acahti MCP / skill work |

Non-Acahti remotes (GitHub, Codeup, …) are out of scope for author and CI rules.

## Install

From this monorepo:

```text
cp -R cursor ~/.cursor/plugins/local/acahti
```

Or install via the repo marketplace (`.cursor-plugin/marketplace.json`). Reload the Cursor window. Do not also add `acahti` to `~/.cursor/mcp.json`.

Source: [github.com/lpythu/acahti-plugin](https://github.com/lpythu/acahti-plugin).
