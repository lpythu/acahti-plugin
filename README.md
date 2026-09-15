# Acahti

Cursor plugin for a self-hosted [Acahti](https://github.com/lpythu/acahti) instance: git, PRs, pipelines, and commit checks.

Set **ACAHTI_URL** in Customize → Acahti → Configure (no trailing slash). MCP is `${ACAHTI_URL}/mcp` (OAuth). Then `whoami` and follow `whoami.skill_url`.

## Rules

| Rule | When |
|---|---|
| `rules/git-author.mdc` | Always: before commit, Acahti author only if an Acahti remote exists |
| `rules/island-git.mdc` | Clone / dual remote / push to the island |
| `rules/island-ci.mdc` | Protected branches, PRs, post-push checks on the island |
| `rules/skill-source.mdc` | Any Acahti MCP / skill work |

Non-Acahti remotes (GitHub, Codeup, …) are out of scope for author and CI rules.

```text
cp -R . ~/.cursor/plugins/local/acahti
```

Reload the Cursor window. Do not also add `acahti` to `~/.cursor/mcp.json`.
