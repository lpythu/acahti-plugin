import importlib.util
import json
from pathlib import Path
import tempfile
import sys
import hashlib
import unittest
import zipfile
import yaml

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

pkg = load("package", ROOT / "scripts/package_workspace.py")
sys.path.insert(0, str(ROOT / "scripts"))
exporter = load("exporter", ROOT / "scripts/export_marketplace.py")
hook = load("reminder", ROOT / "codex/hooks/remind.py")

class ReleaseTests(unittest.TestCase):
    def test_source_and_release_structure(self):
        files, _ = pkg.build(ROOT / "codex", "https://example.com", "Example")
        frontmatter = files["skills/acahti/SKILL.md"].decode().split("---", 2)[1]
        skill = yaml.safe_load(frontmatter)
        self.assertEqual(skill["name"], "acahti")
        self.assertIsInstance(skill["description"], str)
        manifest = json.loads(files[".codex-plugin/plugin.json"])
        self.assertEqual(manifest["name"], "acahti")
        self.assertIn(manifest["mcpServers"].removeprefix("./"), files)
        hooks = json.loads(files["hooks/hooks.json"])["hooks"]
        self.assertEqual(set(hooks), {"SessionStart", "UserPromptSubmit"})
        for event in hooks.values():
            self.assertEqual(event[0]["hooks"][0]["type"], "command")
        workflow = yaml.safe_load((ROOT / ".github/workflows/workspace-release.yml").read_text())
        self.assertIn("publish", workflow["jobs"])

    def test_urls(self):
        for value in ("http://example.com", "https://a:b@example.com", "https://example.com?q=x", "https://example.com/#fragment", "https://example.com:bad", "https://example.com/ bad"):
            with self.assertRaises(ValueError): pkg.endpoint(value)
        self.assertEqual(pkg.endpoint("https://example.com/prefix/"), "https://example.com/prefix/mcp")
        self.assertEqual(pkg.endpoint("https://example.com/prefix/mcp/"), "https://example.com/prefix/mcp")

    def test_workspace_package_and_reproducibility(self):
        files, version = pkg.build(ROOT / "codex", "https://example.com/prefix", "Example")
        self.assertEqual(version, json.loads((ROOT / "codex/.codex-plugin/plugin.json").read_text())["version"].split("+", 1)[0] + "+example.1")
        self.assertEqual(json.loads(files[".mcp.json"])["mcpServers"]["acahti"]["url"], "https://example.com/prefix/mcp")
        self.assertNotIn("This plugin does not bundle", files["skills/acahti/SKILL.md"].decode())
        self.assertNotIn("The generic package has no fixed", files["skills/acahti/SKILL.md"].decode())
        self.assertIn("## Git tags vs image tags", files["skills/acahti/SKILL.md"].decode())
        self.assertFalse(any("__pycache__" in n or n.endswith(".pyc") or "test_" in n for n in files))
        self.assertIn("hooks/remind.py", files)
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d)/"a.zip", Path(d)/"b.zip"
            pkg.write_archive(a, files); pkg.write_archive(b, files)
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with self.assertRaises(FileExistsError): pkg.write_archive(a, files)
            with zipfile.ZipFile(a) as z: self.assertEqual(set(z.namelist()), set(files))

    def test_marketplace_preserves_plugin_id(self):
        config = {"workspace":"Example", "instance":"https://example.com", "pluginId":"Plugin_123abc"}
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            exporter.export(config, output, "a" * 40)
            marketplace = json.loads((output / ".agents/plugins/marketplace.json").read_text())
            entry = marketplace["plugins"][0]
            self.assertEqual(entry["pluginId"], config["pluginId"])
            plugin = output / entry["source"]["path"]
            manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
            self.assertEqual(manifest["version"], json.loads((ROOT / "codex/.codex-plugin/plugin.json").read_text())["version"].split("+", 1)[0] + "+example.git" + "a" * 12)
            metadata = json.loads((output / "build.json").read_text())
            for name, expected in metadata["filesSHA256"].items():
                self.assertEqual(hashlib.sha256((plugin / name).read_bytes()).hexdigest(), expected)
            stale = plugin / "old.txt"
            stale.write_text("stale")
            exporter.export(config, output, "b" * 40)
            self.assertFalse(stale.exists())
        with self.assertRaises(ValueError): exporter.export(config, ROOT, "a" * 40)
        with self.assertRaises(ValueError): exporter.export(config, ROOT / "codex", "a" * 40)

    def test_reminder_only(self):
        for event in ("SessionStart", "UserPromptSubmit"):
            response = hook.response({"hook_event_name":event})
            self.assertEqual(response["hookSpecificOutput"]["hookEventName"], event)
            self.assertNotIn("permissionDecision", response["hookSpecificOutput"])
        for event in ({"hook_event_name":"PreToolUse"}, None, []):
            self.assertEqual(hook.response(event), {})

if __name__ == "__main__": unittest.main()
