#!/usr/bin/env python3
"""Export a generated marketplace tree for the dedicated workspace release branch."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

from package_workspace import ROOT, build, encode


def export(config, output, commit):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("source commit must be a full Git SHA")
    plugin_id = config["pluginId"]
    if not re.fullmatch(r"[Pp]lugin_[A-Za-z0-9]+", plugin_id):
        raise ValueError("invalid workspace plugin ID")
    files, version = build(ROOT / "codex", config["instance"], config["workspace"], "git" + commit[:12])
    # This tree is generated output, never a source checkout.
    output = output.resolve()
    if output == ROOT or output.is_relative_to(ROOT / "codex") or ROOT.is_relative_to(output):
        raise ValueError("output must not replace the source checkout")
    target = output / "plugins" / "acahti"
    if target.exists():
        shutil.rmtree(target)
    for name, data in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    marketplace = output / ".agents/plugins/marketplace.json"
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    marketplace.write_bytes(encode({
        "name": "acahti-" + config["workspace"].lower(),
        "interface": {"displayName": config["workspace"] + " Acahti"},
        "plugins": [{"name": "acahti", "pluginId": plugin_id,
                     "source": {"source": "local", "path": "./plugins/acahti"},
                     "category": "Productivity",
                     "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}}]
    }))
    # Workspace import preserves existing policy; repository policy is only a local default.
    metadata = {"sourceCommit": commit, "pluginVersion": version, "pluginId": plugin_id,
                "filesSHA256": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}}
    (output / "build.json").write_bytes(encode(metadata))
    (output / "README.md").write_text(
        "# SAIDC Acahti workspace release\n\n"
        "Generated from https://github.com/lpythu/acahti-plugin/tree/" + commit + ".\n\n"
        "Do not edit this branch directly. Change main and let the workspace-release workflow rebuild it.\n"
        "The marketplace maps the existing workspace plugin ID; installation policies are managed in ChatGPT.\n"
    )
    print(f"Exported {version} to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "workspaces/saidc.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    export(json.loads(args.config.read_text()), args.output, args.commit)
