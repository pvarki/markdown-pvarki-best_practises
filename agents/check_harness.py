#!/usr/bin/env python3
"""Keep the agent harness to reviewed, inert content.

agents/ is the plugin root: only the listed entries may live there, so nothing
that runs code (hooks, MCP or LSP servers, binaries, commands, subagents) can
ship, and templates carry only prompt hooks, which run no code. Third-party
plugins must be pinned to a full commit SHA, and templates enable only
first-party plugins. Skills use only Agent Skills spec keys so the same folders
work in every agent and upload to claude.ai. This repo's own AGENTS.md,
CLAUDE.md and agent settings must match the templates, the best-practices skill must
link to the root guides, and the release version must agree
everywhere it is written.
"""
import json
import re
import sys
from pathlib import Path

PLUGIN_KEYS = {"name", "version", "description", "author", "homepage", "repository",
               "license", "keywords"}
MARKET_KEYS = {"$schema", "name", "description", "owner", "plugins"}
ENTRY_KEYS = {"name", "source", "description", "version"}
TEMPLATE_KEYS = {
    "claude-settings.template.json": {"attribution", "outputStyle", "extraKnownMarketplaces",
                                      "enabledPlugins", "sandbox", "permissions", "hooks"},
    "gemini-settings.template.json": {"context"},
    "copilot-settings.template.json": {"includeCoAuthoredBy"},
}
PERMISSION_KEYS = {"ask", "deny", "disableBypassPermissionsMode", "disableAutoMode"}
GUIDES = {"general.md": "README.md", "rationality.md": "rationality/README.md", "git.md": "tools/git.md",
          "ci.md": "tools/ci.md", "logging.md": "tools/logging.md", "databases.md": "tools/databases.md",
          "python.md": "frameworks-languages/python.md", "typescript.md": "frameworks-languages/typescript.md",
          "rust.md": "frameworks-languages/rust.md", "c_and_cpp.md": "frameworks-languages/c_and_cpp.md"}
BLOCK = re.compile(r"<!-- BEGIN pvarki-agent-standard.*?<!-- END pvarki-agent-standard -->", re.S)


def entries(folder):
    return [p for p in folder.iterdir() if not (p.name == ".DS_Store" and p.is_file())]


