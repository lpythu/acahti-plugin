#!/usr/bin/env python3
"""Build a versioned workspace archive from current Codex sources (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, urlunsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def endpoint(value):
    if any(c.isspace() or ord(c) < 32 for c in value) or "\\" in value:
        raise ValueError("instance URL contains whitespace or a backslash")
    u = urlsplit(value)
    if u.scheme != "https" or not u.hostname or u.username is not None or u.password is not None or u.query or u.fragment:
        raise ValueError("instance must be HTTPS with a host, without credentials, query or fragment")
    _ = u.port  # Reject malformed ports.
    path = u.path.rstrip("/")
    if not path.endswith("/mcp"):
        path += "/mcp"
    return urlunsplit((u.scheme, u.netloc, path, "", ""))


def build(source, instance, workspace, revision="1"):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", workspace):
        raise ValueError("workspace must be a short alphanumeric name, optionally with hyphens")
    if not re.fullmatch(r"[A-Za-z0-9-]+", revision):
        raise ValueError("revision must contain only letters, numbers or hyphens")
    url = endpoint(instance)
    names = [".codex-plugin/plugin.json", "README.md", "hooks/hooks.json", "hooks/remind.py"]
    for folder in ("skills", "assets"):
        names += [p.relative_to(source).as_posix() for p in (source / folder).rglob("*")
                  if p.is_file() and not any(part.startswith(".") or part == "__pycache__" for part in p.relative_to(source).parts)
                  and p.suffix not in (".pyc", ".pyo")]
    files = {}
    for name in sorted(names):
        p = source / name
        if p.is_symlink() or not p.resolve().is_relative_to(source.resolve()):
            raise ValueError(f"source escapes package: {name}")
        files[name] = p.read_bytes()
    source_hashes = {n: hashlib.sha256(b).hexdigest() for n, b in files.items()}
    manifest = json.loads(files[".codex-plugin/plugin.json"])
    version = manifest["version"].split("+", 1)[0] + "+" + workspace.lower() + "." + revision
    manifest["version"] = version
    manifest["mcpServers"] = "./.mcp.json"
    manifest["interface"]["longDescription"] = (
        f"{workspace} workspace edition. MCP endpoint is preconfigured; each member must authorize "
        "the plugin MCP connection with their own OAuth account. Website login does not authorize MCP. "
        "Use MCP first for identity, repositories and CI. Optional trusted hooks provide author reminders."
    )
    files[".codex-plugin/plugin.json"] = encode(manifest)
    files[".mcp.json"] = encode({"mcpServers": {"acahti": {"type": "http", "url": url}}})
    skill = files["skills/acahti/SKILL.md"].decode()
    start = skill.index("## Instance configuration\n")
    end = skill.index("## First use and connection troubleshooting\n", start)
    skill = skill[:start] + f'''## Instance configuration

This {workspace} workspace release bundles the intended MCP endpoint in `.mcp.json`. Reuse that plugin connection. Do not ask members to enter an instance URL or create a duplicate standalone server. Discover its actual runtime identifier; it need not be exactly `acahti`.

Each member must authenticate this MCP connection with their own OAuth account. Workspace installation distributes configuration, not shared credentials. Open the plugin's MCP connection settings to authorize it; ordinary website login is separate. Confirm the intended account with MCP `whoami` before doing work. If multiple instances are ambiguous, ask which to use instead of switching silently.

The administrator updates the endpoint through the workspace packaging command and republishes the release. Do not change the generic source, local Git remotes or credentials to guess a different host. The bundled connection targets desktop-local tasks; check connection availability explicitly for other execution environments.

''' + skill[end:]
    files["skills/acahti/SKILL.md"] = skill.encode()
    files["README.md"] = (f"# Acahti — {workspace} workspace\n\nVersion: `{version}`\n\nMCP endpoint: `{url}`\n\n"
        "## 首次使用\n\n1. 安装插件，打开插件详情 → MCP 服务器 → 连接设置（齿轮）。\n"
        "2. 如果提示未连接，选择 Authenticate / 登录，完成自己的 OAuth 授权。网页登录不等于 MCP 授权，无需发送密码或 Token。\n"
        "3. 返回本地 Codex 任务；工具未刷新时新建任务，发送：通过 MCP 检查我的 Acahti 身份和待处理事项。\n"
        "4. 验收必须成功调用 whoami 和 inbox；失败时提供连接状态/错误，不改用网页查数据。\n\n"
        "## Author 提醒\n\n可在 /hooks 审查并信任提醒 hook，需要 Python 3。它只注入规则，不读取凭据、不改 Git、不强制拦截提交。"
        "Skill 要求 Acahti 提交前核验当前 MCP 身份、按 remote host 限定范围、设置并检查有效 author。\n\n"
        "## 发布维护\n\n从最新通用源码用 scripts/package_workspace.py 重新生成包，不在旧 ZIP 上累积修改。"
        "release.json 记录源码文件哈希和包内文件哈希，用来核对发布内容。每次修改必须使用新版本。\n").encode()
    files["release.json"] = encode({"version": version, "workspace": workspace, "mcpEndpoint": url,
        "sourceFilesSHA256": source_hashes,
        "packageFilesSHA256": {n: hashlib.sha256(b).hexdigest() for n,b in sorted(files.items())}})
    return files, version


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def write_archive(output, files):
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instance", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        files, version = build(ROOT / "codex", args.instance, args.workspace)
        write_archive(args.output, files)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"Built {version}: {args.output.resolve()}")
    print(f"SHA256 {hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
