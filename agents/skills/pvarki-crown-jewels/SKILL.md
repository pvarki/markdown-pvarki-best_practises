---
name: pvarki-crown-jewels
description: Crown-jewel threat modelling and security review. Rank what is worth protecting, map attack paths to it, verify, fix at chokepoints. Use for security reviews, threat models or re-scoring findings.
---

# pvarki-crown-jewels

Don't ask "what is wrong". Ask "what is worth protecting, and what paths reach
it". The same method covers three jobs:

- a whole system (threat model);
- one change (security review);
- an existing findings list (re-score it from the viewpoint of the crown jewels).

## 1. Reframe

In one or two sentences, say what the system really is from an attacker's point
of view: what it can read, write, sign or reach. Quote the code or config that
proves it. The real exposure is often not what the README says.

## 2. Crown jewel register

Rank by consequence, not likelihood:

| # | Jewel | Where it lives | What its loss means |
|---|---|---|---|
| J1 | ... | file, table, secret store, host | ... |

Look for:

- signing and CA keys;
- identity material (certificates, tokens);
- the integrity of data that others act on;
- credentials that pivot into other systems;
- anything that can grant privilege;
- inventories and topology.

Name the jewel the system is least equipped to protect relative to its value.
When the evidence disagrees with the register, correct the register.

## 3. Attack paths

Write one entry per path that reaches a jewel:

```
### P<n>. <origin> -> <key hops> -> <jewel>
<severity> · reaches J<n> · confirmed | unverified | corrected | broke
Adversary starts with: the role, network position or access they need
Requires: preconditions; flag any unstated assumption
Chain: numbered hops, each with file:line or read-only command/API evidence
Consequence: in operational terms, not scanner words
Chokepoint: the earliest closable hop and the minimal fix
```

- Severity:
  - catastrophic: a jewel is lost with no meaningful precondition, or attacker
    code or instructions run for every user;
  - severe: a jewel is lost after one realistic precondition (a low role, one
    write, one tricked person);
  - serious: it takes several preconditions, or the loss is partial or
    recoverable;
  - moderate: a jewel's protection weakens, or the path enables another path;
  - limited: little attacker value.
- Work through the origins one by one:
  - no account at all;
  - the lowest role, then each higher one;
  - hostile input or content;
  - read access to the host, logs or backups;
  - the supply chain (dependencies, plugins, CI);
  - a man in the middle on each external link.
- One fix that kills a whole path beats several that only narrow it.

## 4. Verify

Try to break every path before you report it:

- Re-read each hop.
- Check that each precondition really holds.
- Run whatever can be run safely in a test environment.

Mark each path confirmed, unverified (nobody has attacked it yet), corrected,
or broke under verification. Keep the broken ones in an appendix, and correct
your own earlier claims openly. The refuter must not be the analyst who wrote
the path: in Claude Code, give each path to a fresh subagent told to refute it;
elsewhere, use a second session.

## 5. Decide what to fix

- Re-score every finding by the jewel it reaches. A finding that reaches no
  jewel waits.
- Order the fixes cheapest high-impact first.
- Derive one detection per chokepoint: the log line or alert that shows the
  path being used.
- A threat model stops at this roadmap. Apply nothing without the human's
  agreement.
- In a review, fix only what the human agreed to, test each fix in a real test
  environment before committing it, and list everything else under "ignore for
  now".

## 6. Report

Keep the result: write the register into the repo's AGENTS.md "Crown jewels"
section, at most 10 lines of jewel, where it lives and its chokepoint. Later
changes are checked against that list instead of rerunning the whole method.

Open with a plain-language "Start here" for the owner:

- what they got right, specifically (this is not politeness);
- the one big cause behind most findings;
- a fix table: `#` · what's wrong · why it matters · time;
- what to ignore for now.

Then the reframe, the register and the paths with their verification status,
and an appendix with everything else. State the scope, the date and what you
could not inspect.

A threat model uses these sections, with "Start here" first; the reframe goes
in 1, the register in 2 and the paths in 5:

1. Introduction
2. Crown jewels
3. Trust boundaries
4. Threat actors
5. Attack vector analysis
6. Detection requirements
7. Implementation roadmap
8. Security assumptions

## Gotchas

- A path is not a finding until it has been verified. Label the severity of an
  unverified path as the analyst's claim.
- Anything new that can grant privilege is itself a crown jewel: an access
  repo, a signing or app key, an agent-instruction supply chain. It needs
  CODEOWNERS, required review with no self-approval, and an empty bypass list.
- Keep live exploit details (hosts, keys, unpatched paths) out of public repos,
  issues and PRs until they are fixed.
- Only test systems you own or were asked to test.
