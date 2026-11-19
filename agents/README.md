# AI agent harness

Rules, gates and a small skill library that make coding agents deliver what we
require, however they plan and ship. Claude Code gets all of it in one step;
other agents get the rules, the skills and the same CI and branch checks.
Everything lives in this `agents/` folder, which is also the Claude Code plugin
root.

## Library

| Part | What it does | Where |
|---|---|---|
| Rules | The shared block every repo vendors at the top of its `AGENTS.md`: security, architecture, git, done means verified | [`AGENTS.template.md`][agents-template] |
| Gates | Claude Code prompt hooks on the agent's own actions: plan, commit, PR, finish. A failed gate sends its reason back and Claude fixes it | [`claude-settings.template.json`][settings-template] |
| `pvarki-adopt` | Installs or updates all of this in a repo | [skill][adopt] |
| `pvarki-crown-jewels` | Threat model or security review: crown jewels, attack paths, chokepoints | [skill][crown] |
| `pvarki-review` | The review standard, built from what our reviewers reject | [skill][review] |
| `pvarki-best-practices` | The org's standards: rationality, general practices, git, CI, logging, databases, Python, TypeScript, Rust, C/C++. Links to this repo's guides, no copies | [skill][bestpractices] |
| Agent settings | Ask and deny rules, no attribution; Copilot and Gemini settings | [`templates/`][templates] |
| Guard | Keeps the plugin to reviewed text and prompt hooks; CI runs it | [`check_harness.py`][guard] |
| Hooks | `pvarki-agent-files` keeps an adopted repo's rules block and Claude settings to the release; `pvarki-no-attribution` rejects AI attribution lines; `pvarki-no-local-settings` keeps personal settings out of git. Adopted repos add them to their config-ci-library pre-commit config, pinned by commit, and its CI runs them | [`.pre-commit-hooks.yaml`][hooks] |
| Marketplace | The `pvarki` plugin, plus ponytail (opt-in, pinned by sha) | [`marketplace.json`][market] |

## What we ensure, and where

Agents plan and ship natively. We check the outcome at the moment the agent
acts, and again where no agent can skip the check.

| Outcome | In the agent loop (Claude Code) | For every agent |
|---|---|---|
| Plans name the layer, boundary crossings, security delta, commits and checks | plan gate | review |
| Conventional, brief commits without attribution; hooks never skipped | commit gate, deny rules | commit-msg hooks, including `pvarki-no-attribution`; CI doesn't check messages yet |
| Agent files keep the harness: rules block, gates, deny rules | `pvarki-adopt` | `pvarki-agent-files`, run in CI by config-ci-library's `general-check`; what binds is code-owner review of `.claude/` and `.pre-commit-config.yaml` |
| Checks run and reported before "done" | finish gate | required CI checks |
| Changes to what's worth protecting are called out; full security reviews on request | rules, the "Crown jewels" list in each `AGENTS.md` | `pvarki-review`; code owners |
| Draft PRs from the org template, with release notes | PR gate | the PR template |
| One version bump per PR | rules | `validate-bumpversion` in [config-ci-library][cicl] |
| Architecture boundaries | rules, plan gate | a tripwire check in CI (to build) |
| Code follows the org's best practices | rules, `pvarki-best-practices`, `pvarki-review` | config-ci-library's checks; review |
| Reviewed merges only, no direct pushes | deny rules | branch rulesets: PR, code-owner review, last-push approval, required checks, no bypass |

Gates are prompts judged by a small model: they catch mistakes early, but they
can be wrong, and local hooks can be skipped. What binds every agent is CI plus
the rulesets.

## Quick start

Every contributor, whatever agent you use:

```bash
git config --global branch.autoSetupMerge simple   # new branches never track origin/main
uv tool install prek   # once per machine, so hooks never run a binary from the repo
prek install --hook-type pre-commit --hook-type commit-msg   # in each clone
```

Turn off your tool's AI co-author or attribution setting. Outside this repo,
no hook rejects the trailer yet.

