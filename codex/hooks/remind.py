#!/usr/bin/env python3
"""Inject Acahti guidance without network, credentials, or repository mutations."""
import json
import sys

CONTEXT = (
    "For Acahti work, load the acahti skill and use MCP first. Website login is "
    "not MCP OAuth. Missing tools require connection diagnostics, not a browser "
    "or REST fallback. Before committing/amending in an Acahti repository, "
    "obtain fresh MCP whoami, match the actual repository's remote host against "
    "apply_when_remote_host, apply setup_local there, and verify effective Git "
    "author against git_name/git_email. Do not commit to a confirmed Acahti "
    "target without verified identity. Leave unrelated repositories' identity "
    "unchanged. Preserve original authorship on amend unless correcting it is "
    "explicitly intended. This hook is a reminder, not an enforced commit guard."
)


def response(event):
    name = event.get("hook_event_name") if isinstance(event, dict) else None
    if name not in ("SessionStart", "UserPromptSubmit"):
        return {}
    return {"hookSpecificOutput": {"hookEventName": name, "additionalContext": CONTEXT}}


if __name__ == "__main__":
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        event = None
    json.dump(response(event), sys.stdout)
