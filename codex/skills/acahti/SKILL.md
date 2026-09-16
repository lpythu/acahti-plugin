---
name: acahti
description: >-
  Use MCP first for Acahti identity, repositories, PRs, pipelines and CI.
  Before git commit in an Acahti repo: whoami, then setup_local.
  Also use for Acahti connection setup and missing MCP tools.
---

# Acahti

## MCP first

Use the selected instance's MCP tools for identity, repository queries, PRs, pipelines and CI. Discover the tools available in this session, call `whoami`, then use the relevant tool (for example `repo_list` or `inbox`). A loaded skill is not proof that the MCP connection is ready.

Do not silently substitute browser automation, web search, REST calls or Git credential extraction for missing MCP tools. Browser use is appropriate for the user completing the MCP OAuth flow, or for an explicitly requested webpage operation. A website login does not authorize the MCP connection. Never request passwords or tokens in chat.

After `whoami` succeeds, fetch its `skill_url` for current instance-specific workflows. Fetching this public instruction document is permitted; it is not a substitute for MCP business tools. Check that the URL belongs to the intended instance. If it cannot be retrieved, explain the failure before making changes that depend on those instructions. Keep MCP-first routing, identity verification and repository scoping in force.

## Instance configuration

The generic package has no fixed instance endpoint. Reuse an existing MCP connection for the intended instance, regardless of its name. If several instances match the task ambiguously, ask which to use. If no connection exists, ask for the instance URL; do not infer it from examples or the publisher.

For a native local Codex connection, use `codex mcp add <connection-name> --url <endpoint>`, then `codex mcp login <connection-name>` if authentication is required. Use the actual configured server identifier. Validate the base URL: HTTPS, a host, no embedded credentials, query or fragment; preserve a deployment path prefix and append `/mcp` once. Quote arguments safely. Changing the instance does not authorize rewriting Git remotes or transferring credentials.

## First use and connection troubleshooting

When the user asks to log in, first explain: **网页登录不等于 MCP 授权，请连接插件里的 MCP 服务器。** Inspect the available connection status before choosing the next step.

- **Not connected / authentication required / 401:** open the installed Acahti plugin details, find its MCP server connection and open its settings (gear). Choose the sign-in / Authenticate action if shown. Have the user finish their own OAuth in the browser, then return to Codex. For a standalone CLI connection, use `codex mcp login <actual-server-name>`. Do not add a duplicate server or send the user to the website's ordinary login page as a substitute.
- **Transport, timeout or initialization error:** report the actual startup error and endpoint. Diagnose network/server compatibility; do not repeatedly ask for login without an authentication error.
- **Connected but tools absent:** verify this task's execution environment supports the bundled connection, refresh/reconnect as available, then start a new local task if its tool inventory is stale. Web/cloud and desktop-local connections are not interchangeable. If status is inaccessible, say it is unknown and ask for the connection's displayed status, not credentials.
- **Success:** call MCP `whoami`, confirm the intended account and instance, then call `inbox` or the requested tool. A successful browser login or repository page is not an MCP acceptance test.

Give one concrete next action matching the observed state. Do not repeat a generic “go log in” message or claim success without a successful tool call.

## Acahti git author

Before `git commit` or `--amend`:

1. `git remote -v`
2. Call MCP `whoami`
3. Gate **only** on remote URL host — never on directory or repo name
4. If **any** remote URL host is in `whoami.apply_when_remote_host`, run `whoami.setup_local` (`git config --local` only). That sets git author to `git_name` / `git_email`.
5. If **no** remote is an Acahti host, leave `user.name` / `user.email` alone.

```text
✅ Acahti remote → git author = whoami.git_name / whoami.git_email
✅ github.com / codeup / other → leave author alone
❌ Infer island from folder or repo name
❌ git config --global
❌ Ask the user for name or email
```

Hooks in this package only remind the agent to follow these steps. They do not set git config.

## Island CI and PRs

When the push or PR target is an Acahti remote (host in `whoami.apply_when_remote_host`):

## Git tags vs image tags

Two namespaces. Do not copy one onto the other.

| | Form | Example |
|---|---|---|
| **git tag** | `v` + semver | `v1.4.0` |
| **OCI / helm `image.tag`** | no `v` | office `dev-{sha}`; HK `1.4.0`; `latest` pointer |

YAML: `${CI_COMMIT_TAG#v}` (the pipe expands it; the runner interpolates `${CI_COMMIT_TAG}`). In `commands:`, write `$IMAGE` not `${IMAGE}`.

Put jobs in `.acahti/pipelines/`. Call official pipes with `pipe: <name>@v1` and `with:`. Do not vendor `.acahti/scripts`, write `uses:`, or call `ACAHTI_RUNNER`. YAML only names island-external secrets (`KUBECONFIG: kubeconfig_office`); never put values in git or `with:`. Acahti packages use the triggering user's identity.

```text
✅ git tag v1.4.0
✅ harbor.example/app:1.4.0
✅ workloads.app.image.tag=${CI_COMMIT_TAG#v}
❌ git tag 1.4.0
❌ harbor.example/app:v1.4.0
❌ image.tag=${CI_COMMIT_TAG}
```

## Branches

Protection is per repository. Call `repo_get` and `branch_list`; do not assume `dev` / `test` / `main` / `release`. Direct-push when `protected` is false. Open a PR when `protected` is true (`pr_create` `base` = `default_branch` unless the user named another). If the remote declines a push, open a PR to the default branch.
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

## Clone and remote name

- Clone via `whoami.clone_url_template` (owner is `whoami.org`, not a team name)
- Team names are access only — do not clone `team/<repo>`
- Prefer remote name `acahti` for the island URL
- If Codeup/GitHub is already `origin`, keep it; fetch/push the island on `acahti`
- Do not `git fetch --all` just to sync the island

```text
✅ git remote add acahti <whoami.clone_url_template>
✅ git push acahti HEAD:dev
❌ Replace origin with Acahti when another host is the product remote
❌ Paste Bearer tokens or read secrets/ for git auth — use MCP OAuth + credential helper
```

On 401, tell the user to finish MCP OAuth for this connection. Do not ask them to paste a token.

Island policy in this skill must stay aligned with `cursor/rules/*.mdc` in the same repository.
