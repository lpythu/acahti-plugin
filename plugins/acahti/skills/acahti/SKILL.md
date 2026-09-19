---
name: acahti
description: >-
  Use MCP first for Acahti identity, repositories, PRs, pipelines and CI.
  For commits and pushes targeting Acahti, use whoami and setup_local; leave other targets alone.
  Also use for Acahti connection setup and missing MCP tools.
---

# Acahti

## MCP first

Use the selected instance's MCP tools for identity, repository queries, PRs, pipelines and CI. Discover the tools available in this session, call `whoami`, then use the relevant tool (for example `repo_list` or `inbox`). A loaded skill is not proof that the MCP connection is ready.

Do not silently substitute browser automation, web search, REST calls or Git credential extraction for missing MCP tools. Browser use is appropriate for the user completing the MCP OAuth flow, or for an explicitly requested webpage operation. A website login does not authorize the MCP connection. Never request passwords or tokens in chat.

After `whoami` succeeds, fetch its `skill_url` for current instance-specific workflows. Fetching this public instruction document is permitted; it is not a substitute for MCP business tools. Check that the URL belongs to the intended instance. If it cannot be retrieved, explain the failure before making changes that depend on those instructions. Keep MCP-first routing, identity verification and repository scoping in force.

## Instance configuration

This SAIDC workspace release bundles the intended MCP endpoint in `.mcp.json`. Reuse that plugin connection. Do not ask members to enter an instance URL or create a duplicate standalone server. Discover its actual runtime identifier; it need not be exactly `acahti`.

Each member must authenticate this MCP connection with their own OAuth account. Workspace installation distributes configuration, not shared credentials. Open the plugin's MCP connection settings to authorize it; ordinary website login is separate. Confirm the intended account with MCP `whoami` before doing work. If multiple instances are ambiguous, ask which to use instead of switching silently.

The administrator updates the endpoint through the workspace packaging command and republishes the release. Do not change the generic source, local Git remotes or credentials to guess a different host. The bundled connection targets desktop-local tasks; check connection availability explicitly for other execution environments.

## First use and connection troubleshooting

When the user asks to log in, first explain: **网页登录不等于 MCP 授权，请连接插件里的 MCP 服务器。** Inspect the available connection status before choosing the next step.

- **Not connected / authentication required / 401:** open the installed Acahti plugin details, find its MCP server connection and open its settings (gear). Choose the sign-in / Authenticate action if shown. Have the user finish their own OAuth in the browser, then return to Codex. For a standalone CLI connection, use `codex mcp login <actual-server-name>`. Do not add a duplicate server or send the user to the website's ordinary login page as a substitute.
- **Transport, timeout or initialization error:** report the actual startup error and endpoint. Diagnose network/server compatibility; do not repeatedly ask for login without an authentication error.
- **Connected but tools absent:** verify this task's execution environment supports the bundled connection, refresh/reconnect as available, then start a new local task if its tool inventory is stale. Web/cloud and desktop-local connections are not interchangeable. If status is inaccessible, say it is unknown and ask for the connection's displayed status, not credentials.
- **Success:** call MCP `whoami`, confirm the intended account and instance, then call `inbox` or the requested tool. A successful browser login or repository page is not an MCP acceptance test.

Give one concrete next action matching the observed state. Do not repeat a generic “go log in” message or claim success without a successful tool call.

## Acahti git author

Apply this policy only to commits intended for Acahti and pushes to Acahti. A repository merely having an Acahti remote does not make its other remotes subject to this policy.

1. Resolve the actual repository and intended push destination from the user's request, explicit push remote/URL, or Git's configured push destination (including push URLs). `git commit` itself has no remote; if multiple destinations are plausible, clarify the intended destination before changing identity. Do not infer it from the directory name, remote name, or whichever remote appears first.
2. For an Acahti destination, obtain a fresh result from the matching MCP `whoami` before each commit-producing operation and compare the destination HTTPS host with `apply_when_remote_host`. Use `git_name` for Author and `git_email` for email directly; `login` identifies the account and is not a replacement for `git_name`. Do not invent or remap names.
3. Before creating a commit for that destination, run `setup_local` in the actual repository using local Git config only. If MCP identity cannot be verified, stop before creating the commit and diagnose the connection. Then verify `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`. This includes merge/pull operations that create merge commits, amend, rebase, cherry-pick, revert and their continuation commands. Account for `git -c`, `--author` and `GIT_AUTHOR_*` / `GIT_COMMITTER_*` overrides.
4. After creating commits, inspect their actual author and committer. For new original commits (including merge commits and reverts), both must match the verified identity. For amend/rebase/cherry-pick, preserve the expected original author and verify the new committer instead. Before pushing to Acahti, inspect the outgoing commits and verify the author and committer of commits created in this task. A push does not change existing commit metadata. If verified identity is unavailable or a newly created commit has an unexpected identity, stop and resolve it before pushing. Do not relabel imported commits as the current user.
5. Preserve existing authorship when amending, rebasing or cherry-picking another contributor's commit; use the current verified identity for the new committer. Reset an existing author only when the user intends that correction. Never rewrite published history automatically.

For GitHub, Codeup or any other non-Acahti target, do not require Acahti OAuth, change identity, block commits, or run island CI. When temporarily applying `setup_local` in a mixed-remote workflow, save and restore the exact prior local identity entries after the Acahti operation so a later non-Acahti commit does not inherit them. Never change global config or delete unrelated identity settings.

Hooks only remind the agent to apply this policy; they do not authenticate, change Git config or enforce a Git-level block.

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
