---
name: acahti
description: Use Acahti git, PRs, pipelines, and commit checks. Use when committing or pushing to an acahti remote, opening or merging a PR, reading pipelines, or when the user mentions Acahti, whoami, or island CI. MCP is this plugin (OAuth). Follow whoami.skill_url. Plugin rules gate author only when an Acahti remote exists.
---

# Acahti

Discover MCP tools this session. Call `whoami`, then GET `whoami.skill_url` and follow that. Do not trust this file or a cached tool list.

MCP is this plugin. Do not add `acahti` to `~/.cursor/mcp.json`.

Before any commit: gate only on remote URL host (never directory/repo name). If any remote host is in `whoami.apply_when_remote_host`, run `setup_local`; otherwise leave the laptop git author alone — including GitHub product repos `acahti` / `acahti-plugin`. See plugin rule `git-author`.
