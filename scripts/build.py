"""Validate and package the shared skill for Claude and OpenAI."""

import json
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def read_json(name):
    return json.loads((ROOT / name).read_text())


def build():
    portable = read_json("plugin.json")
    claude = read_json(".claude-plugin/plugin.json")
    for key in ("name", "version", "description", "author", "license", "repository"):
        if portable[key] != claude[key]:
            raise ValueError(f"Manifest mismatch: {key}")
    version = portable["version"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("Expected a stable semantic version")
    if len(portable["extensions"]["com.openai"]["interface"]["shortDescription"]) > 30:
        raise ValueError("OpenAI subtitle exceeds 30 characters")
    if portable["$schema"] != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Incorrect portable plugin schema")
    connections = read_json("mcp.json")
    if connections["$schema"] != "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json":
        raise ValueError("Incorrect portable MCP schema")
    server = connections["mcpServers"]["remember-this"]
    legacy = read_json(".mcp.json")["mcpServers"]["remember-this"]
    if server["url"] != legacy["url"] or server["url"] != "https://remember-this.io/mcp":
        raise ValueError("MCP endpoints differ")
    if server["type"] != "streamable-http" or legacy["type"] != "http":
        raise ValueError("Incorrect transport")
    auth = server["extensions"]["com.openai"]["auth"]
    if auth != {"type": "oauth", "client": {"mode": "dcr"}, "defaultScopes": ["mcp:use"]}:
        raise ValueError("Expected OAuth with dynamic client registration")
    review = portable.get("extensions", {}).get("com.openai", {}).get("review")
    if review is not None:
        cases = review["test_cases"]
        for kind, count in (("positive", 5), ("negative", 3)):
            if len(cases[kind]) != count:
                raise ValueError(f"Expected {count} {kind} review cases")
            required = ["description", "prompt"]
            if kind == "positive":
                required += ["tools_triggered", "expected_behavior"]
            for case in cases[kind]:
                if any(not isinstance(case.get(key), str) or not case[key].strip() for key in required):
                    raise ValueError(f"Incomplete {kind} review case")
        if not review["demo_recording_url"].startswith("https://"):
            raise ValueError("Expected an HTTPS demo recording URL")
        interface = portable["extensions"]["com.openai"]["interface"]
        for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
            if not interface.get(field, "").startswith("https://"):
                raise ValueError(f"Missing public listing URL: {field}")
        if portable.get("apps") is not None or portable["extensions"]["com.openai"].get("apps") is not None:
            raise ValueError("Public uploads cannot reference an existing app")
    skill_path = "skills/remember-and-recall/SKILL.md"
    skill = (ROOT / skill_path).read_text()
    if not skill.startswith("---\nname: remember-and-recall\ndescription: ") or "\n---\n" not in skill[4:]:
        raise ValueError("Missing skill metadata")
    shared = [skill_path, "assets/icon.png", "LICENSE"]
    targets = {
        "claude": [".claude-plugin/plugin.json", ".mcp.json"],
        "openai": ["plugin.json", "mcp.json"],
    }
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    for target, manifests in targets.items():
        files = sorted(shared + manifests)
        suffix = "-submission" if target == "openai" and review is not None else ""
        archive = output / f"remember-this-{target}-{version}{suffix}.zip"
        with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
            for name in files:
                path = ROOT / name
                if path.is_symlink() or not path.is_file():
                    raise ValueError(f"Not a regular file: {name}")
                bundle.write(path, name)
        with ZipFile(archive) as bundle:
            if bundle.namelist() != files or bundle.testzip() is not None:
                raise ValueError(f"Invalid archive: {archive}")
            for name in manifests:
                json.loads(bundle.read(name))
            if bundle.read(skill_path) != skill.encode():
                raise ValueError("Packaged skill differs from source")
        print(f"Validated {archive.relative_to(ROOT)} ({len(files)} files)")


if __name__ == "__main__":
    build()
