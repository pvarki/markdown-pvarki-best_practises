---
name: pvarki-review
description: The pvarki review standard, built from what our senior reviewers reject. Use when reviewing a diff, branch or PR in a pvarki repo, or before asking for review.
---

# pvarki-review

Review the whole branch: `git diff origin/<default>...HEAD`. In Claude Code,
pass the range, `/code-review origin/<default>...HEAD`; without a target it
reviews only commits ahead of the upstream, and our branches have none.

Report only real problems, most severe first, each with file:line, what breaks
and a concrete fix. If there are none, say "no findings".

1. Correctness: logic errors, unhandled errors, edge cases, broken contracts,
   un-awaited async calls, and checks (healthchecks, CI waits, tests) that
   cannot fail.
2. Security: new process execution, secrets, auth or permission changes,
   hand-rolled security primitives, unvalidated input or data spliced into
   shell or queries, unpinned dependencies.
3. Architecture: boundary crossings per AGENTS.md (core naming a product, edge
   reading core internals).
4. Tests: behaviour changes without a test that fails without them, weakened
   checks, or new warnings.
5. Simplicity: dead or commented-out code, debug leftovers, copy-paste, long
   shell scripts that belong in the repo's language, or code the standard
   library or an existing dependency already provides.
6. Config: hardcoded hosts, ports or deployment names; one concept under two
   names; a new or renamed setting missing from docs, deployment or CI, or
   breaking the default path when unset or empty.
7. Release: a missing or wrong-level version bump; image tags, versions or pins
   that match no built artifact; a submodule pointer not on the submodule's
   merged default branch; a new workflow without `workflow_dispatch`.
8. Logging: `print` or debug output instead of the logger; security events
   logged below audit level.
9. Standards: anything else the language guide in `pvarki-best-practices`
   rules out.


Check the diff against the "Crown jewels" section of AGENTS.md. Run
`pvarki-crown-jewels` only when asked, or when the change adds a jewel or a
trust boundary.

## Gotchas

- History is reviewed too: typo or fixup commits, `fix:` commits for work the
  same branch introduced, build-trigger commits and intermediate submodule
  bumps get squashed into the commit they belong to before review. A branch
  that holds more than one reviewable slice gets split.
- Never post the review on the PR unless asked.
