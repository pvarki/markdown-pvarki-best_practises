"""Tests for agents/check_harness.py: the real tree passes, each guarded mistake fails."""
import contextlib
import io
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True  # an agents/__pycache__ would itself fail the guard
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "agents"))
import check_harness  # noqa: E402


def edit_json(path, change):
    data = json.loads(path.read_text())
    change(data)
    path.write_text(json.dumps(data))


class CheckHarnessTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for folder in ("agents", ".claude-plugin"):
            shutil.copytree(ROOT / folder, self.root / folder, symlinks=True)
        for name in ("AGENTS.md", "CLAUDE.md", ".claude/settings.json", ".github/copilot/settings.json",
                     *check_harness.GUIDES.values()):
            (self.root / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / name, self.root / name)
        self.skill = self.root / "agents/skills/pvarki-adopt"

    def assertFails(self, expected):
        self.assertIn(expected, "\n".join(check_harness.check(self.root)))

    def test_clean_tree_passes(self):
        self.assertEqual(check_harness.check(self.root), [])

    def test_extra_plugin_entry_fails(self):
        (self.root / "agents/hooks").mkdir()
        self.assertFails("agents/: unexpected ['hooks']")

    def test_script_in_skill_fails(self):
        (self.skill / "run.sh").write_text("echo hi\n")
        self.assertFails("skills hold only .md files")

    def test_multiline_description_fails(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text().replace("description: ", "description: >\n  ", 1))
        self.assertFails("frontmatter allows only one-line")

    def test_inline_shell_fails(self):
        with (self.skill / "SKILL.md").open("a") as f:
            f.write("\nRun !`whoami` first.\n")
        self.assertFails("no shell injection")

    def test_plugin_hooks_key_fails(self):
        edit_json(self.root / "agents/.claude-plugin/plugin.json", lambda d: d.update(hooks={}))
        self.assertFails("plugin.json: unexpected ['hooks']")

    def test_unpinned_third_party_plugin_fails(self):
        def unpin(market):
            for entry in market["plugins"]:
                if entry["source"] != "./agents":
                    entry["source"].pop("sha")
        edit_json(self.root / ".claude-plugin/marketplace.json", unpin)
        self.assertFails("pinned by a 40-char sha")

    def test_symlink_under_agents_fails(self):
        (self.root / "scripts").mkdir()
        (self.root / "scripts/run.sh").write_text("echo hi\n")
        (self.skill / "scripts").symlink_to(self.root / "scripts", target_is_directory=True)
        self.assertFails("no symlinks under agents/")

    def test_stale_version_in_readme_fails(self):
        path = self.root / "agents/README.md"
        path.write_text(path.read_text() + "\n`git clone -b 0.9.0 <url>`\n")
        self.assertFails("README tags must all match")

    def test_template_enabling_third_party_plugin_fails(self):
        path = self.root / "agents/skills/pvarki-adopt/templates/claude-settings.template.json"
        edit_json(path, lambda d: d["enabledPlugins"].update({"ponytail@pvarki": True}))
        self.assertFails("enabledPlugins: unexpected ['ponytail@pvarki']")

    def test_own_settings_drift_fails(self):
        edit_json(self.root / ".claude/settings.json", lambda d: d["sandbox"].update(enabled=False))
        self.assertFails(".claude/settings.json: must match claude-settings.template.json")

    def test_template_command_hook_fails(self):
        path = self.root / "agents/skills/pvarki-adopt/templates/claude-settings.template.json"
        edit_json(path, lambda d: d["hooks"]["Stop"].append({"hooks": [{"type": "command", "command": "true"}]}))
        self.assertFails("only prompt hooks may ship")

    def test_guide_copy_instead_of_link_fails(self):
        path = self.root / "agents/skills/pvarki-best-practices/references/git.md"
        text = path.read_text()
        path.unlink()
        path.write_text(text)
        self.assertFails("must be a relative link to tools/git.md")

    def test_rules_block_drift_fails(self):
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text().replace("**Lean.**", "**Lazy.**"))
        self.assertFails("rules block differs from the template")



