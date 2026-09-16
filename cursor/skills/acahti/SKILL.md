---
name: acahti
description: Use Acahti git, PRs, pipelines, and commit checks. Use when committing or pushing to an acahti remote, opening or merging a PR, reading pipelines, or when the user mentions Acahti, whoami, or island CI. MCP is this plugin (OAuth). Follow whoami.skill_url. Plugin rules gate author only when an Acahti remote exists.
---

# Acahti

Discover MCP tools this session. Call `whoami`, then GET `whoami.skill_url` and follow that. Do not trust this file or a cached tool list.

MCP is this plugin. Do not add `acahti` to `~/.cursor/mcp.json`.

For commits and pushes targeting Acahti, follow rule `git-author`: resolve the intended destination, call MCP `whoami`, and use its `git_name` / `git_email`. Include merge/pull paths that create commits. Other remote targets are unaffected even in a mixed-remote repository.
