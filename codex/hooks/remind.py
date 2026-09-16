#!/usr/bin/env python3
"""Inject Acahti guidance without network, credentials, or repository mutations."""
import json
import sys

CONTEXT = (
    "Use MCP first for Acahti work; website login is not MCP OAuth. "
    "Apply author policy only to commits and pushes intended for Acahti, not "
    "every operation in a repository that happens to have an Acahti remote. "
    "Resolve the actual destination; if ambiguous, clarify before changing identity. "
    "For that Acahti target, call fresh whoami and use git_name/git_email via "
    "setup_local. Cover merge/pull-generated commits and check outgoing commits "
    "before push. Preserve original authorship for imported/replayed commits. "
    "Leave non-Acahti targets' identity and workflow unchanged. Load the acahti "
    "skill for details. This is a reminder, not an enforced Git guard."
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