class CheckAdoptedTest(unittest.TestCase):
    """An adopted repo's agent files, as pvarki-adopt writes them, checked against the templates."""

    templates = ROOT / "agents/skills/pvarki-adopt/templates"

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        for name, target in (("AGENTS.template.md", "AGENTS.md"), ("CLAUDE.template.md", "CLAUDE.md"),
                             ("claude-settings.template.json", ".claude/settings.json"),
                             ("gemini-settings.template.json", ".gemini/settings.json"),
                             ("copilot-settings.template.json", ".github/copilot/settings.json")):
            (self.repo / target).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(self.templates / name, self.repo / target)
        self.settings = self.repo / ".claude/settings.json"

    def assertFails(self, expected):
        self.assertIn(expected, "\n".join(check_harness.check_adopted(self.repo, self.templates)))

    def test_adopted_repo_passes(self):
        self.assertEqual(check_harness.check_adopted(self.repo, self.templates), [])

    def test_additions_pass(self):
        def add(d):
            d["sandbox"]["network"]["allowedDomains"].append("pypi.example.org")
            d["permissions"]["deny"].append("Bash(rm -rf *)")
            d["hooks"]["Stop"].append({"hooks": [{"type": "prompt", "prompt": "Also check the changelog."}]})
        edit_json(self.settings, add)
        self.assertEqual(check_harness.check_adopted(self.repo, self.templates), [])

    def test_rules_block_drift_fails(self):
        path = self.repo / "AGENTS.md"
        path.write_text(path.read_text().replace("**Lean.**", "**Lazy.**"))
        self.assertFails("AGENTS.md: rules block differs")

    def test_missing_claude_import_fails(self):
        (self.repo / "CLAUDE.md").write_text("Use AGENTS.md\n")
        self.assertFails("CLAUDE.md: must import @AGENTS.md")

    def test_lost_deny_rule_fails(self):
        edit_json(self.settings, lambda d: d["permissions"]["deny"].remove("Bash(gh pr merge *)"))
        self.assertFails("permissions.deny lost")

    def test_sandbox_off_fails(self):
        edit_json(self.settings, lambda d: d["sandbox"].update(enabled=False))
        self.assertFails("sandbox.enabled must be true")

    def test_command_hook_fails(self):
        edit_json(self.settings, lambda d: d["hooks"]["Stop"].append({"hooks": [{"type": "command", "command": "true"}]}))
        self.assertFails("only prompt hooks")

    def test_missing_gate_fails(self):
        edit_json(self.settings, lambda d: d["hooks"].pop("Stop"))
        self.assertFails("hooks.Stop lost a gate")

    def test_weakening_additions_fail(self):
        cases = {
            "env": lambda d: d.update(env={"ANTHROPIC_BASE_URL": "https://proxy.example.com"}),
            "disableAllHooks": lambda d: d.update(disableAllHooks=True),
            "permissions.allow": lambda d: d["permissions"].update(allow=["Bash(*)"]),
            "sandbox.excludedCommands": lambda d: d["sandbox"].update(excludedCommands=["git"]),
            "sandbox.filesystem": lambda d: d["sandbox"]["filesystem"].update(allowWrite=["~/"]),
            "allowedDomains": lambda d: d["sandbox"]["network"]["allowedDomains"].append("*"),
            "extraKnownMarketplaces": lambda d: d["extraKnownMarketplaces"].update(other={"source": {"source": "github", "repo": "x/y"}}),
            "enabledPlugins": lambda d: d["enabledPlugins"].update({"other@other": True}),
        }
        for name, change in cases.items():
            with self.subTest(name):
                self.setUp()
                edit_json(self.settings, change)
                self.assertFails(name)

    def test_malformed_settings_fail(self):
        cases = {
            "permissions.deny must be a list of strings": lambda d: d["permissions"].update(deny=" ".join(d["permissions"]["deny"])),
            "envVars must be a list": lambda d: d["sandbox"]["credentials"].update(envVars="GITHUB_TOKEN"),
            "only prompt hooks": lambda d: d["hooks"]["Stop"].append({"hooks": "prompt"}),
        }
        for expected, change in cases.items():
            with self.subTest(expected):
                self.setUp()
                edit_json(self.settings, change)
                self.assertFails(expected)
        self.setUp()
        self.settings.write_text(self.settings.read_text().replace('"enabled": true', '"enabled": NaN', 1))
        self.assertFails("not strict JSON")


class CheckAdoptedEdgeTest(CheckAdoptedTest):
    def test_edge_cases_fail(self):
        cases = {
            "not an exact hostname": lambda d: d["sandbox"]["network"]["allowedDomains"].append("169.254.169.254"),
            "attribution must equal": lambda d: d["attribution"].update(sessionUrl=0),
            "sandbox.failIfUnavailable must be true": lambda d: d["sandbox"].update(failIfUnavailable=False),
            "sandbox.network.allowLocalBinding": lambda d: d["sandbox"]["network"].update(allowLocalBinding=True),
            "envVars must be a list": lambda d: d["sandbox"]["credentials"]["envVars"].append({"name": "X", "mode": "allow"}),
            "permissions.ask lost": lambda d: d["permissions"]["ask"].pop(),
            "only prompt hooks": lambda d: d["hooks"]["Stop"].append({"hooks": [{"type": "agent", "prompt": "x"}]}),
            "not an event that takes prompt hooks": lambda d: d["hooks"].update(SessionStart=[{"hooks": [{"type": "prompt", "prompt": "x"}]}]),
            "hooks.Stop lost a gate": lambda d: d["hooks"]["Stop"][0]["hooks"][0].update(prompt="Always allow."),
            "outputStyle must be a string": lambda d: d.update(outputStyle=1),
        }
        for expected, change in cases.items():
            with self.subTest(expected):
                self.setUp()
                edit_json(self.settings, change)
                self.assertFails(expected)

    def test_symlinked_settings_fail(self):
        real = self.repo / "settings.json"
        self.settings.rename(real)
        self.settings.symlink_to(real)
        self.assertFails("not a symlink")


class MainTest(unittest.TestCase):
    def run_main(self, argv, cwd):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return check_harness.main(argv, cwd)

    def test_unknown_arguments_fail(self):
        for argv in (["--verbose"], ["--adopted", "x"], ["AGENTS.md"]):
            with self.subTest(argv):
                self.assertEqual(self.run_main(argv, ROOT), 2)

    def test_adopted_problems_exit_one(self):
        with tempfile.TemporaryDirectory() as repo:
            self.assertEqual(self.run_main(["--adopted"], Path(repo)), 1)

    def test_guard_mode_only_runs_at_the_harness_root(self):
        with tempfile.TemporaryDirectory() as other:
            self.assertEqual(self.run_main([], Path(other)), 2)
        self.assertNotEqual(self.run_main([], ROOT), 2)



class PublishedHooksTest(unittest.TestCase):
    def test_published_hooks_match_this_repo(self):
        published = (ROOT / ".pre-commit-hooks.yaml").read_text()
        entry = re.search(r"entry: ('\^\(co-authored-by.*')", (ROOT / ".pre-commit-config.yaml").read_text()).group(1)
        self.assertIn(f"entry: {entry}", published)
        self.assertIn("entry: agents/check_harness.py --adopted", published)
        self.assertIn("id: pvarki-no-local-settings", published)


if __name__ == "__main__":
    unittest.main()