def check(root):
    """Return the problems in the repo at root; an empty list means it is clean."""
    plugin = root / "agents"
    templates = plugin / "skills/pvarki-adopt/templates"
    errors = []

    def extra(found, allowed, where):
        if set(found) - allowed:
            errors.append(f"{where}: unexpected {sorted(set(found) - allowed)}")

    allowed_entries = {
        root / ".claude-plugin": {"marketplace.json"},
        plugin: {"README.md", "check_harness.py", ".claude-plugin", "skills"},
        plugin / ".claude-plugin": {"plugin.json"},
    }
    for folder, allowed in allowed_entries.items():
        extra([p.name for p in entries(folder)], allowed, f"{folder.relative_to(root)}/")
    refs = plugin / "skills/pvarki-best-practices/references"
    for f in plugin.rglob("*"):
        if f.is_symlink() and not (f.parent == refs and f.name in GUIDES):
            errors.append(f"{f.relative_to(root)}: no symlinks under agents/ except the guide links")

    extra(json.loads((plugin / ".claude-plugin/plugin.json").read_text()), PLUGIN_KEYS, "plugin.json")
    market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
    extra(market, MARKET_KEYS, "marketplace.json")
    for entry in market["plugins"]:
        extra(entry, ENTRY_KEYS, f"marketplace.json {entry['name']}")
        src = entry["source"]
        if src == "./agents":
            continue
        if not (isinstance(src, dict) and src.get("source") == "url" and set(src) <= {"source", "url", "ref", "sha"}
                and src.get("url", "").startswith("https://") and re.fullmatch(r"[0-9a-f]{40}", src.get("sha", ""))):
            errors.append(f"marketplace.json {entry['name']}: third-party source must be an https url pinned by a 40-char sha")

    for skill in sorted(p for p in entries(plugin / "skills")):
        for f in skill.rglob("*") if skill.is_dir() else [skill]:
            if f.is_file() and f.name != ".DS_Store" and not (
                    f.suffix == ".md" or (f.parent.name == "templates" and f.suffix == ".json")):
                errors.append(f"{f.relative_to(root)}: skills hold only .md files (and .json templates)")
        text = (skill / "SKILL.md").read_text() if (skill / "SKILL.md").is_file() else ""
        if not text.startswith("---\n"):
            errors.append(f"{skill.relative_to(root)}: needs a SKILL.md starting with frontmatter")
            continue
        front = text.split("---")[1]
        bad = [line for line in front.strip("\n").splitlines()
               if not re.fullmatch(r"(name|description|license): \S.*", line)]
        if bad:
            errors.append(f"{skill.name}/SKILL.md: frontmatter allows only one-line name, description, license: {bad}")
        fields = dict(re.findall(r"^(name|description): (.+)$", front, re.M))
        if fields.get("name") != skill.name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", skill.name):
            errors.append(f"{skill.name}/SKILL.md: name must equal the folder and be kebab-case")
        if not 0 < len(fields.get("description", "")) <= 200:
            errors.append(f"{skill.name}/SKILL.md: description must be 1-200 chars")
        if re.search(r"```!|(?<![A-Za-z0-9_])!`", text):
            errors.append(f"{skill.name}/SKILL.md: no shell injection (!` or ```!)")

    for name, allowed in TEMPLATE_KEYS.items():
        data = json.loads((templates / name).read_text())
        extra(data, allowed, name)
        extra(data.get("permissions", {}), PERMISSION_KEYS, f"{name} permissions")
        extra(data.get("sandbox", {}), {"enabled", "failIfUnavailable", "filesystem", "network", "credentials"}, f"{name} sandbox")
        for event, groups in data.get("hooks", {}).items():
            kinds = {str(h.get("type")) for g in groups for h in g.get("hooks", [])}
            if kinds - {"prompt"}:
                errors.append(f"{name} hooks.{event}: only prompt hooks may ship, not {sorted(kinds - {'prompt'})}")
        extra(data.get("extraKnownMarketplaces", {}), {"pvarki"}, f"{name} extraKnownMarketplaces")
        extra(data.get("enabledPlugins", {}), {f"{e['name']}@pvarki" for e in market["plugins"] if e["source"] == "./agents"},
              f"{name} enabledPlugins")

    block = BLOCK.search((templates / "AGENTS.template.md").read_text())
    if (root / "AGENTS.md").exists():
        ours = BLOCK.search((root / "AGENTS.md").read_text())
        if not (block and ours and ours.group(0) == block.group(0)):
            errors.append("AGENTS.md: rules block differs from the template")
    if (root / "CLAUDE.md").exists() and (root / "CLAUDE.md").read_text() != (templates / "CLAUDE.template.md").read_text():
        errors.append("CLAUDE.md: differs from the template")
    for path, name, drop in ((".claude/settings.json", "claude-settings.template.json",
                              {"enabledPlugins", "extraKnownMarketplaces"}),
                             (".github/copilot/settings.json", "copilot-settings.template.json", set())):
        want = {k: v for k, v in json.loads((templates / name).read_text()).items() if k not in drop}
        if not (root / path).is_file() or json.loads((root / path).read_text()) != want:
            errors.append(f"{path}: must match {name}")

    extra([p.name for p in refs.glob("*")] if refs.is_dir() else [], set(GUIDES), "pvarki-best-practices/references")
    for link, source in GUIDES.items():
        path = refs / link
        if not (path.is_symlink() and str(path.readlink()) == f"../../../../{source}" and (root / source).is_file()):
            errors.append(f"pvarki-best-practices/references/{link}: must be a relative link to {source}")
    version = json.loads((plugin / ".claude-plugin/plugin.json").read_text())["version"]
    ref = json.loads((templates / "claude-settings.template.json").read_text())["extraKnownMarketplaces"]["pvarki"]["source"]["ref"]
    tags = set(re.findall(r"(?<!≥ )(?<![\d.])\d+\.\d+\.\d+", (plugin / "README.md").read_text()))
    if not (block and f"pvarki-agent-standard {version} -->" in block.group(0) and ref == version and tags == {version}):
        errors.append(f"plugin.json {version}: template marker, settings ref and README tags must all match it")
    return errors


ADOPTED_KEYS = TEMPLATE_KEYS["claude-settings.template.json"] | {"$schema"}
PROMPT_HOOK_KEYS = {"type", "prompt", "if", "continueOnBlock", "timeout", "model"}
HOSTNAME = re.compile(r"([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z]([a-z0-9-]*[a-z0-9])?(:[0-9]{1,5})?")
PROMPT_EVENTS = {"PreToolUse", "PostToolUse", "PostToolUseFailure", "PostToolBatch", "Stop", "SubagentStop",
                 "TaskCompleted", "TaskCreated", "TeammateIdle", "UserPromptExpansion", "UserPromptSubmit",
                 "PermissionDenied", "PermissionRequest"}


def strict_json(path):
    def reject(token):
        raise ValueError(f"{token} is not JSON")
    return json.loads(path.read_text(), parse_constant=reject)


def canon(value):
    return json.dumps(value, sort_keys=True)


def prompt_hook(h):
    return (isinstance(h, dict) and set(h) <= PROMPT_HOOK_KEYS and h.get("type") == "prompt"
            and isinstance(h.get("prompt"), str) and isinstance(h.get("if", ""), str)
            and isinstance(h.get("model", ""), str) and type(h.get("continueOnBlock", False)) is bool
            and ("timeout" not in h or (type(h["timeout"]) in (int, float) and h["timeout"] > 0)))


def prompt_group(group):
    return (isinstance(group, dict) and set(group) <= {"matcher", "hooks"}
            and isinstance(group.get("matcher", ""), str) and isinstance(group.get("hooks"), list)
            and bool(group["hooks"]) and all(prompt_hook(h) for h in group["hooks"]))