| Agent | Rules | Skills | Gates |
|---|---|---|---|
| Claude Code ≥ 2.1.285 | `CLAUDE.md` imports `AGENTS.md` | Adopted repos: trust the folder and the `pvarki` plugin loads. Elsewhere: `/plugin marketplace add https://github.com/pvarki/markdown-pvarki-best_practises.git#1.0.0`, then `/plugin install pvarki@pvarki` | from the repo's `.claude/settings.json` |
| Codex, Cursor, Copilot, Junie | read `AGENTS.md` natively | link the skills into `~/.agents/skills/` (below) | CI and rulesets only |
| Gemini CLI | `.gemini/settings.json` points it at `AGENTS.md` | `~/.agents/skills/` | CI and rulesets only |
| Antigravity | reads `AGENTS.md` natively | link the skills into its skills folder | CI and rulesets only |

Gemini and Antigravity rows follow their vendors' docs; they aren't tested
here.

Skills for any agent:

```bash
git clone --depth 1 --branch 1.0.0 https://github.com/pvarki/markdown-pvarki-best_practises ~/.pvarki-harness
mkdir -p ~/.agents/skills && ln -sfn ~/.pvarki-harness/agents/skills/* ~/.agents/skills/
```

To update to release `X.Y.Z`:

```bash
git -C ~/.pvarki-harness fetch --depth 1 origin tag X.Y.Z && git -C ~/.pvarki-harness checkout X.Y.Z
ln -sfn ~/.pvarki-harness/agents/skills/* ~/.agents/skills/
```

On claude.ai, zip a skill folder so the folder sits at the zip root
(`pvarki-review.zip` → `pvarki-review/SKILL.md`) and upload it under
Customize › Skills, or have an org owner provision it.

Ponytail (lazy-senior-dev mode) is optional; its principles are already in the
rules block. Its hooks run node at session start and on every prompt. To use it in one
repo in Claude Code:
`claude plugin install ponytail@pvarki --scope local`.

## Adopt a repo

Give any agent this prompt:

> Clone pvarki/markdown-pvarki-best_practises at tag 1.0.0 into a temporary
> folder with git (not a web fetch tool) and follow
> `agents/skills/pvarki-adopt/SKILL.md` for this repo. New branch; don't push.

With the plugin in Claude Code, run `/pvarki-adopt`. The [skill][adopt] lists
every file it writes: `AGENTS.md`, `CLAUDE.md` and the per-agent settings,
gates included. Review the result like any other PR. To update a repo later,
run adopt again with the new tag.

## Security setup

- **Security reviews and threat models** start from what is worth protecting:
  `/pvarki-crown-jewels` ranks the crown jewels, maps the attack paths that
  reach them, verifies each path and fixes at the chokepoints.
- **Keys that must always hold go in your user settings**
  (`~/.claude/settings.json`). A checkout can replace a repo's
  `.claude/settings.json`, and Claude Code reads it only when started at the
  repo root. Copy the template's credential deny rules there at least.
- **Bypass mode** (`--dangerously-skip-permissions`) skips every permission
  prompt and Claude Code's protected-path checks. The gates still block, and
  the template's deny rules keep Claude's file tools out of credential files,
  `.claude/settings*.json`, `.mcp.json`, `.git/hooks` and `.git/config`.
  Shell commands are not confined: use it where a mistake can't reach
  credentials you care about.
- **Credentials.** Agents act as whoever is logged in. Don't run agents under an
  account that can bypass branch protection or change repo settings. Use a
  normal account, or a fine-grained token, for agent work. The deny and ask
  rules on `git` and `gh` slow an agent down, but other command forms get past
  them; what stops a merge or a push to `main` is the branch ruleset.
- **Extensions.** Install plugins, skills and MCP servers only from this
  marketplace, or after reading their hooks, MCP config and scripts:
  - pin versions: no `@latest`, no `curl | bash`;
  - never let a tool rewrite your API endpoint (`ANTHROPIC_BASE_URL` and the
    like).
