# Rationality

Am I doing sane things? Ask it every time, with three axioms:

1. You Ain't Gonna Need It (YAGNI)
2. Don't Repeat Yourself (DRY)
3. Divide and conquer
4. Validate with reality

## 1. You Ain't Gonna Need It (YAGNI)

Keep the goal clear in mind.

This asks two things of you:
 - understand what you
are doing and why - ***what and why***
- do whatever you do in the simplest way that still meets that what
and why - ***keep it simple***

### Understand what and why

- What is the problem?
  - What are the whys behind it?
  - What does the user actually need?
  - Are you sure your idea is the solution, and that it answers the problem?
  - Does your team understand these things too?
- Which phase is the project in, and what is the target?
  - Concept: a short, measurable why, what and how.
  - Proof of concept: demonstrate the problem and the solution. All effort
    goes to velocity and the solution, the minimum to quality.
  - MVP (a production product): quality is paramount.
- Code security, information security and compliance:
  - In a proof of concept, keep code security to basic sanity. Never skip it
    past that.
  - Never skip information security; know how tight it has to be.
  - Never skip compliance; know what is required.

### Keep it simple

- Have you done it the simplest way, the simplest thing that could possibly
  work?
- Have you built only what you need now, not what you foresee needing?
- Do others find your approach simple and understandable? If only you do, it
  isn't simple.

Why: a simple program is faster to review and to develop by the book.
Spaghetti is slow to work on, and dangerous.

## 2. Don't Repeat Yourself (DRY)

Aim for efficiency and minimalism.

Make work reusable.

- Copy-pasting? Refactor into helper functions and libraries. A new library
  takes longer now and saves a lot of work later.
- Copy-pasting in a proof of concept? Fine, but if you keep doing the same
  things across proofs of concept, make a reusable library anyway.


Why: Simplicity is security, and copy-paste breeds spaghetti, which
is a nuisance and security threat too.

## 3. Divide and conquer, and validate with reality

Prove your assumptions early, cheaply and objectively.

Thinking is not enough -
verify. Make your thought to meet the grim reality and often.

Slice the work meaningfully at every level so you reach the real world
fast: build small experiments that hit real input, real data or real users:
not castles in your head.

- Did you test the idea in practice?
  - Can you show evidence that it solves the problem?
  - Did you test with realistic data, scale or user behaviour?
  - Is there measurable feedback: logs, metrics, UX or user testing?
- Did you learn from the outcome?
  - Did you adjust to what reality showed, not to what you expected?
  - Do you know how to measure success and failure?
- Did you plan for iteration?
  - Is the system easy to change when you learn new facts?
  - Is there a feedback path from users or monitoring back to development?

Why: unvalidated assumptions create waste faster than bad code. The fastest way
to move is a short learn-adjust loop. Reality is the ultimate reviewer. Consult
it early and often.