def check_adopted(repo, templates):
    """Return the problems in an adopted repo's agent files; an empty list means they keep the harness.

    .claude/settings.json may hold only the template's keys. Lists may add entries but not drop the
    template's, and allowedDomains may add exact hostnames. Anything else that could weaken it fails.
    """
    errors = []
    block = BLOCK.search((templates / "AGENTS.template.md").read_text())
    ours = BLOCK.search((repo / "AGENTS.md").read_text()) if (repo / "AGENTS.md").is_file() else None
    if not (block and ours and ours.group(0) == block.group(0)):
        errors.append("AGENTS.md: rules block differs from the harness release")
    claude = repo / "CLAUDE.md"
    if not (claude.is_file() and "@AGENTS.md" in claude.read_text().splitlines()):
        errors.append("CLAUDE.md: must import @AGENTS.md")
    want = json.loads((templates / "claude-settings.template.json").read_text())
    path = repo / ".claude/settings.json"
    if (repo / ".claude").is_symlink() or path.is_symlink():
        return errors + [".claude/settings.json: must be a regular file, not a symlink"]
    try:
        have = strict_json(path) if path.is_file() else {}
    except ValueError as e:
        return errors + [f".claude/settings.json: not strict JSON ({e})"]

    def bad(message):
        errors.append(f".claude/settings.json: {message}")

    def obj(value, where, allowed):
        if not isinstance(value, dict):
            bad(f"{where or 'the file'} must be an object")
            return {}
        if set(value) - allowed:
            bad(f"keys the harness doesn't allow: {[f'{where}.{k}' if where else k for k in sorted(set(value) - allowed)]}")
        return value

    def strings(value, where, keep):
        if not (isinstance(value, list) and all(isinstance(x, str) for x in value)):
            bad(f"{where} must be a list of strings")
            return []
        if [x for x in keep if x not in value]:
            bad(f"{where} lost {[x for x in keep if x not in value]}")
        return value

    have = obj(have, "", ADOPTED_KEYS)
    for key in ("attribution", "extraKnownMarketplaces", "enabledPlugins"):
        if canon(have.get(key)) != canon(want[key]):
            bad(f"{key} must equal the harness template")
    for key in ("outputStyle", "$schema"):
        if key in have and not isinstance(have[key], str):
            bad(f"{key} must be a string")
    permissions = obj(have.get("permissions", {}), "permissions", {"ask", "deny"})
    for key in ("ask", "deny"):
        strings(permissions.get(key, []), f"permissions.{key}", want["permissions"][key])
    sandbox = obj(have.get("sandbox", {}), "sandbox", set(want["sandbox"]))
    for key in ("enabled", "failIfUnavailable"):
        if sandbox.get(key) is not True:
            bad(f"sandbox.{key} must be true")
    filesystem = obj(sandbox.get("filesystem", {}), "sandbox.filesystem", {"denyWrite"})
    strings(filesystem.get("denyWrite", []), "sandbox.filesystem.denyWrite", want["sandbox"]["filesystem"]["denyWrite"])
    network = obj(sandbox.get("network", {}), "sandbox.network", {"allowedDomains"})
    for host in strings(network.get("allowedDomains", []), "sandbox.network.allowedDomains", []):
        if not HOSTNAME.fullmatch(host):
            bad(f"sandbox.network.allowedDomains: {host!r} is not an exact hostname")
    env = obj(sandbox.get("credentials", {}), "sandbox.credentials", {"envVars"}).get("envVars", [])
    if not (isinstance(env, list) and all(isinstance(e, dict) and set(e) == {"name", "mode"}
                                          and isinstance(e["name"], str) and e["mode"] == "deny" for e in env)):
        bad("sandbox.credentials.envVars must be a list of {name, mode: deny} entries")
    elif [e for e in want["sandbox"]["credentials"]["envVars"] if e not in env]:
        bad(f"sandbox.credentials.envVars lost {[e for e in want['sandbox']['credentials']['envVars'] if e not in env]}")
    hooks = have.get("hooks", {})
    if not isinstance(hooks, dict):
        bad("hooks must be an object")
        hooks = {}
    for event, groups in hooks.items():
        if event not in PROMPT_EVENTS:
            bad(f"hooks.{event}: not an event that takes prompt hooks")
        elif not (isinstance(groups, list) and all(prompt_group(g) for g in groups)):
            bad(f"hooks.{event}: only prompt hooks ({{matcher?, hooks: [{{type: prompt, prompt, ...}}]}})")
    for event, groups in want.get("hooks", {}).items():
        current = hooks.get(event)
        kept = {canon(g) for g in current} if isinstance(current, list) else set()
        if any(canon(g) not in kept for g in groups):
            bad(f"hooks.{event} lost a gate")
    return errors


def main(argv, cwd):
    here = Path(__file__).resolve().parent
    if argv == ["--adopted"]:
        problems, ok = check_adopted(cwd, here / "skills/pvarki-adopt/templates"), "agent files keep the pvarki harness"
    elif argv == [] and cwd.resolve() == here.parent:
        problems, ok = check(here.parent), "harness ok"
    else:
        print("usage: check_harness.py --adopted (in an adopted repo), or no arguments at the harness repo root",
              file=sys.stderr)
        return 2
    print("\n".join(problems) or ok)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:], Path.cwd()))