- **Untrusted PRs.** Agents load repo config (hooks, settings, skills, MCP) from
  whatever is checked out, and headless runs (`claude -p`) trust the folder
  without asking. Never run an agent on an unreviewed PR's checkout. First read
  its changes to `AGENTS.md`, `CLAUDE.md`, the agent config paths in the rules
  block's Security section, `.vscode/`, `.devcontainer/` and the pre-commit
  config yourself.
  - Checking out a branch in a clone or worktree you already trust loads its
    hooks without a dialog. Read its agent config first, or use a fresh clone.
  - For headless or CI runs on unreviewed code, pass `--setting-sources user`
    and `--settings '{"sandbox": {"enabled": true, "failIfUnavailable": true,
    "allowUnsandboxedCommands": false}}'`.
  - A `pull_request` workflow runs from the branch as soon as it's pushed. Keep
    CODEOWNERS on `.github/`, least-privilege `permissions:`, and secrets in
    environments that require a reviewer.
- **Instructions come from local, reviewed files only.** Never tell an agent to
  "fetch this URL and follow it" at runtime:
  - web fetch tools return a summary, not the file;
  - the page can change under you.

## Contributing

- **Guides:** they live only in this repo's folders. The skill's
  `references/` holds relative links to them, which Claude Code dereferences
  when it installs the plugin; add a link when agents need a new guide.
- **Rules:** change them only in the [template][agents-template], by PR;
  adopted repos vendor it, and this repo's `AGENTS.md` must match it.
- **Gates:** prompt hooks only, no command, http or agent hooks. Each prompt
  must be decidable from the hook's input alone; anything that needs to run
  code belongs in CI.
- **Skills:** one folder each, named `pvarki-*`, with a `SKILL.md` that holds
  `name` (the folder name), `description` (≤200 chars, says when to use it)
  and optionally `license`, nothing else, so it works in every agent and on
  claude.ai. Add a Gotchas section; stay under 200 lines; give every
  tool-specific command a generic fallback; no scripts, hooks, `allowed-tools`
  or `` !` `` shell lines. Ship knowledge the agent doesn't have, not
  procedures it already follows.
- **Third-party plugins** enter the marketplace only pinned to a reviewed
  commit (`sha`). To bump one, open a PR after reading the upstream diff.

[`check_harness.py`][guard] enforces the shape of all of this in CI.

## Releases

Tag `X.Y.Z` ([git guide][git]). The same PR bumps the `version` in
`agents/.claude-plugin/plugin.json`, the template's BEGIN marker, the `ref` in
`claude-settings.template.json` and the tag in this file.

## Why it looks like this

- **Agents plan and ship; we gate outcomes.** Teaching an agent a procedure it
  already follows adds nothing. Checking what we require, at the moment it
  acts, does.
- **Prose guides; machines enforce.** Agent instruction files are context, not
  enforced configuration ([Claude Code memory docs][cc-memory]). So the rules
  that matter most are also gates, hooks, CI checks and rulesets.
- **The harness knows config-ci-library, not the reverse.** Adopted repos run
  the harness's hooks through config-ci-library's CI, so config-ci-library
  stays generic.
- **Gates run no code.** Prompt hooks are declarative and judged by a model.
  The only code the harness runs in adopted repos is `check_harness.py`
  (standard library, reads files only), pinned by commit.
- **One source for every agent:** [AGENTS.md][agentsmd] and
  [Agent Skills][agentskills] are open formats read by all major coding agents.
- **Lean, never at the expense of security:** [ponytail][ponytail] for code,
  plus the rules block's Security section.

[agents-template]: ./skills/pvarki-adopt/templates/AGENTS.template.md
[settings-template]: ./skills/pvarki-adopt/templates/claude-settings.template.json
[templates]: ./skills/pvarki-adopt/templates/
[adopt]: ./skills/pvarki-adopt/SKILL.md
[crown]: ./skills/pvarki-crown-jewels/SKILL.md
[review]: ./skills/pvarki-review/SKILL.md
[bestpractices]: ./skills/pvarki-best-practices/SKILL.md
[guard]: ./check_harness.py
[hooks]: ../.pre-commit-hooks.yaml
[market]: ../.claude-plugin/marketplace.json
[cicl]: https://github.com/pvarki/config-ci-library
[git]: ../tools/git.md
[agentskills]: https://agentskills.io/specification
[agentsmd]: https://agents.md/
[cc-memory]: https://code.claude.com/docs/en/memory
[ponytail]: https://github.com/DietrichGebert/ponytail
