---
name: pvarki-best-practices
description: pvarki's coding standards for general rules, git, Python, TypeScript, Rust, C/C++, logging and databases. Use when writing, reviewing or planning code, commits or PRs in a pvarki repo.
---

# pvarki-best-practices

The org's best practices, copied from pvarki/markdown-pvarki-best_practises.
Before you write code, read `references/general.md`, `references/rationality.md`
and the guide for each language or area you touch, and follow it:

| Touching | Read |
|---|---|
| anything | `references/general.md` and `references/rationality.md` |
| commits, branches, PRs, versions | `references/git.md` |
| CI, pre-commit, new repos | `references/ci.md` |
| Python | `references/python.md` |
| TypeScript or JavaScript | `references/typescript.md` |
| Rust | `references/rust.md` |
| C or C++ | `references/c_and_cpp.md` |
| logging | `references/logging.md` |
| databases or SQL | `references/databases.md` |

Where a guide and the repo's own config or CI differ, the repo wins; the rules
block's precedence line settles the rest. If a guide looks wrong or stale, say
so instead of silently ignoring it.

## Gotchas

- The guides are written for humans too; skip workstation setup advice that
  doesn't apply to the task.
- Links inside the guides follow the repo's folder layout and don't resolve
  here; the table above names every guide.
