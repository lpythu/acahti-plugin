---
name: acahti
description: Use Acahti git, PRs, pipelines, and commit checks. Use before committing or amending in a repository with an Acahti remote, when cloning or pushing to Acahti, opening or merging an Acahti PR, reading pipelines, or when the user mentions Acahti, whoami, or island CI. Configure an Acahti instance URL through native Codex MCP settings and use individual OAuth.
---

# Acahti

Discover the available MCP tools in this session and complete instance configuration below if needed. Call `whoami`, then fetch `whoami.skill_url` and follow the live document for current commands and tool schemas. Do not rely on a cached tool list. The sections below preserve the repository, author, and CI scope rules.

## Instance configuration

This plugin does not bundle an instance endpoint. The instance URL belongs in the user's native Codex MCP configuration, independently of the plugin version.

Before calling `whoami`, discover existing Acahti connections. Reuse an existing connection when it matches the user's intended instance. If more than one instance is connected, ask which one to use; never pick arbitrarily. If no connection exists, ask for the Acahti instance base URL. Do not infer the instance from the publisher, examples, or a previous user's connection.

For local Codex, configure the connection using `codex mcp add <connection-name> --url <endpoint>`. Prefer `acahti` for the first connection; use a distinct descriptive name for additional instances. Validate the supplied base URL with a URL parser: require HTTPS and a host, reject credentials, query strings, and fragments, remove trailing slashes, and append `/mcp` once. Preserve any deployment path prefix. Pass command arguments as an argument array or quote them safely. Do not interpolate untrusted URL text into shell code.

The command may start OAuth automatically. Otherwise use `codex mcp login <connection-name>`. Let the user complete sign-in in the browser. Do not request tokens, read secrets, or embed credentials in the plugin. After connection setup, start a new Codex task if the MCP tools are not yet available. Never claim a connection works until `whoami` succeeds.

To change an existing instance, inspect its current URL first. If the user explicitly requested that change, update that named connection with `codex mcp add`, then authenticate against the new instance. Never transfer an old instance's credentials to a new host. Existing git remotes are independent: do not rewrite them merely because the MCP URL changed.

Use `whoami.apply_when_remote_host`, `whoami.clone_url_template`, and `whoami.skill_url` from the selected connection for all instance-specific behavior. If the live skill cannot be retrieved, report that and do not perform write operations using guessed instructions.

## Acahti git author

Applies only when you are about to `git commit` (or amend) in the current repo. Otherwise ignore.

1. `git remote -v`
2. Call MCP `whoami`
3. If **any** remote URL host is in `whoami.apply_when_remote_host`, run every command in `whoami.setup_local` (`git config --local` only)
4. If **no** remote is an Acahti host, do **not** change `user.name` / `user.email` — keep the laptop identity

```text
✅ Acahti remote present → local author = whoami.git_name / whoami.git_email
✅ Only github.com / codeup / other → leave author alone
❌ git config --global
❌ Ask the user for name or email
❌ Invent an email; use whoami.git_email ({login}@noreply.… from whoami)
```

`git_name` is the admin-set commit author (default `login`). Do not substitute the laptop display name when step 3 applies.

## Island CI and PRs

When the push or PR target is an Acahti remote (host in `whoami.apply_when_remote_host`):

## Branches

- Do not push `main` or `release` — open a PR
- `dev` and `test` are protected; if push is declined, open a PR
- Official release trigger is `git push`, a tag, or opening a PR — not `pipeline_trigger` as a substitute

## After push to the island

1. `git rev-parse HEAD`
2. `checks_wait` with `{owner, name, sha}` — follow `whoami.skill_url` for poll vs snapshot
3. Failed: `pipeline_list` → `pipeline_get` → `pipeline_log` (omit `step` unless needed)
4. Fix and push, or `pipeline_rerun`; `pipeline_cancel` only for a stuck run
5. Green → `pr_merge`; `blocked` → `deploy_approve`
6. Triage: `inbox`

When the user only pushes GitHub/Codeup/`origin` and there is no island push in this turn, do not run island CI tools.

## Island git remotes

Follow `whoami.skill_url` for full detail. This rule covers remotes only.

## Scope

- Island git = HTTPS host in `whoami.apply_when_remote_host` 
- Not island: `ssh://`, `:2222`, bare LAN IPs, Codeup, GitHub
- The `acahti/` **product** repo on GitHub is not island git — leave that remote on GitHub

## Clone and remote name

- Clone only `saidc/<repo>` via `whoami.clone_url_template`
- Team names (Platform, ModelCamp, …) are access only — do not clone `modelcamp/<repo>`
- Prefer remote name `acahti` for the island URL
- If Codeup/GitHub is already `origin`, keep it; fetch/push the island on `acahti`
- Do not `git fetch --all` just to sync the island

```text
✅ git remote add acahti https://…/saidc/<repo>.git
✅ git push acahti HEAD:dev
❌ Replace origin with Acahti when another host is the product remote
❌ Paste Bearer tokens or read secrets/ for git auth — use MCP OAuth + credential helper
```

On 401, tell the user to finish MCP OAuth for this connection. Do not ask them to paste a token.

Island policy in this skill must stay aligned with `cursor/rules/*.mdc` in the same repository.
